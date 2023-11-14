from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utillis import *
from langchain.llms import HuggingFaceHub
import os
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
# Replace 'your_token_value' with your actual Hugging Face API token
os.environ['HUGGINGFACEHUB_API_TOKEN'] = "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"
load_dotenv()
st.subheader("Chatbot with Langchain, ChatGPT, Pinecone, and Streamlit")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

openapi_key = os.getenv("OPENAPI_KEY")
llm = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()],model_name="gpt-3.5-turbo", openai_api_key=openapi_key)
if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)
system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully and as in detail/Briefly as possible using the provided context, 
and if the answer is not contained within the text below, say 'I don't know'""")



human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)



response_container = st.container()
# container for text box
textcontainer = st.container()

with textcontainer:
    query = st.text_input("Query: ", key="input")
    try:
        if query:
           with st.spinner("typing"):
                context=find_match(query)
                st.callback=StreamlitCallbackHandler(st.container())
                response=conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}",callbacks=[st.callback])
           st.session_state.requests.append(query)
           st.session_state.responses.append(response)
    except Exception as e:
        raise e


with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

with st.sidebar:
    st.subheader("Your documents")
    pdf_docs = st.file_uploader(
        "Upload your PDFs here and click on 'Process'")
    if st.button("Process"):
        with st.spinner("Processing"):
           bytes_data = pdf_docs.read()
           raw_text=get_pdf_with_images(bytes_data)
           chunks = split_docs(raw_text)
           pinecone_emb = pinecone_clinet(chunks)
           st.write("File has been uploaded,Wait for 3 min to reflect on Vector DB")




