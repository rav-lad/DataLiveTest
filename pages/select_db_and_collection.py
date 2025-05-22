import streamlit as st
import pandas as pd
from src.MongoDB.utils_MongoDB import connect_to_mongo

st.set_page_config(page_title="Select DB & Collection", layout="centered")

# ---------- Connexion check ----------
if "mongo_client" not in st.session_state or "mongo_uri" not in st.session_state:
    st.error("You must connect to MongoDB first.")
    st.stop()

client = st.session_state.mongo_client

# ---------- UI ----------
st.title("Select MongoDB Database and Collection")
st.markdown("Choose a database and one of its collections to preview and analyze.")

# Select DB
try:
    db_names = client.list_database_names()
    selected_db = st.selectbox("Choose a database", db_names)
except Exception as e:
    st.error(f"Failed to retrieve databases: {e}")
    st.stop()

# Select collection
if selected_db:
    try:
        collection_names = client[selected_db].list_collection_names()
        selected_collection = st.selectbox("Choose a collection", collection_names)
    except Exception as e:
        st.error(f"Cannot retrieve collections: {e}")
        st.stop()

    # Preview
    if selected_collection and st.button("Preview Collection"):
        try:
            sample = connect_to_mongo(
                st.session_state.mongo_uri,
                selected_db,
                selected_collection
            )

            if sample:
                st.write("Here is a sample of the raw MongoDB documents:")
                for doc in sample[:1]:  # Affiche les 5 premiers documents
                    st.json(doc)

                # Stockage dans la session
                st.session_state.mongo_raw_docs = sample
                st.session_state.selected_collection = selected_collection
                st.session_state.mongo_db_name = selected_db
                st.session_state.df_uploaded = True

            else:
                st.warning("This collection is empty.")

        except Exception as e:
            st.error(f"Error loading collection: {e}")

    # Navigation vers la suite
    if st.session_state.get("df_uploaded", False):
        if st.button("Choose this collection and continue"):
            st.switch_page("pages/collection_info.py")
