import streamlit as st
import langchain
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationBufferMemory

from langchain import PromptTemplate

from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
persist_directory = 'ChromaDb'
if 'history' not in st.session_state:
    history = []
# history = []

system_message = """You are a helpful assistant that answers questions about mental health from the given context and the chat history."""

template = """/

###Instructions###
Below is a question by the user. Use the following context to answer the question to the best of your ability. If the answer is not in the context or the chat history, then respond with "I don't know."

The questions are never specific to a certain therapy session or use case. Even if the context seems to come from a specific case, answer the question as if responding in general. 

Use as much detail as possible from the context. 

Let's think through this step by step.

###Chat History###
{history}

###Question###
{question}

###Context###
{context1}
------
{context2}
------
{context3}
------
{context4}
------
{context5}

"""
memory = ConversationBufferMemory()

# history = []

prompt = PromptTemplate.from_template(template)
vectordb = Chroma(persist_directory= persist_directory, embedding_function=embedding)
filter = None

def submitQuestion(question, key, history):    
    #TO DO - Need to import vectordb
    docs_mmr = vectordb.max_marginal_relevance_search(query = question, fetch_k = 50, k = 5, filter = filter)

    context_dic = {}
    for idx, page in enumerate(docs_mmr):
        context_dic[f"context{idx+1}"] = (page.page_content)

    chat = ChatOpenAI(openai_api_key=key, temperature = 0, n =1, model= 'gpt-3.5-turbo-16k')
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message = HumanMessagePromptTemplate.from_template(template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message])

    chain = LLMChain(llm=chat, prompt=chat_prompt, verbose = False)
    response = chain.run(history = history, question = question, context1=context_dic['context1'], context2= context_dic['context2'], context3= context_dic['context3'], context4 = context_dic['context4'], context5= context_dic['context5'])

    memory.chat_memory.add_user_message(question)
    memory.chat_memory.add_ai_message(response)
    # history = []
    for msg in memory.chat_memory.messages[-8::]:
        history.append(f"[{msg.type}]:, {msg.content}\n")
    return response, history
# a,b = submitQuestion("What's anxiety?", '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', [])
# print(a)
# print(b)
