import os
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler

os.environ["GOOGLE_CSE_ID"] = ""
os.environ["GOOGLE_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""
os.environ['SERPER_API_KEY'] = ""
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
def get_chatgpt_chain(openai_api_key,openai_api_url,model_name,temperature,top_p):
    search = GoogleSerperAPIWrapper()
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to ask with search"
        )
    ]
    llm = OpenAI(top_p=top_p,temperature=temperature, openai_api_key=openai_api_key, streaming=True,openai_api_base=openai_api_url,model_name=model_name)
    self_ask_with_search = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return self_ask_with_search



with st.sidebar:
    openai_api_key=st.text_input(type="password",label="请输入openai api key",value="")
    openai_api_url=st.text_input(label="请输入openai api url",value="")
    model_name=st.text_input(label="请输入openai model name",value="")
    top_p = st.slider(label='top_p', min_value=0.0, max_value=1.0, value=0.1)
    temperature = st.slider(label='temperature', min_value=0.0, max_value=1.0, value=0.1)


self_ask_with_search=get_chatgpt_chain(openai_api_key,openai_api_url,model_name,temperature,top_p)
with st.form(key="form"):
    user_input = st.text_input("请输入问题")
    submit_clicked = st.form_submit_button("提交问题")
output_container = st.empty()
if submit_clicked:
    output_container = output_container.container()
    output_container.chat_message("user").write(user_input)
    answer_container = output_container.chat_message("assistant", avatar="😀")
    answer=self_ask_with_search(user_input,callbacks=[StreamlitCallbackHandler(answer_container)])
    st.write(answer)




