import pandas as pd
from sklearn.impute import KNNImputer
import pyarrow as pa

def enforce_arrow_compatibility(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures the DataFrame can be serialized by PyArrow (used by Streamlit)."""
    for col in df.columns:
        try:
            _ = pa.array(df[col])
        except (pa.ArrowInvalid, pa.ArrowTypeError):
            df[col] = df[col].astype(str)
    return df


def data_cleaning_remove(df: pd.DataFrame) -> pd.DataFrame:
    original_shape = df.shape
    cleaned_df = df.dropna()
    cleaned_shape = cleaned_df.shape
    rows_removed = original_shape[0] - cleaned_shape[0]

    print(f"Original shape: {original_shape[0]} rows × {original_shape[1]} columns")
    print(f"After cleaning: {cleaned_shape[0]} rows × {cleaned_shape[1]} columns")
    print(f"Rows removed: {rows_removed}")

    return enforce_arrow_compatibility(cleaned_df)


def data_cleaning_fill(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = df.copy()
    total_missing_before = cleaned_df.isnull().sum().sum()
    original_shape = cleaned_df.shape

    for col in cleaned_df.columns:
        if cleaned_df[col].isnull().any():
            dtype = cleaned_df[col].dtype

            if pd.api.types.is_numeric_dtype(dtype):
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mean())

            elif pd.api.types.is_bool_dtype(dtype):
                cleaned_df[col] = cleaned_df[col].fillna(False)

            elif pd.api.types.is_datetime64_any_dtype(dtype):
                try:
                    fallback = cleaned_df[col].min()
                    if pd.isnull(fallback):
                        fallback = pd.Timestamp("2000-01-01")
                    cleaned_df[col] = cleaned_df[col].fillna(fallback)
                except Exception:
                    cleaned_df[col] = cleaned_df[col].fillna(pd.Timestamp("2000-01-01"))

            else:  # object or mixed
                cleaned_df[col] = cleaned_df[col].fillna("Unknown")

    total_missing_after = cleaned_df.isnull().sum().sum()
    filled_values = total_missing_before - total_missing_after

    print(f"Original shape: {original_shape[0]} rows × {original_shape[1]} columns")
    print(f"Missing values filled: {filled_values}")

    return enforce_arrow_compatibility(cleaned_df)


def data_cleaning_knn(df: pd.DataFrame, n_neighbors: int = 5) -> pd.DataFrame:
    cleaned_df = df.copy()
    original_shape = cleaned_df.shape
    total_missing_before = cleaned_df.isnull().sum().sum()

    # Fill non-numeric columns intelligently
    for col in cleaned_df.columns:
        if cleaned_df[col].isnull().any():
            dtype = cleaned_df[col].dtype

            if pd.api.types.is_bool_dtype(dtype):
                cleaned_df[col] = cleaned_df[col].fillna(False)

            elif pd.api.types.is_datetime64_any_dtype(dtype):
                fallback = cleaned_df[col].min()
                if pd.isnull(fallback):
                    fallback = pd.Timestamp("2000-01-01")
                cleaned_df[col] = cleaned_df[col].fillna(fallback)

            elif pd.api.types.is_object_dtype(dtype):
                cleaned_df[col] = cleaned_df[col].fillna("Unknown")

    # Apply KNN only to numeric cols
    num_cols = cleaned_df.select_dtypes(include=["number"]).columns
    if not num_cols.empty:
        imputer = KNNImputer(n_neighbors=n_neighbors)
        cleaned_df[num_cols] = imputer.fit_transform(cleaned_df[num_cols])

    total_missing_after = cleaned_df.isnull().sum().sum()
    filled_values = total_missing_before - total_missing_after

    print(f"Original shape: {original_shape[0]} rows × {original_shape[1]} columns")
    print(f"Missing values filled: {filled_values}")

    return enforce_arrow_compatibility(cleaned_df)
