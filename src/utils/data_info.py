import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 


def get_first_row(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the first row of the DataFrame as a new DataFrame.
    Equivalent to df.head(1).
    """
    return df.head(1)


def describe_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a describe DataFrame with only selected statistics
    and appends a final row showing the dtype of each column.
    """
    stats_df = df.describe().loc[["count", "mean", "std", "min", "max"]]
    dtypes = df.dtypes.apply(lambda x: str(x)).to_frame().T
    dtypes.index = ["dtype"]
    result = pd.concat([stats_df, dtypes], axis=0)

    return result


def get_shape_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the shape of the DataFrame as a one-row DataFrame
    with columns: 'rows' and 'columns'
    """
    shape_df = pd.DataFrame([{"rows": df.shape[0], "columns": df.shape[1]}])
    return shape_df



def get_missing_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame with the count and percentage of missing values per column,
    sorted by percentage descending.
    """
    total_missing = df.isnull().sum()
    percent_missing = (total_missing / len(df)) * 100

    missing_df = pd.DataFrame({
        "missing_count": total_missing,
        "missing_percent": percent_missing
    })

    missing_df = missing_df[missing_df["missing_count"] > 0]
    missing_df = missing_df.sort_values(by="missing_percent", ascending=False)

    return missing_df


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_missing_values(df):
    """
    Génère un graphique des valeurs manquantes avec style épuré
    """
    missing = df.isna().mean().sort_values(ascending=False) * 100
    missing = missing[missing > 0]
    
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')  
    ax.set_facecolor('none')  
    colors = sns.color_palette("Reds_r", len(missing))
    bars = ax.bar(missing.index, missing.values, color=colors)
    
    ax.set_title('Missing Values Distribution', fontsize=14, pad=20, color='black')
    ax.set_ylabel('Missing (%)', fontsize=12, color='black')
    ax.tick_params(colors='black')
    ax.grid(False)
    plt.xticks(rotation=45, ha='right')
    for spine in ax.spines.values():
        spine.set_edgecolor('none')
    
    plt.tight_layout()
    return fig


def summarize_dataset(df: pd.DataFrame) -> dict:
    """
    Returns a summary of the dataset as a dictionary (JSON-compatible):
    - shape (rows, columns)
    - column names
    - column types
    """
    summary = {
        "shape": {
            "rows": df.shape[0],
            "columns": df.shape[1]
        },
        "features": [
            {"name": col, "dtype": str(df[col].dtype)} for col in df.columns
        ]
    }
    return summary
