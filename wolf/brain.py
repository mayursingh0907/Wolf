
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


class WolfBrain:

    def __init__(self):

        if not API_KEY:
            raise ValueError("Gemini API key not found.")

        self.client = genai.Client(api_key=API_KEY)

        # Conversation history
        self.history = []

        # WOLF personality
        self.system_instruction = """
        You are WOLF, a personal AI assistant.

        Your personality:
        - Friendly and intelligent.
        - Helpful and respectful.
        - Explain technical topics simply.
        - Give beginner-friendly programming help.
        - Keep answers clear and organized.
        - Remember the context of this conversation.
        """

    def think(self, question: str) -> str:

        self.history.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=question)]
            )
        )

        try:

            for attempt in range(2):

                try:

                    response = self.client.models.generate_content(
                        model=MODEL,
                        contents=self.history,
                        config=types.GenerateContentConfig(
                            system_instruction=self.system_instruction,
                            temperature=0.7
                        )
                    )

                    answer = response.text

                    if not answer:
                        return "I couldn't generate a response."

                    self.history.append(
                        types.Content(
                            role="model",
                            parts=[types.Part.from_text(text=answer)]
                        )
                    )

                    return answer

                except Exception as error:

                    error_text = str(error).upper()

                    if (
                        attempt == 0
                        and any(code in error_text for code in ["503", "429", "500", "502"])
                    ):
                        print("[WOLF] Retrying AI connection...")
                        time.sleep(2)
                        continue

                    raise error

        except Exception as error:

            print("[WOLF] AI Error:", error)

            # Remove the unanswered user message.
            if self.history and self.history[-1].role == "user":
                self.history.pop()

            return "Sorry, my AI brain is temporarily unavailable."

    def clear_memory(self):

        self.history.clear()

        return "My conversation memory has been cleared."
