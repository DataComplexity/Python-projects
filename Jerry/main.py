import threading
import sys
import os
import subprocess
from agent.graph import JerryAgent
from voice.wakeword import WakeWordListener
from voice.listener import VoiceListener
from voice.speaker import Speaker
from ui.terminal import TerminalUI

BANNER = """
     _  ___ ___ _____   ___   _ 
    | || __| _ \\ _ \\ \\ / / | | |
 _  | || _||   /  _/\\ V /| |_| |
| |_/ /|___|_|_\\_|   |_|  \\___/ 
 \\___/  Personal AI Assistant   
        by Lakshya | v1.0
"""

def main():
    print(BANNER)
    print("[JERRY] Initializing systems...\n")

    agent = JerryAgent()
    speaker = Speaker()
    voice_listener = VoiceListener()
    wake_listener = WakeWordListener(
        callback=lambda: handle_voice(agent, speaker, voice_listener)
    )

    speaker.speak("Hello! Jerry here. Say Hey Jerry anytime or type below.")

    # Launch Streamlit UI in background
    ui_thread = threading.Thread(
        target=lambda: subprocess.Popen(
            ["streamlit", "run", "ui/app.py",
             "--server.headless", "false",
             "--server.port", "8501"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        ),
        daemon=True
    )
    ui_thread.start()
    print("[JERRY] Streamlit UI → http://localhost:8501")

    # Wake word listener in background
    wake_thread = threading.Thread(target=wake_listener.listen, daemon=True)
    wake_thread.start()

    # Terminal UI on main thread
    terminal = TerminalUI(agent=agent, speaker=speaker)
    terminal.run()


def handle_voice(agent, speaker, voice_listener):
    speaker.speak("Yes? I'm listening.")
    text = voice_listener.listen()
    if text:
        print(f"\n[YOU - voice]: {text}")
        response = agent.chat(text, source="voice")
        print(f"[JERRY]: {response}\n")
        speaker.speak(response)


if __name__ == "__main__":
    main()
