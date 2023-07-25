import streamlit as st
from langchain import OpenAI
from langchain.callbacks import  StreamlitCallbackHandler
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
@st.cache_resource
def get_chatgpt_chain(openai_api_key,openai_api_url,model_name,temperature,top_p):
    llm = OpenAI(top_p=top_p,temperature=temperature, openai_api_key=openai_api_key, streaming=True,openai_api_base=openai_api_url,model_name=model_name)
    template = """Assistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    {history}
    Human: {human_input}
    Assistant:"""
    prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)
    chatgpt_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=10),
    )

    return chatgpt_chain





with st.sidebar:
    openai_api_key=st.text_input(type="password",label="请输入openai api key",value="")
    openai_api_url=st.text_input(label="请输入openai api url",value="")
    model_name=st.text_input(label="请输入openai model name",value="")
    top_p = st.slider(label='top_p', min_value=0.0, max_value=1.0, value=0.1)
    temperature = st.slider(label='temperature', min_value=0.0, max_value=1.0, value=0.1)

chatgpt_chain=get_chatgpt_chain(openai_api_key,openai_api_url,model_name,temperature,top_p)
with st.form(key="form"):
    user_input = st.text_input("请输入问题")
    submit_clicked = st.form_submit_button("提交问题")
output_container = st.empty()
if submit_clicked:
    output_container = output_container.container()
    output_container.chat_message("user").write(user_input)
    answer_container = output_container.chat_message("assistant", avatar="😀")
    answer=chatgpt_chain(user_input,callbacks=[StreamlitCallbackHandler(answer_container)])
    st.write(chatgpt_chain.llm)

    # answer_container.code(answer)

