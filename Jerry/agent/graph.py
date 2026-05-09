from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
from agent.memory import MemoryManager
from agent.tools import ToolHandler

AVAILABLE_BRAINS = {
    "phi4-mini": "phi4-mini",
    "qwen3.5": "qwen3:4b",
    "qwen2.5": "qwen2.5-coder:7b",
}

SYSTEM_PROMPT = """You are Jerry, a highly capable personal AI assistant for Lakshya running on Windows.

Your personality:
- Helpful, direct, and intelligent
- You speak both Hindi and British English naturally — mix them as the user does
- Always use British English spelling and phrasing (colour not color, realise not realize, whilst, cheers, etc.)
- You have a male and female voice mode available
- You always confirm before doing tasks UNLESS the user has said "you can handle it yourself"
- You remember past conversations and user preferences
- You are private — no data leaves this machine

Your capabilities:
- Chat and answer questions
- Search the web (Google + DuckDuckGo)
- Control PC: open/close apps, manage files, run scripts
- Read and write files
- Remember context across sessions

Confirmation rules:
- ALWAYS ask before: deleting files, running scripts, installing anything, sending anything
- AUTO-HANDLE: web searches, opening apps, reading files, answering questions
- If user says "handle it yourself" or "kar le" — switch to auto mode for that session

Current brain: {brain}
Auto-mode: {auto_mode}
"""

class AgentState(TypedDict):
    messages: List
    last_input: str
    response: str
    auto_mode: bool
    requires_confirmation: bool
    pending_action: Optional[str]

class JerryAgent:
    def __init__(self, brain="phi4-mini"):
        self.current_brain = brain
        self.auto_mode = False
        self.llm = ChatOllama(model=AVAILABLE_BRAINS.get(brain, brain))
        self.memory = MemoryManager()
        self.tools = ToolHandler(agent=self)
        self.history = []
        self.pending_action = None
        self.graph = self._build_graph()
        print(f"[JERRY] Brain loaded: {brain}")

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("think", self._think_node)
        graph.add_node("confirm", self._confirm_node)
        graph.add_node("execute", self._execute_node)
        graph.add_node("respond", self._respond_node)

        graph.set_entry_point("think")
        graph.add_conditional_edges("think", self._route)
        graph.add_edge("confirm", "execute")
        graph.add_edge("execute", "respond")
        graph.add_edge("respond", END)

        return graph.compile()

    def _think_node(self, state: AgentState):
        user_input = state["last_input"]

        # Check for auto-mode trigger
        auto_triggers = ["handle it yourself", "kar le", "you decide", "tu kar", "manage yourself"]
        if any(t in user_input.lower() for t in auto_triggers):
            self.auto_mode = True
            return {**state, "auto_mode": True, "response": "Auto-mode on. I'll handle tasks without asking.", "requires_confirmation": False}

        # Check for brain switch command
        if "switch brain" in user_input.lower() or "brain badlo" in user_input.lower():
            for name in AVAILABLE_BRAINS:
                if name in user_input.lower():
                    self.switch_brain(name)
                    return {**state, "response": f"Brain switched to {name}.", "requires_confirmation": False}

        # Check if tool action needed
        action = self.tools.detect_action(user_input)
        needs_confirm = action and not self.auto_mode and self.tools.is_sensitive(action)

        # Build context from memory
        memory_context = self.memory.get_relevant(user_input)

        # Build messages
        system = SYSTEM_PROMPT.format(
            brain=self.current_brain,
            auto_mode="ON — handling autonomously" if self.auto_mode else "OFF — will confirm before actions"
        )
        messages = [SystemMessage(content=system)]
        if memory_context:
            messages.append(SystemMessage(content=f"Relevant memory:\n{memory_context}"))
        for h in self.history[-6:]:
            messages.append(h)
        messages.append(HumanMessage(content=user_input))

        response = self.llm.invoke(messages)
        self.history.append(HumanMessage(content=user_input))
        self.history.append(AIMessage(content=response.content))
        self.memory.save(user_input, response.content)

        return {
            **state,
            "response": response.content,
            "requires_confirmation": needs_confirm,
            "pending_action": action,
            "auto_mode": self.auto_mode
        }

    def _route(self, state: AgentState):
        if state.get("requires_confirmation") and state.get("pending_action"):
            return "confirm"
        if state.get("pending_action") and (self.auto_mode or not self.tools.is_sensitive(state["pending_action"])):
            return "execute"
        return "respond"

    def _confirm_node(self, state: AgentState):
        action = state.get("pending_action", "")
        print(f"\n[JERRY] Confirmation needed: {action}")
        print("[JERRY] Shall I proceed? (yes/no/handle it yourself): ", end="")
        user_reply = input().strip().lower()

        auto_triggers = ["handle it yourself", "kar le", "yes always", "haan kar le"]
        if any(t in user_reply for t in auto_triggers):
            self.auto_mode = True
            print("[JERRY] Auto-mode activated. Won't ask again this session.")

        if user_reply in ["yes", "y", "haan", "ha"] or self.auto_mode:
            return state
        else:
            return {**state, "pending_action": None, "response": "Okay, skipped. Let me know if you want anything else."}

    def _execute_node(self, state: AgentState):
        action = state.get("pending_action")
        if action:
            result = self.tools.execute(action, state["last_input"])
            return {**state, "response": state["response"] + f"\n\n[Done]: {result}"}
        return state

    def _respond_node(self, state: AgentState):
        return state

    def chat(self, user_input: str, source="terminal") -> str:
        state = {
            "messages": [],
            "last_input": user_input,
            "response": "",
            "auto_mode": self.auto_mode,
            "requires_confirmation": False,
            "pending_action": None
        }
        result = self.graph.invoke(state)
        return result["response"]

    def switch_brain(self, brain_name: str):
        model = AVAILABLE_BRAINS.get(brain_name, brain_name)
        self.llm = ChatOllama(model=model)
        self.current_brain = brain_name
        print(f"[JERRY] Brain switched to: {brain_name} ({model})")

    def get_status(self):
        return {
            "brain": self.current_brain,
            "auto_mode": self.auto_mode,
            "memory_entries": self.memory.count()
        }
