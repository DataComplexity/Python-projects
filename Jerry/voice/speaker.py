import subprocess
import os
import tempfile
import pyttsx3
import threading

PIPER_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "piper")
MALE_VOICE_MODEL = os.path.join(PIPER_PATH, "en_US-ryan-high.onnx")
FEMALE_VOICE_MODEL = os.path.join(PIPER_PATH, "en_US-lessac-high.onnx")
PIPER_EXE = os.path.join(PIPER_PATH, "piper.exe")

class Speaker:
    def __init__(self, gender="male"):
        self.gender = gender
        self.lock = threading.Lock()
        self.piper_available = self._check_piper()

        # Fallback TTS engine
        self.engine = pyttsx3.init()
        self._configure_pyttsx3()
        print(f"[SPEAKER] TTS ready. Mode: {'Piper' if self.piper_available else 'pyttsx3 fallback'} | Voice: {gender}")

    def _check_piper(self) -> bool:
        return os.path.exists(PIPER_EXE) and (
            os.path.exists(MALE_VOICE_MODEL) or os.path.exists(FEMALE_VOICE_MODEL)
        )

    def _configure_pyttsx3(self):
        voices = self.engine.getProperty("voices")
        if not voices:
            return
        if self.gender == "female":
            for v in voices:
                if "zira" in v.name.lower() or "female" in v.name.lower():
                    self.engine.setProperty("voice", v.id)
                    break
        else:
            for v in voices:
                if "david" in v.name.lower() or "male" in v.name.lower():
                    self.engine.setProperty("voice", v.id)
                    break
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 0.95)

    def speak(self, text: str):
        if not text.strip():
            return
        print(f"[JERRY]: {text}")
        with self.lock:
            if self.piper_available:
                self._speak_piper(text)
            else:
                self._speak_pyttsx3(text)

    def _speak_piper(self, text: str):
        try:
            model = MALE_VOICE_MODEL if self.gender == "male" else FEMALE_VOICE_MODEL
            if not os.path.exists(model):
                model = MALE_VOICE_MODEL if os.path.exists(MALE_VOICE_MODEL) else FEMALE_VOICE_MODEL
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                wav_path = f.name
            result = subprocess.run(
                [PIPER_EXE, "--model", model, "--output_file", wav_path],
                input=text.encode("utf-8"),
                capture_output=True,
                timeout=15
            )
            if result.returncode == 0 and os.path.exists(wav_path):
                subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{wav_path}').PlaySync()"],
                               capture_output=True)
                os.unlink(wav_path)
            else:
                self._speak_pyttsx3(text)
        except Exception as e:
            print(f"[SPEAKER] Piper error: {e}")
            self._speak_pyttsx3(text)

    def _speak_pyttsx3(self, text: str):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[SPEAKER] TTS error: {e}")

    def switch_gender(self, gender: str):
        self.gender = gender
        self._configure_pyttsx3()
        print(f"[SPEAKER] Switched to {gender} voice.")

    def set_rate(self, rate: int):
        self.engine.setProperty("rate", rate)
