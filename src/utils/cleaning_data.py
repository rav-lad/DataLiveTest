import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from pandas.api.types import (
    is_bool_dtype,
    is_numeric_dtype,
    is_datetime64_any_dtype,
)

# 1. Détection des colonnes d'identifiants
def is_identifier(col_name):
    return col_name.lower().endswith("id") or col_name.lower() == "index"

def split_identifiers(df):
    id_cols = [col for col in df.columns if is_identifier(col)]
    return df.drop(columns=id_cols), df[id_cols]

def rejoin(df_core, df_ids):
    return pd.concat([df_ids.reset_index(drop=True), df_core.reset_index(drop=True)], axis=1)

# 2. Imputation simple
def handle_missing(col):
    if col.isna().sum() == 0:
        return col

    if is_bool_dtype(col):
        return col.fillna(col.mode().iloc[0]).astype(bool)

    if is_numeric_dtype(col):
        if pd.api.types.is_integer_dtype(col):
            return col.fillna(int(col.mean())).astype(col.dtype)
        return col.fillna(col.mean()).astype(col.dtype)

    if is_datetime64_any_dtype(col):
        return col.fillna(col.min() or pd.Timestamp("2000-01-01"))

    return col.fillna(col.mode().iloc[0] if not col.mode().empty else "Unknown")

# 3. Méthodes de cleaning
def data_cleaning_remove(df: pd.DataFrame) -> pd.DataFrame:
    df_core, df_ids = split_identifiers(df)
    cleaned = df_core.dropna()
    return rejoin(cleaned, df_ids.loc[cleaned.index])

def data_cleaning_fill(df: pd.DataFrame) -> pd.DataFrame:
    df_core, df_ids = split_identifiers(df)

    # Conversion explicite des colonnes object → numérique si possible
    for col in df_core.columns:
        # Si la colonne est de type object mais contient des chiffres, on la convertit
        if df_core[col].dtype == object:
            coerced = pd.to_numeric(df_core[col], errors='coerce')
            if coerced.notna().sum() > 0:
                df_core[col] = coerced

    # Ensuite on applique ton handle_missing sur chaque colonne
    filled = df_core.apply(handle_missing)
    return rejoin(filled, df_ids)


def data_cleaning_knn(df: pd.DataFrame, n_neighbors=5) -> pd.DataFrame:
    df_core, df_ids = split_identifiers(df)

    # 1. Non numériques
    non_num = df_core.select_dtypes(exclude=np.number).columns
    df_core[non_num] = df_core[non_num].apply(handle_missing)

    # 2. KNN sur numériques
    num = df_core.select_dtypes(include=np.number).columns
    if len(num):
        imputer = KNNImputer(n_neighbors=n_neighbors)
        df_core[num] = imputer.fit_transform(df_core[num])

        for col in num:
            if pd.api.types.is_integer_dtype(df[col]):
                df_core[col] = df_core[col].round().astype(df[col].dtype)

    return rejoin(df_core, df_ids)
