import streamlit as st
import pandas as pd 
import matplotlib as pd

def main():
    main_page = st.Page("pages/main_page.py",title="Main page")
    cover = st.Page("pages/cover.py",title="Cover",icon="")
    data_import = st.Page("pages/data_import.py",title="Import Data",icon="")

    pg = st.navigation([cover,data_import,main_page])

    pg.run()
    




if __name__ == "__main__":
    main()
