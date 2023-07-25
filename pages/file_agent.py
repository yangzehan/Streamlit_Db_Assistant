import streamlit as st
import os
from langchain import OpenAI, FAISS
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
# 获取当前目录路径
current_file = __file__
current_dir = os.path.dirname(current_file)
os.environ["OPENAI_API_BASE"]=""
os.environ["OPENAI_API_KEY"]=""





@st.cache_resource
def get_file_agent(openai_api_key,openai_api_url,top_p,temperature,model_name,file_value):
    # 获取文件的临时路径
    temp_file_path = f"{current_dir}/tmp/temp.pdf"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_value)
        temp_file.close()
    loader = PyMuPDFLoader(f"{current_dir}/tmp/temp.pdf")
    dos = loader.load_and_split()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(dos)
    embeddings = OpenAIEmbeddings()
    # vectorstore = Chroma.from_documents(documents, embeddings)
    db = FAISS.from_documents(documents, embeddings)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(verbose=True,llm=OpenAI(streaming=True,model_name=model_name,openai_api_key=openai_api_key,openai_api_base=openai_api_url,top_p=top_p,temperature=temperature),retriever= db.as_retriever(), memory=memory)
    return qa
with st.sidebar:
    openai_api_key=st.text_input(type="password",label="请输入openai api key",value="")
    openai_api_url=st.text_input(label="请输入openai api url",value="")
    model_name=st.text_input(label="请输入openai model name",value="gpt-3.5-turbo-16k")
    top_p = st.slider(label='top_p', min_value=0.0, max_value=1.0, value=0.1)
    temperature = st.slider(label='temperature', min_value=0.0, max_value=1.0, value=0.1)
# 获取上传的文件
uploaded_file = st.file_uploader("上传文件", type=["pdf"])
if uploaded_file is not None:
    qa=get_file_agent(openai_api_key,openai_api_url,top_p,temperature,model_name,uploaded_file.getvalue())
    with st.form(key="form"):
        user_input = st.text_input("请输入问题")
        submit_clicked = st.form_submit_button("提交问题")
    output_container = st.empty()
    if submit_clicked:
        output_container = output_container.container()
        output_container.chat_message("user").write(user_input)
        answer_container = output_container.chat_message("assistant", avatar="😀")
        answer=qa(user_input,callbacks=[StreamlitCallbackHandler(answer_container)])
        st.write(answer)













