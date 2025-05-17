import streamlit as st
import matplotlib.pyplot as plt
import io
from openai import OpenAI
from src.openai_caller import run_code_with_df, get_python_code_from_gpt
from src.utils.data_info_function import summarize_dataset
from src.model.ui_utils import display_graph

openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)

st.set_page_config(page_title="Main Page", layout="wide")
st.title("📊 Your Data Dashboard")

# Check if dataframe is available
if "df" in st.session_state and st.session_state.df is not None:
    
    # Fetch dataframe
    df = st.session_state.df
    # Get Summary of dataset
    metadata = summarize_dataset(df=df)
    
    # Preview of the clean dataframe
    st.subheader("🔍 Preview of your cleaned dataset")
    st.dataframe(df.head())
    
    # Container for the chatbot 
    chat_bot_container = st.container()
    chat_bot_container.header("💬 Chatbot")
    
    # Button that clear the chat and the history 
    if st.button("🗑️ Clear Chat", key="clear_chat_button"):
        # Reset message
        st.session_state["messages"] = [{"role": "assistant","plot":None,"content": "How can I help you?"}]
        
        #  Reset context
        st.session_state["context"] = []
        st.rerun()  # force refresh to remove old messages immediately
    
    # Initialize message history 
    if "messages" not in st.session_state:
        # Save what to display
        st.session_state["messages"] = [{"role": "assistant","plot":None,"content": "How can I help you?"}]
        
        # Save context for LLM
        st.session_state["context"] = []

    # Display all message 
    for id,msg in enumerate(st.session_state.messages):
        if msg['plot'] is None:
            st.chat_message(msg["role"]).write(msg["content"])
        else:
            display_graph(msg['plot'],msg["role"],id,msg['content'])

    # When user write store it inside prompt
    if prompt := st.chat_input():        

        # Add Prompt to message memory
        st.session_state.messages.append({"role": "user","plot":None,"content": prompt})
        
        # Display user prompt
        st.chat_message("user").write(prompt)
        
        # Get Plot
        generated_code = get_python_code_from_gpt(metadata, user_request=prompt,context="")
        msg,fig = run_code_with_df(df=df,metadata=metadata,user_request=prompt)

        # Display the graph
        display_graph(fig,"assistant",len(st.session_state.messages),msg)

        # Add Result to session chat
        st.session_state.messages.append({"role": "assistant","plot":fig,"content": msg})
        
       
else:
    st.warning("⚠️ No dataset found. Please upload your data first.")
    if st.button("Go back to upload"):
        st.switch_page("pages/data_import.py")
