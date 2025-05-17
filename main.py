import streamlit as st

def main():
    # Déclaration des pages du projet
    cover = st.Page("pages/cover.py", title="Cover")
    data_import = st.Page("pages/data_import.py", title="Import Data")
    data_info = st.Page("pages/data_info.py", title="Data info")
    main_page = st.Page("pages/main_page.py", title="Main Page")

    # Navigation entre les pages
    pg = st.navigation([
        cover,
        data_import,
        data_info,
        main_page
    ])

    pg.run()

if __name__ == "__main__":
    main()
