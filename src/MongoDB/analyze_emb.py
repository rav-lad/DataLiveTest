import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def clean_embedding_column(df: pd.DataFrame, value_column: str = "value") -> pd.DataFrame:
    """
    Convertit les vecteurs sous forme de chaînes en listes de float.
    Supposé que df contient les colonnes 'id', 'column', 'value' (string).
    """
    def safe_parse_vector(v):
        try:
            return [float(x) for x in v.split(",")] if isinstance(v, str) else v
        except:
            return None

    df = df.copy()
    df[value_column] = df[value_column].apply(safe_parse_vector)
    df = df[df[value_column].apply(lambda x: isinstance(x, list) and all(isinstance(i, float) for i in x))]
    return df


import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def prepare_embedding_matrix(df: pd.DataFrame, value_column: str = "value") -> np.ndarray:
    return np.vstack(df[value_column].values)


def compute_pca(embedding_matrix: np.ndarray, n_components: int = 2) -> tuple[pd.DataFrame, list]:
    pca = PCA(n_components=n_components)
    reduced = pca.fit_transform(embedding_matrix)
    explained_var = pca.explained_variance_ratio_.cumsum().tolist()
    df = pd.DataFrame(reduced, columns=[f"PC{i+1}" for i in range(n_components)])
    return df, explained_var


def compute_tsne(embedding_matrix: np.ndarray, n_components: int = 2, perplexity: int = 30, random_state: int = 42) -> pd.DataFrame:
    tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=random_state)
    reduced = tsne.fit_transform(embedding_matrix)
    return pd.DataFrame(reduced, columns=[f"TSNE{i+1}" for i in range(n_components)])


def compute_embedding_stats(embedding_matrix: np.ndarray) -> dict:
    norms = np.linalg.norm(embedding_matrix, axis=1)
    return {
        "mean_norm": float(np.mean(norms)),
        "std_norm": float(np.std(norms)),
        "min_norm": float(np.min(norms)),
        "max_norm": float(np.max(norms)),
        "norms": norms.tolist()
    }


def find_similar_embeddings(embedding_matrix: np.ndarray, index: int, top_k: int = 5) -> tuple:
    similarities = cosine_similarity([embedding_matrix[index]], embedding_matrix)[0]
    similar_indices = np.argsort(similarities)[::-1][1:top_k+1]
    return similar_indices.tolist(), similarities[similar_indices].tolist()


def compute_kmeans_clusters(embedding_matrix: np.ndarray, n_clusters: int = 5, random_state: int = 42) -> np.ndarray:
    scaler = StandardScaler()
    scaled = scaler.fit_transform(embedding_matrix)
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = kmeans.fit_predict(scaled)
    return labels