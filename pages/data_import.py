import streamlit as st
import pandas as pd
import matplotlib
from src.utils.data_info import describe_dataset, get_shape_dataframe, plot_missing_values
from src.utils.cleaning_data import data_cleaning_fill, data_cleaning_remove

st.set_page_config(page_title="Import data", layout="centered")




# Session state setup
if "df_uploaded" not in st.session_state:
    st.session_state.df_uploaded = False
if "df" not in st.session_state:
    st.session_state.df = None

# Show uploader only if not already uploaded
if not st.session_state.df_uploaded:
    st.title("📂 Import your data")
    csv = st.file_uploader(label="Upload a CSV file", type="csv")

    if csv is not None:
        try:
            df = pd.read_csv(csv)
            st.session_state.df = df
            st.session_state.df_uploaded = True
            st.toast("✅ File uploaded and loaded successfully!")
            st.rerun()  # Hide uploader after successful upload
        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")

# After upload — use stored df
if st.session_state.df_uploaded and st.session_state.df is not None:
    st.title("Dataset summary")
    df = st.session_state.df

    st.header("🎲 Sample")
    st.dataframe(df.head(1))

    description = describe_dataset(df)
    shape = get_shape_dataframe(df)

    st.header("General Information")
    tab1, tab2, tab3 = st.tabs(["Description", "Shape", "Missing Values"])
    with tab1:
        st.header("📄 Dataset description")
        st.dataframe(description)
    with tab2:
        st.header("📐 Dataset shape")
        st.dataframe(shape)
    with tab3:
        st.header("🩹 Missing Values")
        st.pyplot(fig=plot_missing_values(df))

    clean_dataset = st.button("🧹 Clean dataset and start exploring 🚀")
    remove_toggle = st.toggle("Remove missing value")

    if clean_dataset:
        if remove_toggle:
            df = data_cleaning_remove(df)
        else:
            df = data_cleaning_fill(df)
        st.session_state.df = df  # Store cleaned df if needed later
        st.switch_page("pages/main_page.py")
