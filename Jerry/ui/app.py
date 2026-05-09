import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.graph import JerryAgent, AVAILABLE_BRAINS
from voice.speaker import Speaker

st.set_page_config(
    page_title="Jerry — Personal AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.main { background-color: #0e1117; }
.stChatMessage { border-radius: 12px; margin: 4px 0; }
.status-box { background: #1e2130; padding: 12px; border-radius: 8px; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

if "agent" not in st.session_state:
    st.session_state.agent = JerryAgent()
if "speaker" not in st.session_state:
    st.session_state.speaker = Speaker()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_gender" not in st.session_state:
    st.session_state.voice_gender = "male"

agent = st.session_state.agent
speaker = st.session_state.speaker

with st.sidebar:
    st.title("Jerry Controls")

    st.markdown("### Status")
    status = agent.get_status()
    st.markdown(f"""
    <div class="status-box">
    Brain: <b>{status['brain']}</b><br>
    Auto-mode: <b>{'ON' if status['auto_mode'] else 'OFF'}</b><br>
    Memory: <b>{status['memory_entries']} entries</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Brain")
    brain_choice = st.selectbox(
        "Active Brain",
        options=list(AVAILABLE_BRAINS.keys()),
        index=list(AVAILABLE_BRAINS.keys()).index(agent.current_brain)
    )
    if brain_choice != agent.current_brain:
        agent.switch_brain(brain_choice)
        st.success(f"Switched to {brain_choice}")

    st.markdown("### Voice")
    gender = st.radio("Voice Gender", ["male", "female"], horizontal=True)
    if gender != st.session_state.voice_gender:
        speaker.switch_gender(gender)
        st.session_state.voice_gender = gender

    st.markdown("### Mode")
    auto = st.toggle("Auto-mode", value=agent.auto_mode)
    if auto != agent.auto_mode:
        agent.auto_mode = auto
        st.info(f"Auto-mode {'ON' if auto else 'OFF'}")

    if st.button("Clear History", type="secondary"):
        agent.history = []
        st.session_state.messages = []
        st.success("History cleared.")

    if st.button("Clear Memory", type="secondary"):
        agent.memory.clear()
        st.success("Memory cleared.")

st.title("Jerry — Personal AI Assistant")
st.caption("Local · Private · British English · Hindi + English")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Talk to Jerry..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Jerry is thinking..."):
            response = agent.chat(prompt, source="ui")
        st.markdown(response)
        speaker.speak(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
