import streamlit as st

def main():
    # Déclaration des pages du projet
    cover = st.Page("pages/cover.py", title="Cover")
    data_import = st.Page("pages/data_import.py", title="Import Data")
    select_db_and_collection = st.Page("pages/select_db_and_collection.py", title="Select Data Base & Collection")
    collection_info = st.Page("pages/collection_info.py",title="Collection informations and Intelligent extraction")
    data_info = st.Page("pages/data_info.py", title="Data Info")
    explore_special = st.Page("pages/explore_special.py", title ="Analyse of Graphs,Images and Embedding")
    main_page = st.Page("pages/main_page.py", title="Main Page")

    # Navigation entre les pages
    pg = st.navigation([
        cover,
        data_import,
        select_db_and_collection,
        collection_info,
        data_info,
        explore_special,
        main_page
    ])

    pg.run()

if __name__ == "__main__":
    main()
