import streamlit as st

st.set_page_config(page_title="DataLive.ia Get Started", layout="centered")

st.title("DataLive.ia 📊")
st.write("Make your data alive!")
st.write("Codeless tool for data analysis")
button = st.button("Get started")
if button:
    st.switch_page("pages/data_import.py")

