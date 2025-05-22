import streamlit as st
import pandas as pd
from src.MongoDB.utils_MongoDB import analyze_structure, flatten_nested_objects, convert_and_separate_dataframe

# ---------- Page Config ----------
st.set_page_config(page_title="Collection Conversion", layout="centered")

# ---------- Security Check ----------
if "mongo_raw_docs" not in st.session_state or not st.session_state.mongo_raw_docs:
    st.error("Please select a collection first from the MongoDB browser.")
    st.stop()

# ---------- Header ----------
st.markdown("""
    <style>
        .title {
            font-size: 2.4rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #00e676;
        }
        .sub {
            font-size: 1.1rem;
            margin-bottom: 2rem;
            color: #cccccc;
        }
        .data-preview {
            background-color: #111827;
            padding: 1rem;
            border-radius: 10px;
            color: #e5e7eb;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="title"> MongoDB to DataFrame Conversion</div>
<div class="sub">Database: {st.session_state.mongo_db_name} | Collection: {st.session_state.selected_collection}</div>
""", unsafe_allow_html=True)

# ---------- Sample Document Preview ----------
with st.expander("📄 View raw document sample", expanded=True):
    st.json(st.session_state.mongo_raw_docs[0])

# ---------- Structure Analysis ----------
with st.spinner("Analyzing collection structure..."):
    structure = analyze_structure(st.session_state.mongo_raw_docs)

st.subheader("🧮 Field Type Analysis")

analysis_data = []
for field, info in structure.items():
    null_pct = (info['null_count'] / len(st.session_state.mongo_raw_docs)) * 100
    sample_values = ', '.join(list(info['sample_values'])[:3]) + ("..." if len(info['sample_values']) > 3 else "")
    analysis_data.append({
        "Field": field,
        "Types": ', '.join(info['types'].keys()),
        "Null %": f"{null_pct:.1f}%",
        "Sample Values": sample_values
    })

st.dataframe(pd.DataFrame(analysis_data), use_container_width=True)

# ---------- Conversion Controls ----------
st.subheader("⚙️ Conversion Settings")

col1, col2 = st.columns(2)
with col1:
    config = {
        'sep': st.selectbox("Nested field separator", ["_", ".", "-"], index=0),
        'flatten_nested': st.checkbox("Flatten nested documents", True)
    }

with col2:
    max_docs = len(st.session_state.mongo_raw_docs)

    if max_docs > 3000:
        st.markdown(
            "<span style='color:orange; font-size:0.9rem;'>⚠️ Large preview sizes may slow down or crash the app depending on available memory.</span>",
            unsafe_allow_html=True
        )

    config.update({
        'sample_size': st.slider("Number of documents to convert", min_value=1, max_value=max_docs, value=min(1000, max_docs))
    })

# ---------- Conversion Execution ----------
if st.button("✨ Convert to DataFrame", type="primary"):
    with st.spinner(f"Converting {config['sample_size']} documents..."):
        try:
            config['meta_fields'] = [
                k for k in structure.keys()
                if not any(t in structure[k]['types'] for t in ['object', 'array'])
            ]

            df, special_data = convert_and_separate_dataframe(
                st.session_state.mongo_raw_docs[:config['sample_size']],
                config,
                structure
            )

            st.session_state.df = df
            st.session_state.special_data = special_data
            st.session_state.df_uploaded = True
            st.session_state.show_data_info = True

            st.success(f"✅ Converted to DataFrame: {df.shape[0]} rows, {df.shape[1]} columns")
            st.dataframe(df.head(20), use_container_width=True)

            # Message additionnel si types spéciaux détectés
            special_detected = {
                kind: list(special_data.get(kind, {}).keys())
                for kind in ["embedding", "image", "graph"]
                if special_data.get(kind)
            }

            if any(special_detected.values()):
                detected_list = [f"**{k}**: {', '.join(cols)}"
                                 for k, cols in special_detected.items() if cols]
                st.info(
                "🔍 Special data detected: " + " | ".join(detected_list) + 
                ". You will be able to explore them in the next section."
                )

        except Exception as e:
            st.error(f"Critical conversion error: {str(e)}")
            st.session_state.show_data_info = False


# ---------- Redirection Handling ----------
if st.session_state.get('show_data_info', False):
    st.markdown("---")
    if st.button("📊 Go to Data Analysis"):
        st.switch_page("pages/data_info.py")
