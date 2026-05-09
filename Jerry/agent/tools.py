import os
import subprocess
import platform
import shutil
import psutil
import pyperclip
import webbrowser
from datetime import datetime
from search.web import WebSearch

SENSITIVE_ACTIONS = ["delete", "run_script", "install", "format", "shutdown", "restart", "kill_process"]

ACTION_KEYWORDS = {
    "open_app": ["open", "launch", "start", "khol"],
    "close_app": ["close", "quit", "band kar", "terminate"],
    "search_web": ["search", "google", "find online", "dhundh", "look up"],
    "read_file": ["read", "show file", "open file", "padh"],
    "write_file": ["write", "create file", "save file", "likho"],
    "delete": ["delete", "remove", "hatao", "mita do"],
    "list_files": ["list files", "show files", "files dikhao", "what's in"],
    "copy_file": ["copy", "duplicate"],
    "move_file": ["move", "shift"],
    "run_script": ["run script", "execute", "chalao script"],
    "screenshot": ["screenshot", "capture screen", "screen capture"],
    "clipboard": ["clipboard", "copy text", "paste text"],
    "system_info": ["system info", "cpu", "ram", "memory", "disk space", "battery"],
    "shutdown": ["shutdown", "band karo pc", "turn off pc"],
    "restart": ["restart", "reboot"],
    "kill_process": ["kill", "force close", "stop process"],
    "open_browser": ["open browser", "open chrome", "open edge", "browser khol"],
    "volume": ["volume", "louder", "quieter", "mute", "unmute"],
    "time_date": ["time", "date", "aaj ka din", "kitne baje"],
    "weather": ["weather", "mausam"],
    "calculator": ["calculate", "calculator", "hisaab"],
}

class ToolHandler:
    def __init__(self, agent=None):
        self.agent = agent
        self.searcher = WebSearch()
        self.os_type = platform.system()

    def detect_action(self, user_input: str) -> str | None:
        text = user_input.lower()
        for action, keywords in ACTION_KEYWORDS.items():
            if any(k in text for k in keywords):
                return action
        return None

    def is_sensitive(self, action: str) -> bool:
        return action in SENSITIVE_ACTIONS

    def execute(self, action: str, user_input: str) -> str:
        try:
            handlers = {
                "open_app": self.open_app,
                "close_app": self.close_app,
                "search_web": self.search_web,
                "read_file": self.read_file,
                "write_file": self.write_file,
                "delete": self.delete_file,
                "list_files": self.list_files,
                "copy_file": self.copy_file,
                "run_script": self.run_script,
                "screenshot": self.screenshot,
                "clipboard": self.clipboard_read,
                "system_info": self.system_info,
                "shutdown": self.shutdown,
                "restart": self.restart,
                "kill_process": self.kill_process,
                "open_browser": self.open_browser,
                "time_date": self.time_date,
                "calculator": self.calculator,
            }
            handler = handlers.get(action)
            if handler:
                return handler(user_input)
            return f"No handler for action: {action}"
        except Exception as e:
            return f"Error executing {action}: {str(e)}"

    def open_app(self, user_input: str) -> str:
        apps = {
            "chrome": "chrome", "browser": "chrome",
            "notepad": "notepad", "calculator": "calc",
            "explorer": "explorer", "files": "explorer",
            "vs code": "code", "vscode": "code",
            "spotify": "spotify", "vlc": "vlc",
            "word": "winword", "excel": "excel",
            "terminal": "cmd", "cmd": "cmd",
            "powershell": "powershell",
            "task manager": "taskmgr",
            "settings": "ms-settings:",
        }
        text = user_input.lower()
        for name, cmd in apps.items():
            if name in text:
                os.startfile(cmd) if cmd.endswith(":") else subprocess.Popen(cmd, shell=True)
                return f"Opened {name}"
        return "App not recognized. Please specify the app name."

    def close_app(self, user_input: str) -> str:
        text = user_input.lower()
        for proc in psutil.process_iter(['name', 'pid']):
            if any(word in proc.info['name'].lower() for word in text.split()):
                proc.kill()
                return f"Closed {proc.info['name']}"
        return "Process not found."

    def search_web(self, user_input: str) -> str:
        query = user_input.lower()
        for kw in ["search", "google", "find online", "dhundh", "look up"]:
            query = query.replace(kw, "").strip()
        results = self.searcher.search(query)
        return results

    def read_file(self, user_input: str) -> str:
        path = self._extract_path(user_input)
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(3000)
            return f"File contents:\n{content}"
        return f"File not found: {path}"

    def write_file(self, user_input: str) -> str:
        path = self._extract_path(user_input)
        if path:
            content = input("[JERRY] What should I write in the file? ")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"File written: {path}"
        return "Please specify a file path."

    def delete_file(self, user_input: str) -> str:
        path = self._extract_path(user_input)
        if path and os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return f"Deleted: {path}"
        return f"Path not found: {path}"

    def list_files(self, user_input: str) -> str:
        path = self._extract_path(user_input) or os.path.expanduser("~")
        if os.path.exists(path):
            items = os.listdir(path)
            return f"Files in {path}:\n" + "\n".join(items[:30])
        return f"Path not found: {path}"

    def copy_file(self, user_input: str) -> str:
        parts = user_input.split(" to ")
        if len(parts) == 2:
            src = self._extract_path(parts[0])
            dst = self._extract_path(parts[1])
            if src and dst:
                shutil.copy2(src, dst)
                return f"Copied {src} → {dst}"
        return "Please specify source and destination: copy [file] to [destination]"

    def run_script(self, user_input: str) -> str:
        path = self._extract_path(user_input)
        if path and os.path.exists(path):
            result = subprocess.run(["python", path], capture_output=True, text=True, timeout=30)
            return result.stdout or result.stderr
        return f"Script not found: {path}"

    def screenshot(self, user_input: str) -> str:
        try:
            import pyautogui
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.expanduser(f"~/Pictures/jerry_screenshot_{timestamp}.png")
            pyautogui.screenshot(path)
            return f"Screenshot saved: {path}"
        except Exception as e:
            return f"Screenshot failed: {e}"

    def clipboard_read(self, user_input: str) -> str:
        content = pyperclip.paste()
        return f"Clipboard contents:\n{content}"

    def system_info(self, user_input: str) -> str:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        info = f"""System Info:
CPU Usage: {cpu}%
RAM: {ram.used // (1024**2)}MB used / {ram.total // (1024**2)}MB total ({ram.percent}%)
Disk: {disk.used // (1024**3)}GB used / {disk.total // (1024**3)}GB total ({disk.percent}%)"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                info += f"\nBattery: {battery.percent}% {'(Charging)' if battery.power_plugged else '(Discharging)'}"
        except:
            pass
        return info

    def shutdown(self, user_input: str) -> str:
        subprocess.run(["shutdown", "/s", "/t", "30"], shell=True)
        return "PC will shut down in 30 seconds. Type 'shutdown /a' in cmd to cancel."

    def restart(self, user_input: str) -> str:
        subprocess.run(["shutdown", "/r", "/t", "30"], shell=True)
        return "PC will restart in 30 seconds."

    def kill_process(self, user_input: str) -> str:
        text = user_input.lower()
        for proc in psutil.process_iter(['name', 'pid']):
            if any(word in proc.info['name'].lower() for word in text.split()):
                proc.kill()
                return f"Killed process: {proc.info['name']} (PID: {proc.info['pid']})"
        return "Process not found."

    def open_browser(self, user_input: str) -> str:
        webbrowser.open("https://google.com")
        return "Browser opened."

    def time_date(self, user_input: str) -> str:
        now = datetime.now()
        return f"Current time: {now.strftime('%I:%M %p')}\nDate: {now.strftime('%A, %d %B %Y')}"

    def calculator(self, user_input: str) -> str:
        import re
        expr = re.sub(r"[^0-9+\-*/().\s]", "", user_input)
        try:
            result = eval(expr)
            return f"Result: {result}"
        except:
            subprocess.Popen("calc", shell=True)
            return "Opened calculator."

    def _extract_path(self, text: str) -> str | None:
        words = text.split()
        for word in words:
            if "/" in word or "\\" in word or word.endswith((".py", ".txt", ".pdf", ".csv", ".json", ".docx", ".xlsx")):
                return word.strip("'\"")
        return None
