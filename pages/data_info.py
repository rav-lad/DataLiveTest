import streamlit as st
from src.utils.data_info import describe_dataset, get_shape_dataframe, plot_missing_values
from src.utils.cleaning_data import data_cleaning_fill, data_cleaning_remove, data_cleaning_knn

# ---------- Page config ----------
st.set_page_config(page_title="Clean your data", layout="centered")

# ---------- CSS ----------
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
        .stButton>button {
            font-size: 1.1rem;
            padding: 0.8rem 2.5rem;
            border-radius: 10px;
            background: linear-gradient(135deg, #00e676 0%, #00bcd4 100%);
            color: black;
            border: none;
            transition: all 0.4s ease;
        }
        h1, h2, h3 {
            color: white;
            text-shadow: 0 0 20px rgba(0, 230, 118, 0.3);
        }
        .stTabs [role="tablist"] > div {
            font-weight: bold;
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
            margin: 2rem 0;
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

# ---------- Vérification de la présence du dataset ----------
if "df" not in st.session_state or st.session_state.df is None:
    st.error("❌ No dataset loaded. Please import your data first.")
    st.stop()

# ---------- Contenu ----------
df = st.session_state.df

st.markdown('<div class="big-title">Clean your dataset</div>', unsafe_allow_html=True)

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

# ---------- Cleaning options ----------
st.markdown("### 🧼 Data Cleaning Options")

with st.container(border=True):
    method = st.radio(
        "Choose cleaning strategy:",
        options=[
            "❌ Remove rows with missing values",
            "📊 Fill with mean/Unknown",
            "🤖 Advanced KNN Imputation"
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

# ---------- Action button ----------
if st.button("🚀 Clean dataset and start exploring", type="primary"):
    with st.status("Cleaning data...", expanded=True) as status:
        try:
            if "Remove" in method:
                df = data_cleaning_remove(df)
            elif "Fill" in method:
                df = data_cleaning_fill(df)
            elif "KNN" in method:
                df = data_cleaning_knn(df, n_neighbors=n_neighbors)

            st.session_state.df = df
            status.update(label="✅ Cleaning complete!", state="complete", expanded=False)
            st.switch_page("pages/main_page.py")

        except Exception as e:
            st.error(f"❌ Cleaning failed: {str(e)}")
            st.stop()
