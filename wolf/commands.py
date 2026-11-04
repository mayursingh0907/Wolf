import re


def normalize_command(text: str) -> str:
    """Normalize recognized speech without destroying search punctuation."""
    text = (text or "").lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text.strip(" \t\r\n.!?,")


def parse_command(command: str):
    """
    Return (action, argument).
    Unknown text is passed to Gemini by main.py.
    """
    command = normalize_command(command)

    # Google search phrases must be checked before generic 'open ...'.
    search_patterns = [
        r"(?:open )?google and search(?: for)?(?:\s+(.+))?",
        r"(?:open )?google search(?: for)?(?:\s+(.+))?",
        r"search google for\s+(.+)",
        r"google search\s+(.+)",
        r"search for\s+(.+)",
        r"search\s+(.+)",
    ]
    for pattern in search_patterns:
        match = re.fullmatch(pattern, command)
        if match:
            query = (match.group(1) or "").strip()
            if query:
                return "search_google", query
            return "open_google_search", ""

    # Volume controls
    match = re.fullmatch(r"(?:set|change) volume to (\d+)\s*(?:%|percent)?", command)
    if match:
        return "set_volume", int(match.group(1))

    match = re.fullmatch(
        r"(?:increase|raise|turn up) volume(?: by (\d+)\s*(?:%|percent)?)?",
        command,
    )
    if match or command in {"volume up", "increase volume"}:
        return "volume_up", int(match.group(1)) if match and match.group(1) else 10

    match = re.fullmatch(
        r"(?:decrease|lower|reduce|turn down) volume(?: by (\d+)\s*(?:%|percent)?)?",
        command,
    )
    if match or command in {"volume down", "decrease volume"}:
        return "volume_down", int(match.group(1)) if match and match.group(1) else 10

    if command in {"mute", "mute volume", "silence volume"}:
        return "mute", None
    if command in {"unmute", "unmute volume", "restore volume"}:
        return "unmute", None
    if command in {"what is the volume", "check volume", "current volume"}:
        return "get_volume", None

    # Date, time and help
    if command in {"time", "what time is it", "tell me the time"}:
        return "time", None
    if command in {"date", "today", "what is today's date", "what is todays date"}:
        return "date", None
    if command in {"help", "what can you do"}:
        return "help", None
    if command in {"clear memory", "forget this conversation"}:
        return "clear_memory", None

    # Open and close commands
    match = re.fullmatch(r"open\s+(.+)", command)
    if match:
        return "open", match.group(1).strip()

    match = re.fullmatch(r"close\s+(.+)", command)
    if match:
        return "close", match.group(1).strip()

    return "unknown", None
