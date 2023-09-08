# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import openai
import streamlit as st

SYSTEM_MESSAGE = {
    "role": "system",
    "content": """
    *** You are GuideBot, an automated service to provide career guidance to \
    people, primarily students. Your job is to provide career guidance and \
    plan to reach their career goals based on the information provided. \
    *** You first greet the user and then ask for basic information to provide \
    appropriate guidance. You create a detailed guideline for users to follow \
    based on the information they provide. 
    *** You wait till all the information has been provided. \
    *** You are always very respectful, motivational, and friendly in your style of asking questions. \
    *** Always ask short questions in a conversational style to collect the basic information. \
    You focus on the following information to gain background of the user: \
    Educational background: level of their highest education, \
    Hobbies: what are their hobbies, \
    Skill level: what are they currently good at, \
    Primary interests: programming, graphics, marketing, SEO and other freelancing skills, \
    Experience: number of years of experience at their previous job, \
    Target: what goals exactly the user is trying to achieve.
    """
}

with st.sidebar:
    st.title('🤖💬 Shadhinlab Career GuideBot')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        messages_to_send = [SYSTEM_MESSAGE] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        for response in openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages_to_send, stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
