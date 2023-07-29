import openai
import streamlit as st
from LLM_functions import submitQuestion

# from LLM_functions import submitQuestion
response = []

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask me any questions related to clinical psychology, psychiatry, or mental health"}]

# if "dogs" not in st.session_state:
#     st.session_state["dogs"] = 'test'

if "history" not in st.session_state:
    st.session_state["history"] = []

if question := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    # st.session_state.messages.append({"role": "user", "content": question})
    # st.chat_message("user").write(question)
    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message
    # st.session_state.messages.append(msg)
    # st.chat_message("assistant").write(msg.content)

    response, history = submitQuestion(question, st.session_state['chatbot_api_key'], st.session_state['history'][-8::])
    # st.chat_message("user").write(question)
    # st.chat_message("assistant").write(response)
    st.session_state.messages.append({'role': 'user',
                                    'content': question})
    st.session_state.messages.append({'role': 'assistant',
                                    'content': response})
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
# st.session_state.messages
