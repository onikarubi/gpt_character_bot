from app.apis.openai.gpt.conversion_bot import ConversationChatGUI


import streamlit as st
st.title("ChatGPT-like clone")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input('input prompt'):
    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})


    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ''
        chat = ConversationChatGUI(container=message_placeholder)

        for response in chat.run(prompt):
            full_response += response
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({'role': 'assistant', 'content': full_response})
