import streamlit as st
import uuid
from phi.storage.agent.sqlite import SqlAgentStorage
from agent_phidata import getAgentResponse

def main():
    st.set_page_config(page_title="Phidata Chat UI", layout="wide")
    st.title("Phidata Agent Chat")

    # Initialize messages in session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Get user input
    user_input = st.chat_input("Type your message...")
    if user_input:
        # Append user message
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        # Get agent response
        with st.spinner("Thinking..."):
            response = getAgentResponse(user_input)
        # Append assistant response
        st.session_state.messages.append({'role': 'assistant', 'content': response})

    # Display existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])

    
if __name__ == '__main__':
    main()