import streamlit as st 
import io 
import base64
from src.utils.analyse import analyse_plot

def display_graph(fig,role,id,code):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)

        # Encode to base64
        encoded = base64.b64encode(buf.read()).decode()

        html_code = f"""
        <div style="position: relative; width: 100%; max-width: 1200px; height: 600px; overflow: hidden;">
        <img src="data:image/png;base64,{encoded}" style="width: 100%; height: 100%; object-fit: contain; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);" />
        </div>
        """     
        # Display the plot 
        with st.chat_message(role):
            st.write("Here is the plot you request")
            
            # Col to center the plot
            _, col2, _ = st.columns([1, 3, 1])  # middle column is wide
            with col2:
                # Col for save, analyze and code button
                _,save_c, ana_c ,code_c,_ = st.columns([1.1,0.9,1.1,1.4,4.6],)

                # Save button
                with save_c:
                    # Save the plot to a buffer
                    
                    st.download_button(
                        label="💾 Save",
                        data=buf,
                        file_name="plot.png",
                        mime="image/png",
                        key=f"downlaod_button{id}")
                        
                # Analyze button
                with ana_c:
                    if st.button("🔎 Analyze",key=f"ana_button{id}"):
                        ana_result = analyse_plot(fig)
                        # Add new assistant message to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "plot": None,
                            "content": ana_result
                        })

                        st.rerun()
                                        
                
                # Display code button 
                with code_c:
                    with st.popover("⌨️ See code"):
                        st.code(code,language="python")
                
                # Display plot
                st.markdown(html_code, unsafe_allow_html=True)
                #st.pyplot(fig=fig)
                  