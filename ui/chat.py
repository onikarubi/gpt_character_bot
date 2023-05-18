import logging
import streamlit as st
from streamlit_chat import message
import time
import asyncio

def chat_template(callback_action):
    st.title('テストチャット')

    if 'user' not in st.session_state:
        st.session_state['user'] = []

    if 'assistant' not in st.session_state:
        st.session_state['assistant'] = []

    with st.form(key="chatbot", clear_on_submit=True):
        user_message = st.text_area(label='質問')
        submit = st.form_submit_button(label='送信する')

        if st.session_state.user:
            for i in range(len(st.session_state.user)):
                message(st.session_state.user[i],
                        is_user=True, key=str(i) + '_user')
                message(st.session_state.assistant[i], key=str(i) + '_assistant')

        if submit:
            st.session_state.user.append(user_message)
            assistant_message = callback_action(user_message)
            st.session_state.assistant.append(assistant_message)
