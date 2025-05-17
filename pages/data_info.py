import streamlit as st
from src.utils.data_info_function import (
    describe_dataset,
    get_shape_dataframe,
    plot_missing_values,
)
from src.utils.cleaning_data import (
    data_cleaning_fill,
    data_cleaning_remove,
    data_cleaning_knn,
)

# ---------- Page config ----------
st.set_page_config(page_title="Clean your data", layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

    /* Onglets stylisés */
    .stTabs [role="tablist"] {
        gap: .5rem;
        margin-bottom: 1.5rem;
        border-bottom: none !important;
    }
    [role="tab"] {
        background: transparent !important;
        border: 1px solid transparent !important;
        color: rgba(255,255,255,.8) !important;
        transition: all .3s ease !important;
        padding: .8rem 1.5rem !important;
    }
    [role="tab"]:hover {
        border-color: rgba(0,230,118,.3) !important;
        box-shadow: 0 0 12px rgba(0,230,118,.1) !important;
    }
    [role="tab"][aria-selected="true"] {
        color: #00e676 !important;
        border-bottom: 3px solid #00e676 !important;
        transform: translateY(-1px);
        background: transparent !important;
        box-shadow: none !important;
        outline: none !important;
    }
    div[data-baseweb="tab-highlight"] {
        display: none !important;
    }
    [role="tab"]:focus,
    [role="tab"]:focus-visible {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Glow commun pour big-title, subtitle, et h2 */
    .big-title,
    .subtitle,
    .stApp h2 {
        text-align: center;
        color: #ffffff !important;
        margin: 1rem 0;
        text-shadow:
            0 0 6px rgba(0,230,118,0.5),
            0 0 12px rgba(0,230,118,0.3),
            0 0 18px rgba(0,230,118,0.15);
    }

    .big-title {
        font-size: 4.5rem;
        font-weight: 700;
        letter-spacing: -1.5px;
        line-height: 1.1;
        transform: perspective(400px) rotateX(5deg);
    }

    .subtitle {
        font-size: 1.4rem;
        color: rgba(224,224,224,0.9) !important;
        margin: 1.5rem 0 3rem;
        letter-spacing: 0.5px;
    }

    /* Animation hover identique */
    .big-title:hover,
    .subtitle:hover,
    .stApp h2:hover {
        animation: text-glow 1.5s ease-in-out infinite alternate;
    }

    @keyframes text-glow {
        from {
            text-shadow:
                0 0 6px rgba(0,230,118,0.5),
                0 0 12px rgba(0,230,118,0.3),
                0 0 18px rgba(0,230,118,0.15);
        }
        to {
            text-shadow:
                0 0 12px rgba(0,230,118,0.6),
                0 0 18px rgba(0,230,118,0.4),
                0 0 24px rgba(0,230,118,0.2);
        }
    }

    /* Sous-header (h3) inchangé */
    .stApp h3 {
        color: #ffffff !important;
        text-shadow:
            0 0 2px #00e676,
            0 0 4px #00e676 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Vérification de la présence du dataset ----------
if "df" not in st.session_state or st.session_state.df is None:
    st.error("No dataset loaded. Please import your data first.")
    st.stop()

# ---------- Contenu principal ----------
df = st.session_state.df.copy()

# Titre principal
st.markdown('<div class="big-title">Dataset Preparation</div>', unsafe_allow_html=True)
# Sous-titre
st.markdown('<div class="subtitle">Prepare and clean your dataset seamlessly</div>', unsafe_allow_html=True)

# Section Sample
with st.container():
    st.header("Data Sample")
    st.dataframe(df.head(3))

# Section General Information
with st.container():
    st.header("General Information")
    tab1, tab2, tab3 = st.tabs(["Description", "Shape", "Missing Values"])
    with tab1:
        st.dataframe(describe_dataset(df))
    with tab2:
        st.dataframe(get_shape_dataframe(df))
    with tab3:
        st.pyplot(fig=plot_missing_values(df))

# Cleaning Options
with st.container():
    st.header("Data Cleaning")
    with st.container(border=True):
        method = st.radio(
            "Cleaning Method:",
            options=[
                "Remove rows with missing values",
                "Fill missing values",
                "KNN Imputation"
            ],
            index=1
        )
        if "KNN" in method:
            n_neighbors = st.slider(
                "Number of neighbors for KNN:",
                min_value=2,
                max_value=10,
                value=5,
                help="Number of nearest neighbors to use for imputation"
            )

# Action Button
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("Process Dataset", type="primary"):
        with st.status("Processing data...", expanded=True) as status:
            try:
                if "Remove" in method:
                    df = data_cleaning_remove(df)
                elif "Fill" in method:
                    df = data_cleaning_fill(df)
                elif "KNN" in method:
                    df = data_cleaning_knn(df, n_neighbors=n_neighbors)

                st.session_state.df = df
                status.update(label="Processing complete!", state="complete", expanded=False)
                st.switch_page("pages/main_page.py")
            except Exception as e:
                st.error(f"Processing failed: {str(e)}")
                st.stop()
