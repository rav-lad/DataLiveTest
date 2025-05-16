import streamlit as st
from openai import OpenAI

openai_api_key = "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"
st.set_page_config(page_title="Main Page", layout="wide")
st.title("📊 Your Data Dashboard")

# Check if dataframe is available
if "df" in st.session_state and st.session_state.df is not None:
    
    # Fetch dataframe
    df = st.session_state.df

    # Preview of the clean dataframe
    st.subheader("🔍 Preview of your cleaned dataset")
    st.dataframe(df.head())
    
    # Container for the chatbot 
   
    chat_bot_container = st.container()
    chat_bot_container.header("💬 Chatbot")

    # System Content     
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
else:
    st.warning("⚠️ No dataset found. Please upload your data first.")
    if st.button("Go back to upload"):
        st.switch_page("pages/data_import.py")
