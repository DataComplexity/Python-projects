import speech_recognition as sr
from faster_whisper import WhisperModel
import numpy as np
import io
import wave

class VoiceListener:
    def __init__(self, model_size="small"):
        print("[VOICE] Loading Whisper model...")
        self.whisper = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        print("[VOICE] Whisper ready.")

    def listen(self, timeout=8, phrase_limit=15) -> str:
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("[VOICE] Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
                return self._transcribe(audio)
            except sr.WaitTimeoutError:
                return ""
            except Exception as e:
                print(f"[VOICE] Listen error: {e}")
                return ""

    def _transcribe(self, audio: sr.AudioData) -> str:
        try:
            wav_bytes = audio.get_wav_data()
            wav_file = io.BytesIO(wav_bytes)
            segments, info = self.whisper.transcribe(wav_file, beam_size=5, language="en")
            text = " ".join(seg.text for seg in segments).strip()
            print(f"[VOICE] Heard: {text} (lang: {info.language})")
            return text
        except Exception as e:
            print(f"[VOICE] Transcribe error: {e}")
            return ""
