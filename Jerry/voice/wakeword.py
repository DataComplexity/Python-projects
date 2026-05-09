import pyaudio
import numpy as np
import threading
import time

try:
    from openwakeword.model import Model as WakeModel
    OWW_AVAILABLE = True
except ImportError:
    OWW_AVAILABLE = False
    print("[WAKEWORD] openwakeword not available. Using keyboard fallback.")

CHUNK = 1280
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
WAKE_WORDS = ["hey jerry", "jerry"]

class WakeWordListener:
    def __init__(self, callback):
        self.callback = callback
        self.running = False
        self.audio = pyaudio.PyAudio()

        if OWW_AVAILABLE:
            self.model = WakeModel(wakeword_models=["hey_jarvis"], inference_framework="onnx")
            print("[WAKEWORD] Wake word model loaded. Say 'Hey Jerry' to activate.")
        else:
            print("[WAKEWORD] Using keyboard fallback — press Enter to activate Jerry.")

    def listen(self):
        self.running = True
        if OWW_AVAILABLE:
            self._listen_audio()
        else:
            self._listen_keyboard()

    def _listen_audio(self):
        stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        print("[WAKEWORD] Listening for 'Hey Jerry'...")
        try:
            while self.running:
                audio_chunk = stream.read(CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
                predictions = self.model.predict(audio_data)
                for name, score in predictions.items():
                    if score > 0.5:
                        print(f"\n[WAKEWORD] Detected! ({name}: {score:.2f})")
                        stream.stop_stream()
                        self.callback()
                        time.sleep(1)
                        stream.start_stream()
                        break
        except Exception as e:
            print(f"[WAKEWORD] Error: {e}")
        finally:
            stream.stop_stream()
            stream.close()

    def _listen_keyboard(self):
        print("[WAKEWORD] Press Enter anytime to talk to Jerry...")
        while self.running:
            try:
                input()
                self.callback()
            except EOFError:
                break

    def stop(self):
        self.running = False
