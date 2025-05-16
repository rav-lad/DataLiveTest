import streamlit as st
import pandas as pd
import matplotlib
from src.utils.data_info import describe_dataset, get_shape_dataframe, plot_missing_values
from src.utils.cleaning_data import data_cleaning_fill, data_cleaning_remove

st.set_page_config(page_title="Import data", layout="centered")

# ---------- STYLE CSS partagé ----------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

        body {
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #3a1c71);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            font-family: 'Space Grotesk', sans-serif;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stButton>button, .stDownloadButton>button {
            font-size: 1.1rem;
            padding: 0.8rem 2.5rem;
            border-radius: 10px;
            background: linear-gradient(135deg, #00e676 0%, #00bcd4 100%);
            color: black;
            border: none;
            box-shadow: 0 4px 20px rgba(0, 230, 118, 0.3);
            transition: all 0.4s ease;
        }

        .stButton>button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 30px rgba(0, 230, 118, 0.5);
        }

        h1, h2, h3 {
            color: white;
            text-shadow: 0 0 20px rgba(0, 230, 118, 0.3);
        }

        .stTabs [role="tablist"] > div {
            font-weight: bold;
        }

        .block-container {
            padding-top: 2rem;
        }

        .stToggleSwitch label {
            color: white;
        }
            
        .big-title {
            font-size: 3.2rem;
            font-weight: 700;
            text-align: center;
            color: rgba(255, 255, 255, 0.95);
            text-shadow: 0 0 25px rgba(0, 230, 118, 0.4);
            margin: 1rem 0;
            line-height: 1.1;
            letter-spacing: -1.5px;
            transform: perspective(400px) rotateX(5deg);
        }

        .big-title:hover {
            animation: text-glow 1.5s ease-in-out infinite alternate;
        }

        @keyframes text-glow {
            from { text-shadow: 0 0 10px rgba(0, 230, 118, 0.3); }
            to { text-shadow: 0 0 30px rgba(0, 230, 118, 0.7); }
        }

    </style>
""", unsafe_allow_html=True)

# ---------- Session state setup ----------
if "df_uploaded" not in st.session_state:
    st.session_state.df_uploaded = False
if "df" not in st.session_state:
    st.session_state.df = None

# ---------- Upload Section ----------
if not st.session_state.df_uploaded:
    st.markdown('<div class="big-title">Import your data</div>', unsafe_allow_html=True)
    csv = st.file_uploader(label="Upload a CSV file", type="csv")

    if csv is not None:
        try:
            df = pd.read_csv(csv)
            st.session_state.df = df
            st.session_state.df_uploaded = True
            st.toast("✅ File uploaded and loaded successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error reading CSV: {e}")

# ---------- After upload ----------
if st.session_state.df_uploaded and st.session_state.df is not None:
    st.title("🧾 Dataset Summary")
    df = st.session_state.df

    st.header("🎲 Sample")
    st.dataframe(df.head(1))

    description = describe_dataset(df)
    shape = get_shape_dataframe(df)

    st.header("📊 General Information")
    tab1, tab2, tab3 = st.tabs(["📄 Description", "📐 Shape", "🩹 Missing Values"])
    with tab1:
        st.dataframe(description)
    with tab2:
        st.dataframe(shape)
    with tab3:
        st.pyplot(fig=plot_missing_values(df))

# ---------- Cleaning controls ----------
st.markdown("### 🧼 Data Cleaning Options")

# Création d'un conteneur pour les options
with st.container(border=True):
    # Sélection de la méthode
    method = st.radio(
        "Choose cleaning strategy:",
        options=[
            "❌ Remove rows with missing values",
            "📊 Fill with mean/Unknown",
            "🤖 Advanced KNN Imputation"
        ],
        index=1
    )

    # Paramètres conditionnels pour KNN
    if "KNN" in method:
        n_neighbors = st.slider(
            "Number of neighbors for KNN:",
            min_value=2,
            max_value=10,
            value=5,
            help="Number of nearest neighbors to use for imputation"
        )

# Bouton de validation
clean_dataset = st.button("🚀 Clean dataset and start exploring", type="primary")

if clean_dataset:
    with st.status("Cleaning data...", expanded=True) as status:
        try:
            # Application de la méthode sélectionnée
            if "Remove" in method:
                df = data_cleaning_remove(df)
            elif "Fill" in method:
                df = data_cleaning_fill(df)
            elif "KNN" in method:
                df = data_cleaning_knn(df, n_neighbors=5)  

            st.session_state.df = df
            status.update(label="Cleaning complete!", state="complete", expanded=False)
            st.switch_page("pages/main_page.py")
            
        except Exception as e:
            st.error(f"Cleaning failed: {str(e)}")
            st.stop()
