import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_first_row(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the first row of the DataFrame as a new DataFrame."""
    if df.empty:
        return pd.DataFrame({"Message": ["Le DataFrame est vide."]})
    return df.head(1)


def describe_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a describe DataFrame with selected statistics
    and a final row showing the dtype of each column.
    """
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty or numeric_df.shape[1] == 0:
        return pd.DataFrame({"Message": ["Aucune colonne numérique à décrire."]})

    stats_df = numeric_df.describe().loc[["count", "mean", "std", "min", "max"]]
    dtypes = df.dtypes.apply(lambda x: str(x)).to_frame().T
    dtypes.index = ["dtype"]

    return pd.concat([stats_df, dtypes], axis=0)


def get_shape_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the shape of the DataFrame."""
    if df is None:
        return pd.DataFrame({"Message": ["Le DataFrame est None."]})
    return pd.DataFrame([{"rows": df.shape[0], "columns": df.shape[1]}])


def get_missing_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame of missing values (count and percent),
    sorted by percent descending.
    """
    if df.empty:
        return pd.DataFrame({"Message": ["Le DataFrame est vide."]})

    total_missing = df.isnull().sum()
    percent_missing = (total_missing / len(df)) * 100

    missing_df = pd.DataFrame({
        "missing_count": total_missing,
        "missing_percent": percent_missing
    })

    missing_df = missing_df[missing_df["missing_count"] > 0]

    if missing_df.empty:
        return pd.DataFrame({"Message": ["Aucune valeur manquante détectée."]})

    return missing_df.sort_values(by="missing_percent", ascending=False)


def plot_missing_values(df):
    """Affiche un graphique des valeurs manquantes."""
    if df.empty:
        return None

    missing = df.isna().mean().sort_values(ascending=False) * 100
    missing = missing[missing > 0]

    if missing.empty:
        return None

    fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')
    ax.set_facecolor('none')

    colors = sns.color_palette("Reds_r", len(missing))
    ax.bar(missing.index, missing.values, color=colors)

    ax.set_title('Missing Values Distribution', fontsize=14, pad=20, color='white')
    ax.set_ylabel('Missing (%)', fontsize=12, color='white')
    ax.tick_params(colors='white')
    ax.grid(False)
    plt.xticks(rotation=45, ha='right')

    for spine in ax.spines.values():
        spine.set_edgecolor('none')

    plt.tight_layout()
    return fig


def summarize_dataset(df: pd.DataFrame) -> str:
    """Retourne un résumé textuel du DataFrame."""
    if df.empty:
        return "Le DataFrame est vide.\n"

    shape_info = f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
    feature_info = "Columns:\n"
    for col in df.columns:
        dtype = str(df[col].dtype)
        feature_info += f"- {col}: {dtype}\n"

    return shape_info + feature_info
