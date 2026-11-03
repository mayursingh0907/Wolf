
class WolfVoice:

    def __init__(self):
        self.enabled = False

    def listen(self):
        raise NotImplementedError(
            "Voice input will be enabled in the Windows version."
        )

    def speak(self, message: str):
        print(f"WOLF: {message}")
