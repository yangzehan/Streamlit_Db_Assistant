import streamlit as st
from langchain import OpenAI
from langchain.agents import create_sql_agent
from Streamlit_Db_Assistant.sql_agent.toolkit import SQLDatabaseToolkit
from langchain.callbacks import StreamlitCallbackHandler
from Streamlit_Db_Assistant.clear_results import with_clear_container
from Streamlit_Db_Assistant.sql_agent.sql_prompt import SQL_PREFIX,SQL_SUFFIX

with st.sidebar:
    openai_api_key=st.text_input(type="password",label="请输入openai api key",value="")
    openai_api_url=st.text_input(label="请输入openai api url",value="")
    model_name=st.text_input(label="请输入openai model name",value="")
    top_p = st.slider(label='top_p', min_value=0.0, max_value=1.0, value=0.1)
    temperature = st.slider(label='temperature', min_value=0.0, max_value=1.0, value=0.1)


llm = OpenAI(temperature=temperature,top_p=top_p, openai_api_key=openai_api_key, streaming=True,openai_api_base=openai_api_url,model_name=model_name)

db=st.session_state['db']
options = st.multiselect(
    '请选择需要查询的表',
    db.get_table_names(),
    [])
with st.expander("查看表结构"):
    st.write('你选择的表:', options)
    st.code(db.get_table_info_no_throw(options))
Toolkit=SQLDatabaseToolkit(db=db,llm=llm)
agent=create_sql_agent(llm=llm,verbose=True,toolkit=Toolkit,agent_executor_kwargs={"handle_parsing_errors":True},prefix=SQL_PREFIX,suffix=SQL_SUFFIX)
with st.form(key="form"):
    user_input = f"使用{str(options)}中的表回答问题。"
    user_input += st.text_input("请输入问题")
    submit_clicked = st.form_submit_button("提交问题")
output_container = st.empty()
if with_clear_container(submit_clicked):
    output_container = output_container.container()
    output_container.chat_message("user").write(user_input)
    answer_container = output_container.chat_message("assistant", avatar="🦜")
    st_callback = StreamlitCallbackHandler(answer_container)
    answer = agent.run(user_input, callbacks=[st_callback])
    answer_container.write(answer)







