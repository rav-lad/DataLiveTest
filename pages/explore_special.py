import streamlit as st
import pandas as pd
import plotly.express as px
from src.MongoDB.analyze_emb import (
    clean_embedding_column,
    prepare_embedding_matrix,
    compute_pca,
    compute_tsne,
    compute_kmeans_clusters,
    compute_embedding_stats,
    find_similar_embeddings
)
from src.MongoDB.analyze_img import (
    analyze_image_sizes,
    analyze_image_rgb,
    plot_image_size_histograms,
    plot_rgb_scatter,
    detect_grayscale_images
)
from src.MongoDB.analyze_graph import (
    extract_edge_list_from_dataframe,
    build_graph_from_edges,
    compute_graph_stats,
    compute_node_centrality,
    plot_graph_networkx
)

from bson import ObjectId

# ---------- Page Config ----------
st.set_page_config(page_title="Special Data Exploration", layout="wide")
st.title("Special Data Exploration")

# ---------- Load Data ----------
special_data = st.session_state.get("special_data", {})

if not special_data:
    st.error("No special data detected. Please return to the conversion step.")
    st.stop()

# ---------- Section: Embeddings ----------
if "embedding" in special_data and any(not df.empty for df in special_data["embedding"].values()):
    st.subheader("Embeddings Detected")

    for col_name, df_raw in special_data["embedding"].items():
        if not isinstance(df_raw, pd.DataFrame) or df_raw.empty:
            continue

        st.markdown(f"**Column**: `{col_name}` — {len(df_raw)} vectors detected")
        df_emb = clean_embedding_column(df_raw)
        if df_emb.empty:
            st.warning("No valid vectors after parsing.")
            continue

        st.dataframe(df_emb.head(3), use_container_width=True)
        matrix = prepare_embedding_matrix(df_emb)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button(f"PCA — {col_name}"):
                pca_df, explained = compute_pca(matrix)
                fig = px.scatter(pca_df, x="PC1", y="PC2", hover_name=df_emb["id"])
                st.plotly_chart(fig, use_container_width=True)
                st.caption(f"Cumulative variance (2D): {explained[1]*100:.2f}%")

        with col2:
            if st.button(f"t-SNE — {col_name}"):
                tsne_df = compute_tsne(matrix)
                fig = px.scatter(tsne_df, x="TSNE1", y="TSNE2", hover_name=df_emb["id"])
                st.plotly_chart(fig, use_container_width=True)

        with col3:
            if st.button(f"Cluster — {col_name}"):
                labels = compute_kmeans_clusters(matrix)
                pca_df, _ = compute_pca(matrix)
                pca_df["cluster"] = labels
                fig = px.scatter(pca_df, x="PC1", y="PC2", color=pca_df["cluster"].astype(str), hover_name=df_emb["id"])
                st.plotly_chart(fig, use_container_width=True)

        with col4:
            if st.button(f"Stats — {col_name}"):
                stats = compute_embedding_stats(matrix)
                st.metric("Mean norm", f"{stats['mean_norm']:.4f}")
                st.metric("Standard deviation", f"{stats['std_norm']:.4f}")
                st.metric("Min", f"{stats['min_norm']:.4f}")
                st.metric("Max", f"{stats['max_norm']:.4f}")
                st.bar_chart(stats["norms"])

        with col5:
            if st.button(f"Similar — {col_name}"):
                index = st.number_input(f"Base index for search ({col_name})", 0, len(matrix) - 1, 0)
                indices, scores = find_similar_embeddings(matrix, index)
                st.markdown(f"### Most similar to `{df_emb.iloc[index]['id']}`")

                for i, (idx, sim) in enumerate(zip(indices, scores)):
                    with st.expander(f"id: {df_emb.iloc[idx]['id']} — Similarity: {sim:.4f}", expanded=False):
                        obj_id = df_emb.iloc[idx]['id']
                        try:
                            doc = st.session_state.mongo_client[
                                st.session_state.mongo_db_name
                            ][st.session_state.selected_collection].find_one({"_id": ObjectId(obj_id)})
                            st.json(doc)
                        except Exception as e:
                            st.error(f"Failed to retrieve document: {e}")

        st.markdown("---")

# ---------- Section: Images ----------
if "image" in special_data and any(not df.empty for df in special_data["image"].values()):
    st.subheader("Images Detected")

    max_width = st.slider("Maximum image width (px)", 100, 512, 256)

    for col, df in special_data["image"].items():
        if isinstance(df, pd.DataFrame) and not df.empty:
            st.markdown(f"**Column**: `{col}` — {len(df)} images detected")
            df_sample = df.dropna().head(3)
            rows = [df_sample.iloc[i:i+3] for i in range(0, len(df_sample), 3)]

            for row_df in rows:
                cols = st.columns(len(row_df))
                for idx, (_, row) in enumerate(row_df.iterrows()):
                    with cols[idx]:
                        image_data = row["value"]
                        image_id = row["id"]

                        if isinstance(image_data, str) and (
                            image_data.startswith("data:image") or image_data.lower().endswith((".jpg", ".jpeg", ".png"))
                        ):
                            st.image(image_data, width=max_width)
                            with st.expander(f"id: {image_id}", expanded=False):
                                try:
                                    doc = st.session_state.mongo_client[
                                        st.session_state.mongo_db_name
                                    ][st.session_state.selected_collection].find_one({"_id": ObjectId(image_id)})
                                    st.json(doc)
                                except Exception as e:
                                    st.error(f"Failed to load document: {e}")
                        else:
                            st.code(str(image_data))

            # --- Image analysis ---
            st.markdown("### Image Analysis")

            df_sizes = analyze_image_sizes(df)
            df_rgb = analyze_image_rgb(df)
            figs_sizes = plot_image_size_histograms(df_sizes)
            fig_rgb = plot_rgb_scatter(df_rgb)
            df_gray = detect_grayscale_images(df_rgb)

            tab_dim, tab_rgb, tab_gray = st.tabs(["Dimensions", "RGB Means", "Grayscale Images"])

            with tab_dim:
                st.markdown("#### Size histograms")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.plotly_chart(figs_sizes[0], use_container_width=True)
                with col2:
                    st.plotly_chart(figs_sizes[1], use_container_width=True)
                with col3:
                    st.plotly_chart(figs_sizes[2], use_container_width=True)

            with tab_rgb:
                st.markdown("#### RGB scatter plot")
                st.plotly_chart(fig_rgb, use_container_width=True)

            with tab_gray:
                st.markdown("#### Potential grayscale images")
                if not df_gray.empty:
                    st.dataframe(df_gray[["id", "mean_R", "mean_G", "mean_B"]], use_container_width=True)
                    st.info(f"{len(df_gray)} image(s) detected as near grayscale (R ≈ G ≈ B)")
                else:
                    st.success("No grayscale images detected.")

            st.markdown("---")

# ---------- Section: Graphs ----------
if "graph" in special_data and any(not df.empty for df in special_data["graph"].values()):
    st.subheader("Graphs Detected")

    for col, df in special_data["graph"].items():
        if not isinstance(df, pd.DataFrame) or df.empty:
            continue

        st.markdown(f"**Column**: `{col}` — {len(df)} raw graphs detected")

        st.code(str(df["value"].iloc[0])[:300] + "...")

        edge_list = extract_edge_list_from_dataframe(df)
        if not edge_list:
            st.warning("No valid graph structure detected in documents.")
            continue

        G = build_graph_from_edges(edge_list)

        stats = compute_graph_stats(G)
        st.markdown("### Graph Statistics")
        for k, v in stats.items():
            st.markdown(f"- **{k.replace('_', ' ').capitalize()}**: {v}")

        st.markdown("### Node Centrality")
        centrality_df = compute_node_centrality(G)
        st.dataframe(centrality_df.head(10), use_container_width=True)

        st.markdown("### Interactive Visualization")
        layout = st.selectbox(f"Layout for `{col}`", ["spring", "kamada_kawai", "circular"], key=f"layout_{col}")
        fig = plot_graph_networkx(G, layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

# ---------- Navigation ----------
if st.button("Back to data analysis"):
    st.switch_page("pages/data_info.py")