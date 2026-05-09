import os
import sys

COMMANDS = """
┌─────────────────────────────────────────────┐
│  JERRY TERMINAL COMMANDS                    │
│  /status     — show brain & memory info     │
│  /switch     — switch AI brain              │
│  /memory     — show memory count            │
│  /clear      — clear conversation history  │
│  /voice male — switch to male voice         │
│  /voice female — switch to female voice     │
│  /auto       — toggle auto-mode             │
│  /help       — show this menu               │
│  /quit       — exit Jerry                   │
└─────────────────────────────────────────────┘
"""

class TerminalUI:
    def __init__(self, agent, speaker):
        self.agent = agent
        self.speaker = speaker

    def run(self):
        print(COMMANDS)
        print("[JERRY] Terminal ready. Type your message or a /command.\n")

        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    self._handle_command(user_input)
                    continue

                # Send to agent
                response = self.agent.chat(user_input, source="terminal")
                print(f"\nJerry: {response}\n")
                self.speaker.speak(response)

            except KeyboardInterrupt:
                print("\n[JERRY] Goodbye! Shutting down...")
                sys.exit(0)
            except Exception as e:
                print(f"[ERROR] {e}")

    def _handle_command(self, cmd: str):
        cmd = cmd.lower().strip()

        if cmd == "/quit":
            print("[JERRY] Goodbye!")
            sys.exit(0)

        elif cmd == "/help":
            print(COMMANDS)

        elif cmd == "/status":
            status = self.agent.get_status()
            print(f"\n[STATUS]")
            print(f"  Brain     : {status['brain']}")
            print(f"  Auto-mode : {'ON' if status['auto_mode'] else 'OFF'}")
            print(f"  Memory    : {status['memory_entries']} entries\n")

        elif cmd == "/memory":
            count = self.agent.memory.count()
            print(f"[MEMORY] {count} entries stored locally.\n")

        elif cmd == "/clear":
            self.agent.history = []
            print("[JERRY] Conversation history cleared.\n")

        elif cmd == "/auto":
            self.agent.auto_mode = not self.agent.auto_mode
            state = "ON" if self.agent.auto_mode else "OFF"
            print(f"[JERRY] Auto-mode {state}\n")
            self.speaker.speak(f"Auto mode is now {state}")

        elif cmd.startswith("/voice"):
            parts = cmd.split()
            if len(parts) > 1:
                gender = parts[1]
                self.speaker.switch_gender(gender)
                print(f"[JERRY] Voice switched to {gender}.\n")
            else:
                print("[JERRY] Usage: /voice male  or  /voice female\n")

        elif cmd == "/switch":
            print("[JERRY] Available brains:")
            from agent.graph import AVAILABLE_BRAINS
            for name, model in AVAILABLE_BRAINS.items():
                marker = " <-- active" if name == self.agent.current_brain else ""
                print(f"  {name} ({model}){marker}")
            choice = input("Switch to: ").strip()
            if choice in AVAILABLE_BRAINS:
                self.agent.switch_brain(choice)
                self.speaker.speak(f"Brain switched to {choice}")
            else:
                print("[JERRY] Unknown brain name.\n")

        else:
            print(f"[JERRY] Unknown command: {cmd}. Type /help for options.\n")
