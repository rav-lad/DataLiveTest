import pandas as pd
import numpy as np
from PIL import Image
import base64
import requests
import io
import plotly.express as px

def analyze_image_sizes(df: pd.DataFrame, value_column: str = "value") -> pd.DataFrame:
    data = []
    for i, row in df.iterrows():
        img_data = row[value_column]
        try:
            if isinstance(img_data, str) and img_data.startswith("data:image"):
                header, encoded = img_data.split(",", 1)
                image = Image.open(io.BytesIO(base64.b64decode(encoded)))
            elif isinstance(img_data, str) and img_data.startswith("http"):
                response = requests.get(img_data)
                image = Image.open(io.BytesIO(response.content))
            else:
                continue

            w, h = image.size
            data.append({"id": row["id"], "width": w, "height": h, "aspect_ratio": round(w / h, 2)})
        except Exception:
            continue
    return pd.DataFrame(data)


import numpy as np

def analyze_image_rgb(df: pd.DataFrame, value_column: str = "value") -> pd.DataFrame:
    data = []
    for i, row in df.iterrows():
        img_data = row[value_column]
        try:
            if isinstance(img_data, str) and img_data.startswith("data:image"):
                header, encoded = img_data.split(",", 1)
                image = Image.open(io.BytesIO(base64.b64decode(encoded)))
            elif isinstance(img_data, str) and img_data.startswith("http"):
                response = requests.get(img_data)
                image = Image.open(io.BytesIO(response.content))
            else:
                continue

            img = np.array(image.convert("RGB"))
            mean_rgb = img.mean(axis=(0, 1))  # Moyenne sur les deux dimensions spatiales
            data.append({
                "id": row["id"],
                "mean_R": float(mean_rgb[0]),
                "mean_G": float(mean_rgb[1]),
                "mean_B": float(mean_rgb[2])
            })
        except Exception:
            continue
    return pd.DataFrame(data)


def plot_image_size_histograms(df_sizes: pd.DataFrame):
    """
    Affiche des histogrammes pour largeur, hauteur et aspect_ratio
    """
    cols = ["width", "height", "aspect_ratio"]
    figs = []
    for col in cols:
        fig = px.histogram(df_sizes, x=col, nbins=30, title=f"Distribution de {col}")
        figs.append(fig)
    return figs


def plot_rgb_scatter(df_rgb: pd.DataFrame):
    """
    Scatter plot RGB avec couleur dynamique sur B
    """
    fig = px.scatter(
        df_rgb,
        x="mean_R",
        y="mean_G",
        size_max=8,
        color="mean_B",
        hover_name=df_rgb["id"],
        color_continuous_scale="Bluered",
        title="Distribution moyenne des canaux RGB"
    )
    return fig


def detect_grayscale_images(df_rgb: pd.DataFrame, threshold: float = 10.0) -> pd.DataFrame:
    """
    Retourne les images où R≈G≈B, indiquant du gris
    """
    rgb_diff = ((df_rgb["mean_R"] - df_rgb["mean_G"]).abs() +
                (df_rgb["mean_G"] - df_rgb["mean_B"]).abs() +
                (df_rgb["mean_R"] - df_rgb["mean_B"]).abs())
    return df_rgb[rgb_diff < threshold]