# WOLF AI Assistant — Source Update

This source bundle contains the WOLF Python files. It does not include your
private `.env` file, virtual environment, or Vosk model.

## Requirements

- Windows 10/11
- Python 3.12 (recommended)
- A microphone and speakers
- Internet for Google Speech Recognition and Gemini
- Your existing Vosk model folder

## Setup

From PowerShell, inside your `Wolf` project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Keep your existing `models` folder in the project root:

```text
Wolf/
  models/
    vosk-model-small-en-us-0.15/
```

Create `.env` in the project root. Put your own Gemini key in it:

```env
GEMINI_API_KEY=your_private_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Never upload `.env` to GitHub or share its contents.

Run:

```powershell
python main.py
```

## Commands

- Wake up WOLF
- Open Notepad / Calculator / VS Code
- Close Notepad / Calculator / VS Code
- Open Google / YouTube / GitHub / Instagram
- Open Google and search for Python
- Open Google and search, then say your search query
- Search Google for AI projects
- Increase volume by 10 percent
- Decrease volume by 10 percent
- Set volume to 50 percent
- Mute / Unmute
- What is the volume?
- What time is it?
- What is today's date?
- Clear memory
- Keyboard mode / Voice mode
- Stop WOLF

## Notes and limitations

- Voice recognition uses Google's online speech recognition, so it needs internet.
- Wake-word detection uses Vosk offline.
- Gemini response time depends on internet, API availability, and model load.
- App closing sends a normal Windows close message; it does not force-kill apps.
- Browser-tab closing is deliberately not enabled. Closing Instagram as a tab
  without risking the entire browser requires a separate browser integration.
- Brightness control is not included because laptop display support varies.
