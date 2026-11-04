import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


class WolfBrain:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add it to the .env file in the Wolf project folder."
            )

        self.client = genai.Client(api_key=api_key)
        self.history = []
        self.max_history_messages = 12

        self.system_instruction = """
You are WOLF, a helpful personal AI assistant.
Be friendly, accurate, and concise by default.
Explain technical topics in beginner-friendly steps.
Use the conversation context when it is relevant.
Do not claim to have performed computer actions unless a tool actually did them.
"""

    def think(self, question: str) -> str:
        self.history.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=question)],
            )
        )

        # Keep recent context bounded to reduce request size and latency.
        request_history = self.history[-self.max_history_messages:]

        try:
            response = self.client.models.generate_content(
                model=MODEL,
                contents=request_history,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.5,
                    max_output_tokens=512,
                ),
            )

            answer = (response.text or "").strip()
            if not answer:
                answer = "I couldn't generate a response. Please try again."

            self.history.append(
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=answer)],
                )
            )
            self.history = self.history[-self.max_history_messages:]
            return answer

        except Exception as error:
            print("[WOLF] AI Error:", error)

            if self.history and getattr(self.history[-1], "role", None) == "user":
                self.history.pop()

            error_text = str(error).lower()
            if "429" in error_text or "resource_exhausted" in error_text:
                return "Gemini is rate-limited right now. Please wait a moment and try again."
            if "404" in error_text or "not_found" in error_text:
                return f"The configured Gemini model ({MODEL}) was not found. Check GEMINI_MODEL in your .env file."
            return "Sorry, my AI brain is temporarily unavailable. Please check your internet connection and Gemini settings."

    def clear_memory(self):
        self.history.clear()
        return "Conversation memory cleared."
