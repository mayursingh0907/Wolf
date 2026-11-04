import csv
import ctypes
import io
import subprocess
import webbrowser
from ctypes import wintypes
from urllib.parse import quote_plus


class WolfDesktop:
    def __init__(self):
        self.apps = {
            "notepad": {
                "command": ["notepad.exe"],
                "processes": ["notepad.exe"],
            },
            "calculator": {
                "command": ["calc.exe"],
                "processes": ["calculator.exe", "calculatorapp.exe"],
            },
            "vs code": {
                "command": ["code"],
                "processes": ["code.exe"],
            },
        }

        self.websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://github.com",
            "instagram": "https://www.instagram.com",
        }

    def open_app(self, app_name):
        app_name = app_name.lower().strip()
        if app_name not in self.apps:
            return "This application is not in my approved list."

        try:
            subprocess.Popen(self.apps[app_name]["command"], shell=False)
            return f"Opening {app_name}."
        except FileNotFoundError:
            return f"I couldn't find {app_name}. Check whether it is installed and available in PATH."
        except Exception as error:
            return f"Application error: {error}"

    def open_website(self, site_name):
        site_name = site_name.lower().strip()
        if site_name not in self.websites:
            return "This website is not in my approved list."

        try:
            opened = webbrowser.open_new_tab(self.websites[site_name])
            return f"Opening {site_name}." if opened else f"I couldn't open {site_name} in your default browser."
        except Exception as error:
            return f"Website error: {error}"

    def open_target(self, target):
        target = target.lower().strip()
        if target in self.apps:
            return self.open_app(target)
        if target in self.websites:
            return self.open_website(target)
        return (
            f"{target} is not in my approved app or website list. "
            "I have not run any system command."
        )

    def close_app(self, app_name):
        app_name = app_name.lower().strip()

        if app_name in self.websites:
            return (
                f"{app_name} is a browser tab, not a separate desktop app. "
                "Browser-tab closing is not enabled yet, so I won't close your whole browser."
            )

        if app_name not in self.apps:
            return "I can only close applications in my approved list: Notepad, Calculator and VS Code."

        if not hasattr(ctypes, "WinDLL"):
            return "Closing desktop applications is supported on Windows only."

        try:
            result = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                shell=False,
                check=False,
            )
            process_by_pid = {}
            for row in csv.reader(io.StringIO(result.stdout)):
                if len(row) >= 2:
                    try:
                        process_by_pid[int(row[1])] = row[0].lower()
                    except ValueError:
                        continue

            allowed_processes = set(self.apps[app_name]["processes"])
            user32 = ctypes.WinDLL("user32", use_last_error=True)
            WM_CLOSE = 0x0010
            windows_to_close = []

            callback_type = ctypes.WINFUNCTYPE(
                wintypes.BOOL, wintypes.HWND, wintypes.LPARAM
            )

            user32.IsWindowVisible.argtypes = [wintypes.HWND]
            user32.IsWindowVisible.restype = wintypes.BOOL
            user32.GetWindowThreadProcessId.argtypes = [
                wintypes.HWND,
                ctypes.POINTER(wintypes.DWORD),
            ]
            user32.GetWindowThreadProcessId.restype = wintypes.DWORD
            user32.PostMessageW.argtypes = [
                wintypes.HWND,
                wintypes.UINT,
                wintypes.WPARAM,
                wintypes.LPARAM,
            ]
            user32.PostMessageW.restype = wintypes.BOOL

            def callback(hwnd, _):
                if not user32.IsWindowVisible(hwnd):
                    return True

                process_id = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
                if process_by_pid.get(process_id.value, "") in allowed_processes:
                    windows_to_close.append(hwnd)
                return True

            enum_callback = callback_type(callback)
            user32.EnumWindows.argtypes = [callback_type, wintypes.LPARAM]
            user32.EnumWindows.restype = wintypes.BOOL
            user32.EnumWindows(enum_callback, 0)

            closed = 0
            for hwnd in set(windows_to_close):
                if user32.PostMessageW(hwnd, WM_CLOSE, 0, 0):
                    closed += 1

            if closed:
                return f"Close request sent to {app_name}. Any unsaved-work prompt will remain visible."
            return f"{app_name} is not running or has no closable window."

        except Exception as error:
            return f"Close application error: {error}"

    def search_google(self, query):
        query = (query or "").strip()
        for suffix in (" in google", " on google"):
            if query.lower().endswith(suffix):
                query = query[:-len(suffix)].strip()

        if not query:
            return "Please tell me what to search."

        try:
            url = "https://www.google.com/search?q=" + quote_plus(query)
            opened = webbrowser.open_new_tab(url)
            return (
                f"Searching Google for {query}."
                if opened
                else "I couldn't open Google in your default browser."
            )
        except Exception as error:
            return f"Google search error: {error}"
