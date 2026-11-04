"""Small allowlist helpers. Desktop actions never execute arbitrary shell text."""

ALLOWED_APPS = {"notepad", "calculator", "vs code"}
ALLOWED_WEBSITES = {"google", "youtube", "github", "instagram"}


def is_allowed_app(name: str) -> bool:
    return (name or "").strip().lower() in ALLOWED_APPS


def is_allowed_website(name: str) -> bool:
    return (name or "").strip().lower() in ALLOWED_WEBSITES
