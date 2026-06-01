import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

## langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "QA Chatbot with Groq"

groq_api_key = os.getenv("GROQ_API_KEY")

## defining prompt

prompt = ChatPromptTemplate.from_messages(
    [
    ("system", "You are a helpful assistant please response to the user queries."),
    ("human", "Question :{question}")
    ]
)



## here temparature should be always between 0 to 1, if you set it to 0 then the model will always generate the same response for the same question, if you set it to 1 then the model will generate different responses for the same question. so you can set it according to your needs.  
def generate_response(question,api_key,llm,temparature,max_tokens):
    lm = ChatGroq(model = llm,groq_api_key=api_key)
    outputparser = StrOutputParser()
    chain = prompt|lm|outputparser
    response  = chain.invoke({"question": question})
    return response


## tittle of the app
st.title(" Welcome to the Groq Chatbot, How can I help you ?")
st.secrets["HF_TOKEN"]

st.sidebar.title("Settings")
## Dropdown to select various Model
llm = st.sidebar.selectbox("Select Model", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"])

## adjust temparature response
temparature = st.sidebar.slider("Select Temparature", 0.0, 1.0)
max_tokens = st.sidebar.slider("Select Max Tokens", min_value = 20, max_value = 300, value = 150)

## input box to ask question
st.write("Ask your question here :")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input,groq_api_key,llm,temparature,max_tokens)
    st.write(response)
else:
    st.write("Please enter a question to get the response.")
