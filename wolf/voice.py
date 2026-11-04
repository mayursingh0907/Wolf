
"""WOLF microphone input and ElevenLabs bilingual speech output."""

import base64
import os
import subprocess
import tempfile
import threading
import wave
from pathlib import Path

import speech_recognition as sr
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

POWERSHELL_TTS_SCRIPT = r'''
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.Volume = 100
$speaker.Rate = 2
[Console]::Out.WriteLine('WOLF_READY')
[Console]::Out.Flush()
while (($line = [Console]::In.ReadLine()) -ne $null) {
    try {
        $bytes = [Convert]::FromBase64String($line)
        $text = [Text.Encoding]::UTF8.GetString($bytes)
        if ($text) { $speaker.Speak($text) }
        [Console]::Out.WriteLine('WOLF_DONE')
    }
    catch {
        [Console]::Out.WriteLine('WOLF_TTS_ERROR')
    }
    [Console]::Out.Flush()
}
$speaker.Dispose()
'''


class WolfVoice:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.45
        self.recognizer.non_speaking_duration = 0.25
        self.recognizer.phrase_threshold = 0.2
        self.recognizer.operation_timeout = 8

        self._tts_process = None
        self._tts_lock = threading.Lock()
        self._elevenlabs_client = None

        # Brian: Deep, Resonant and Comforting
        self._elevenlabs_voice_id = os.getenv(
            "ELEVENLABS_VOICE_ID",
            "nPczCjzI2devNBz1zQrb"
        ).strip()

        # Hindi + English multilingual model
        self._elevenlabs_model_id = os.getenv(
            "ELEVENLABS_MODEL_ID",
            "eleven_multilingual_v2"
        ).strip()

        self._tts_provider = os.getenv(
            "WOLF_TTS_PROVIDER",
            "elevenlabs"
        ).strip().lower()

        # English first; Hindi fallback
        language_setting = os.getenv(
            "WOLF_STT_LANGUAGES",
            "en-IN,hi-IN"
        )

        self._stt_languages = [
            item.strip()
            for item in language_setting.split(",")
            if item.strip()
        ] or ["en-IN", "hi-IN"]

        api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()

        if self._tts_provider == "elevenlabs" and api_key:
            try:
                from elevenlabs.client import ElevenLabs

                self._elevenlabs_client = ElevenLabs(
                    api_key=api_key
                )

                print(
                    f"[VOICE] ElevenLabs enabled | Brian | "
                    f"{self._elevenlabs_model_id}"
                )

            except Exception as error:
                print("[VOICE] ElevenLabs initialization failed:", error)
                print("[VOICE] Windows speech fallback is available.")

        elif self._tts_provider == "elevenlabs":
            print(
                "[VOICE] ELEVENLABS_API_KEY missing; "
                "using Windows speech fallback."
            )

        else:
            print("[VOICE] Windows speech output selected.")

        print("[VOICE] Bilingual microphone input initialized.")

    def speak(self, text: str):

        text = str(text or "").strip()

        if not text:
            return

        if len(text) > 1200:
            text = (
                text[:1200].rsplit(" ", 1)[0].rstrip()
                + ". The remaining answer is on the screen."
            )

        with self._tts_lock:

            if (
                self._elevenlabs_client is not None
                and self._tts_provider == "elevenlabs"
            ):
                try:
                    self._speak_elevenlabs(text)
                    return

                except Exception as error:
                    print("[ELEVENLABS ERROR]", error)
                    print(
                        "[VOICE] Using Windows speech for this response."
                    )

            self._speak_windows(text)

    def _speak_elevenlabs(self, text: str):

        import winsound

        audio_chunks = self._elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id=self._elevenlabs_voice_id,
            model_id=self._elevenlabs_model_id,
            output_format="pcm_44100",
        )

        pcm_audio = b"".join(
            chunk
            for chunk in audio_chunks
            if isinstance(chunk, bytes)
        )

        if not pcm_audio:
            raise RuntimeError("ElevenLabs returned empty audio.")

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as temp_file:
                temp_path = temp_file.name

            with wave.open(temp_path, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(44100)
                wav_file.writeframes(pcm_audio)

            winsound.PlaySound(
                temp_path,
                winsound.SND_FILENAME
            )

        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    def _start_tts(self):

        if (
            self._tts_process
            and self._tts_process.poll() is None
        ):
            return

        self._tts_process = None

        creation_flags = getattr(
            subprocess,
            "CREATE_NO_WINDOW",
            0
        )

        process = subprocess.Popen(
            [
                "powershell.exe",
                "-NoLogo",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                POWERSHELL_TTS_SCRIPT,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            creationflags=creation_flags,
        )

        ready = process.stdout.readline().strip()

        if ready != "WOLF_READY":
            process.terminate()
            raise RuntimeError(
                "Windows speech engine could not start."
            )

        self._tts_process = process

    def _speak_windows(self, text: str):

        try:
            self._start_tts()

            payload = base64.b64encode(
                text.encode("utf-8")
            ).decode("ascii")

            self._tts_process.stdin.write(payload + "\n")
            self._tts_process.stdin.flush()

            status = self._tts_process.stdout.readline().strip()

            if status != "WOLF_DONE":
                print(
                    "[VOICE ERROR] Windows speech "
                    "did not complete normally."
                )

        except FileNotFoundError:
            print(
                "[VOICE ERROR] PowerShell was not found."
            )

        except Exception as error:
            print("[VOICE ERROR]", error)
            self._stop_tts()

    def listen(self, timeout=8, phrase_time_limit=8):

        try:
            with sr.Microphone() as source:

                print("\n[WOLF] Listening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )

            print("[WOLF] Recognizing speech...")

            for language in self._stt_languages:

                try:
                    text = self.recognizer.recognize_google(
                        audio,
                        language=language
                    ).strip()

                    if text:
                        print(f"[YOU - {language}]", text)
                        return text

                except sr.UnknownValueError:
                    continue

                except sr.RequestError as error:
                    print("[VOICE NETWORK ERROR]", error)
                    return None

            print(
                "[WOLF] I couldn't understand. Please try again."
            )

            return None

        except sr.WaitTimeoutError:
            return None

        except Exception as error:
            print("[MIC ERROR]", error)
            return None

    def _stop_tts(self):

        process = self._tts_process
        self._tts_process = None

        if not process:
            return

        try:
            if process.stdin and not process.stdin.closed:
                process.stdin.close()

            process.wait(timeout=3)

        except Exception:
            try:
                process.terminate()
                process.wait(timeout=2)
            except Exception:
                pass

    def close(self):

        with self._tts_lock:
            self._stop_tts()
