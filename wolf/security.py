
# WOLF Security: only approved commands are allowed.

ALLOWED_COMMANDS = {
    "hello",
    "hi",
    "hey wolf",
    "who are you",
    "what is your name",
    "time",
    "what time is it",
    "date",
    "what is today's date",
    "help",
    "open google",
    "open youtube",
    "open github",
    "exit",
    "quit",
    "stop wolf",
}


def is_allowed_command(command: str) -> bool:
    """Check whether a command is explicitly allowed."""
    return command.strip().lower() in ALLOWED_COMMANDS
