import pandas as pd 
from sklearn.impute import KNNImputer

def data_cleaning_remove(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes all rows that contain at least one NaN or None value.
    Prints the shape before and after cleaning.

    Parameters:
        df (pd.DataFrame): The original dataset

    Returns:
        pd.DataFrame: A cleaned dataset
    """
    original_shape = df.shape
    cleaned_df = df.dropna()
    cleaned_shape = cleaned_df.shape
    rows_removed = original_shape[0] - cleaned_shape[0]

    print(f"Original shape: {original_shape[0]} rows × {original_shape[1]} columns")
    print(f"After cleaning: {cleaned_shape[0]} rows × {cleaned_shape[1]} columns")
    print(f"Rows removed: {rows_removed}")

    return cleaned_df


def data_cleaning_fill(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills missing values in the DataFrame:
    - Numerical columns: filled with the mean
    - Object (string) columns: filled with 'Unknown'
    Prints shape and number of filled values.

    Parameters:
        df (pd.DataFrame): The original dataset

    Returns:
        pd.DataFrame: A cleaned dataset with missing values filled
    """
    cleaned_df = df.copy()
    total_missing_before = cleaned_df.isnull().sum().sum()
    original_shape = cleaned_df.shape

    for col in cleaned_df.columns:
        if cleaned_df[col].isnull().any():
            if cleaned_df[col].dtype == "object":
                cleaned_df[col].fillna("Unknown", inplace=True)
            else:
                cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)

    total_missing_after = cleaned_df.isnull().sum().sum()
    filled_values = total_missing_before - total_missing_after

    print(f"Original shape: {original_shape[0]} rows × {original_shape[1]} columns")
    print(f"Missing values filled: {filled_values}")

    return cleaned_df


def data_cleaning_knn(df: pd.DataFrame, n_neighbors: int = 5) -> pd.DataFrame:
    """
    Fills missing values in the DataFrame:
    - Numerical columns: filled using KNN imputation
    - Object (string) columns: filled with 'Unknown'
    Prints shape and number of filled values.

    Parameters:
        df (pd.DataFrame): The original dataset
        n_neighbors (int): Number of neighbors for KNNImputer

    Returns:
        pd.DataFrame: A cleaned dataset with missing values filled
    """
    cleaned_df = df.copy()
    original_shape = cleaned_df.shape
    total_missing_before = cleaned_df.isnull().sum().sum()

    # 1. Handle categorical columns
    object_cols = cleaned_df.select_dtypes(include="object").columns
    for col in object_cols:
        if cleaned_df[col].isnull().any():
            cleaned_df[col].fillna("Unknown", inplace=True)

    # 2. Handle numerical columns with KNN
    num_cols = cleaned_df.select_dtypes(include=["number"]).columns
    if not num_cols.empty:
        imputer = KNNImputer(n_neighbors=n_neighbors)
        cleaned_df[num_cols] = imputer.fit_transform(cleaned_df[num_cols])

    total_missing_after = cleaned_df.isnull().sum().sum()
    filled_values = total_missing_before - total_missing_after

    print(f"Original shape: {original_shape[0]} rows × {original_shape[1]} columns")
    print(f"Missing values filled: {filled_values}")

    return cleaned_df
