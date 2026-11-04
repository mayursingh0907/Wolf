from pycaw.pycaw import AudioUtilities


class WolfSystem:
    def __init__(self):
        self.volume = None
        self.connect_audio()

    def connect_audio(self):
        try:
            device = AudioUtilities.GetSpeakers()
            self.volume = device.EndpointVolume
            print("[SYSTEM] Windows audio control connected.")
        except Exception as error:
            self.volume = None
            print("[SYSTEM ERROR] Audio connection:", error)

    def get_volume(self):
        if self.volume is None:
            return None
        try:
            return round(self.volume.GetMasterVolumeLevelScalar() * 100)
        except Exception as error:
            print("[SYSTEM ERROR] Reading volume:", error)
            return None

    def set_volume(self, level):
        if self.volume is None:
            return "Audio control is unavailable."
        try:
            level = max(0, min(100, int(level)))
            self.volume.SetMasterVolumeLevelScalar(level / 100, None)
            self.volume.SetMute(0, None)
            return f"Volume set to {level} percent."
        except Exception as error:
            return f"Could not change volume: {error}"

    def volume_up(self, amount=10):
        current = self.get_volume()
        if current is None:
            return "Audio control is unavailable."
        return self.set_volume(current + max(0, int(amount)))

    def volume_down(self, amount=10):
        current = self.get_volume()
        if current is None:
            return "Audio control is unavailable."
        return self.set_volume(current - max(0, int(amount)))

    def mute(self):
        if self.volume is None:
            return "Audio control is unavailable."
        try:
            self.volume.SetMute(1, None)
            return "Volume muted."
        except Exception as error:
            return f"Could not mute volume: {error}"

    def unmute(self):
        if self.volume is None:
            return "Audio control is unavailable."
        try:
            self.volume.SetMute(0, None)
            return "Volume unmuted."
        except Exception as error:
            return f"Could not unmute volume: {error}"
