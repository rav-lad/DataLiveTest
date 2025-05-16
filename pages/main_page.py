import streamlit as st
import matplotlib.pyplot as plt
import io
from openai import OpenAI
from src.openai_caller import get_python_code_from_gpt
from src.utils.data_info import summarize_dataset

openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)

st.set_page_config(page_title="Main Page", layout="wide")
st.title("📊 Your Data Dashboard")

# Check if dataframe is available
if "df" in st.session_state and st.session_state.df is not None:
    
    # Fetch dataframe
    df = st.session_state.df
    #metadata = summarize_dataset()
    
    # Preview of the clean dataframe
    st.subheader("🔍 Preview of your cleaned dataset")
    st.dataframe(df.head())
    
    # Container for the chatbot 
    chat_bot_container = st.container()
    chat_bot_container.header("💬 Chatbot")
    
    # Button that clear the chat and the history 
    if st.button("🗑️ Clear Chat", key="clear_chat_button"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        st.rerun()  # force refresh to remove old messages immediately
    
    # Initialize message history 
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # Display all message 
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # When user write store it inside prompt
    if prompt := st.chat_input():        

        # Add Prompt to message memory
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user prompt
        st.chat_message("user").write(prompt)
        
        # Get Plot
        msg = get_python_code_from_gpt(metadata="",user_request=prompt)
        
        # Add Result to session chat
        st.session_state.messages.append({"role": "assistant", "content": msg})
        
        # Display the plot 
        with st.chat_message("assistant"):
            st.write("Here is the plot you request")
            
            # Col to center the plot
            col1, col2, col3 = st.columns([1, 4, 1])  # middle column is wide
            with col2:
                # Generate fake plot for now
                fig, ax = plt.subplots(figsize=(5, 3))
                ax.plot([1, 2, 3], [4, 1, 7])
                ax.set_title("Example Line Plot")

                # Col for save, analyze and code button
                save_c, ana_c ,code_c = st.columns(3)

                # Save button
                with save_c:
                    # Save the plot to a buffer
                    buf = io.BytesIO()
                    fig.savefig(buf, format="png", bbox_inches="tight")
                    buf.seek(0)
                    st.download_button(
                        label="💾 Save",
                        data=buf,
                        file_name="plot.png",
                        mime="image/png",
                        key="download_button")
                        
                # Analyze button
                with ana_c:
                    if st.button("🔎 Analyze"):
                        st.info("Running analysis (simulate).")
                
                # Display code button 
                with code_c:
                    if st.button(" See code"):
                        st.info("See code")
                
                # Display plot
                st.pyplot(fig=fig)        
else:
    st.warning("⚠️ No dataset found. Please upload your data first.")
    if st.button("Go back to upload"):
        st.switch_page("pages/data_import.py")
