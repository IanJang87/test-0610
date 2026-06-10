import streamlit as st

st.set_page_config(page_title="Hello", layout="wide")

st.title("Hello Streamlit! 👋")

st.write("Streamlit 앱에 오신 것을 환영합니다!")

with st.sidebar:
    st.header("설정")
    name = st.text_input("당신의 이름은?", "사용자")
    age = st.slider("나이", 0, 100, 25)

st.write(f"안녕하세요, **{name}**님! 나이가 {age}세군요.")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("메트릭 1", 100, 10)
with col2:
    st.metric("메트릭 2", 200, -5)
with col3:
    st.metric("메트릭 3", 300, 15)

st.divider()

st.subheader("샘플 코드")
code = """
def hello():
    print("Hello, Streamlit!")

hello()
"""
st.code(code, language="python")
