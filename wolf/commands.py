
import datetime
import re

from wolf.security import is_allowed_command


def handle_command(command: str):
    """Process user commands with basic natural language support."""

    command = command.strip().lower()

    # Remove unnecessary punctuation and extra spaces
    command = re.sub(r"[^\w\s]", "", command)
    command = " ".join(command.split())

    # Greetings
    if command in ("hello", "hi", "hey", "hey wolf"):
        return "Hello! How can I help you?", True

    # Personal conversation
    if command in ("how are you", "how are you wolf"):
        return "I am doing great! Ready to help you.", True

    # Identity
    if command in ("who are you", "what is your name"):
        return "I am WOLF, your personal AI assistant.", True

    # Time
    if command in ("time", "what time is it", "tell me the time"):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}.", True

    # Date
    if command in ("date", "today", "what is todays date"):
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        return f"Today's date is {current_date}.", True

    # Website commands
    websites = {
        "open google": "https://www.google.com",
        "open youtube": "https://www.youtube.com",
        "open github": "https://github.com",
    }

    if command in websites:
        return f"Here is the link: {websites[command]}", True

    # Help
    if command == "help":
        return (
            "I can greet you, tell time and date, "
            "answer how I am, introduce myself, "
            "and provide Google, YouTube and GitHub links.",
            True
        )

    # Exit
    if command in ("exit", "quit", "stop wolf", "goodbye"):
        return "WOLF is shutting down. Goodbye!", False

    return (
        "I don't know that yet. My AI brain will be upgraded soon.",
        True
    )
