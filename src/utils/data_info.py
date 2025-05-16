import pandas as pd
import matplotlib.pyplot as plt


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


def plot_missing_values(df: pd.DataFrame):
    """
    Plots a horizontal bar chart of missing value percentages per column.
    Only displays columns with missing values.
    Suitable for use with Streamlit (st.pyplot(fig)).
    """
    percent_missing = (df.isnull().sum() / len(df)) * 100
    percent_missing = percent_missing[percent_missing > 0].sort_values(ascending=True)

    if percent_missing.empty:
        return None  # Let Streamlit handle the fallback

    fig, ax = plt.subplots(figsize=(8, 6))
    percent_missing.plot(kind="barh", color="red", ax=ax)
    ax.set_xlabel("Percentage of missing values")
    ax.set_ylabel("Columns")
    ax.set_title("Missing Values per Column")
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
