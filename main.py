from urllib.parse import quote_plus
import streamlit as st
from langchain import SQLDatabase
@st.cache_resource
def get_db_engine(user_db_password,user_db_username,user_db_addr,user_db_base_db):
    encoded_password = quote_plus(f"{user_db_password}")
    url = f"mysql+pymysql://{user_db_username}:PASSWORD@{user_db_addr}:{user_db_port}/{user_db_base_db}"
    # 构建包含编码密码的连接 URL
    connection_url = url.replace("PASSWORD", encoded_password)
    try:
        db = SQLDatabase.from_uri(connection_url)
        st.success('连接成功!', icon="✅")
        return db
    except  Exception as e1:
        e = RuntimeError(f'连接失败')
        st.exception(e)
        st.exception(e1)
        return None


if 'DB_addr' not in st.session_state:
    st.session_state['DB_addr'] = ""
if 'DB_port' not in st.session_state:
    st.session_state['DB_port'] = ""
if 'DB_username' not in st.session_state:
    st.session_state['DB_username'] = ""
if 'DB_password' not in st.session_state:
    st.session_state['DB_password'] = ""
if 'DB_base_db' not in st.session_state:
    st.session_state['DB_base_db'] = ""
if 'db' not in st.session_state:
    st.session_state['db'] = None


with st.form(key="form"):
    st.write("第一步请先配置好所有信息")
    user_db_addr = st.text_input(
        "DB_addr", help="请输入数据库主机地址",value=st.session_state['DB_addr']
    )
    user_db_port=st.text_input(
        "DB_port", help="请输入数据库连接端口",value=st.session_state['DB_port']
    )
    user_db_base_db=st.text_input(
        "DB_base_db", help="请输入要连接的数据库名称",value=st.session_state['DB_base_db']
    )
    user_db_username = st.text_input(
        "DB_username", help="请输入数据库用户名",value=st.session_state['DB_username']
    )
    user_db_password = st.text_input(
        "DB_password", help="请输入数据库密码", type="password",value=st.session_state['DB_password']
    )
    col1, col2 = st.columns(2)
    with col2:
        check_db = st.form_submit_button("测试数据库连接")
if check_db:
    db=get_db_engine(user_db_password,user_db_username,user_db_addr,user_db_base_db)
    if db is not None:
        st.session_state['DB_addr']=user_db_addr
        st.session_state['DB_port'] = user_db_port
        st.session_state['DB_username'] = user_db_username
        st.session_state['DB_password'] = user_db_password
        st.session_state['DB_base_db'] = user_db_base_db
db=get_db_engine(user_db_password,user_db_username,user_db_addr,user_db_base_db)
if db is not None:
    st.session_state['db'] = db






