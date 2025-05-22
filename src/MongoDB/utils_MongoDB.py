from pymongo import MongoClient
from urllib.parse import quote_plus
from collections import defaultdict
import pandas as pd
from pandas import json_normalize
import streamlit as st
import re 


def connect_to_mongo(uri, db_name, collection_name):
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    try:
        client.admin.command("ping")  # Test de connexion
        db = client[db_name]
        collection = db[collection_name]
        sample = list(collection.find().limit(100))
        return sample  # ou metadata
    except Exception as e:
        raise ValueError(f"Échec de connexion : {e}")

def is_float_list(lst):
    if not isinstance(lst, list) or not lst:
        return False
    return all(isinstance(x, (float, int)) for x in lst)

def is_image_string(s):
    if not isinstance(s, str):
        return False
    return (
        bool(re.match(r"^data:image\/[a-zA-Z]+;base64,", s)) or
        bool(re.search(r"\.(jpg|jpeg|png|gif|bmp|webp)(\?.*)?$", s, re.IGNORECASE))
    )



from collections import defaultdict
import re

def analyze_structure(docs, parent_key=''):
    field_info = defaultdict(lambda: {
        'types': defaultdict(int),
        'null_count': 0,
        'sample_values': set(),
        'nested_fields': {},
        'is_embedding': False,
        'is_image': False,
        'is_graph_candidate': False
    })

    # Pour comptage progressif
    embedding_candidates = defaultdict(list)
    image_matches = defaultdict(int)
    graph_candidates = defaultdict(int)

    for doc in docs:
        for k, v in doc.items():
            full_path = f"{parent_key}.{k}" if parent_key else k

            if v is None:
                field_info[full_path]['null_count'] += 1
                continue

            # Type tracking
            if isinstance(v, list):
                field_info[full_path]['types']['array'] += 1

                # Candidat embedding : list of floats/ints
                if is_float_list(v):
                    embedding_candidates[full_path].append(len(v))

                # Candidat graph : via nom
                if k.lower() in {"edges", "nodes"}:
                    graph_candidates[full_path] += 1

                # Nested list of dicts
                if v and isinstance(v[0], dict):
                    field_info[full_path]['nested_fields'] = analyze_structure(v, full_path)

            elif isinstance(v, dict):
                field_info[full_path]['types']['object'] += 1

                # Candidat graph : via contenu (source/target)
                if "source" in v and "target" in v:
                    graph_candidates[full_path] += 1

                field_info[full_path]['nested_fields'] = analyze_structure([v], full_path)

            elif isinstance(v, str):
                field_info[full_path]['types']['str'] += 1

                if is_image_string(v):
                    image_matches[full_path] += 1

            else:
                field_info[full_path]['types'][type(v).__name__] += 1

            # Ajout échantillon
            if len(field_info[full_path]['sample_values']) < 5:
                field_info[full_path]['sample_values'].add(str(v)[:100])

    # Analyse post-parcours
    for field, lengths in embedding_candidates.items():
        if len(lengths) >= 5:
            mean_length = sum(lengths) / len(lengths)
            std_dev = (sum((l - mean_length) ** 2 for l in lengths) / len(lengths)) ** 0.5
            if mean_length >= 3 and std_dev < 2:
                field_info[field]['is_embedding'] = True

    for field, count in image_matches.items():
        if count >= 3:
            field_info[field]['is_image'] = True

    for field, count in graph_candidates.items():
        if count >= 3:
            field_info[field]['is_graph_candidate'] = True

    return field_info


def flatten_nested_objects(df, sep="_"):
    """Recursively flatten nested columns"""
    while True:
        # Find columns with dict values
        dict_cols = [col for col in df.columns 
                    if df[col].apply(lambda x: isinstance(x, dict)).any()]
        
        if not dict_cols:
            break
            
        for col in dict_cols:
            nested_df = json_normalize(df[col], sep=sep)
            nested_df.columns = [f"{col}{sep}{subcol}" for subcol in nested_df.columns]
            df = df.drop(col, axis=1).merge(nested_df, right_index=True, left_index=True)
    
    return df


import pandas as pd
from pandas import json_normalize

def convert_and_separate_dataframe(docs, config, structure):
    """
    Convertit les documents MongoDB en DataFrame tabulaire, 
    tout en extrayant les colonnes embedding, image et graph brutes dans des datasets dédiés.

    Retourne :
        df_tabular : DataFrame nettoyé tabulaire
        special_data : {
            'embedding': {col: DataFrame(id, column, value)},
            'image': {col: DataFrame(...)},
            'graph': {col: DataFrame(...)}
        }
    """

    special_data = {
        "embedding": {},
        "image": {},
        "graph": {}
    }

    # 1. Identification des colonnes spéciales à partir des flags de structure
    for field, info in structure.items():
        if info.get("is_embedding", False):
            special_data["embedding"][field] = None
        if info.get("is_image", False):
            special_data["image"][field] = None
        if info.get("is_graph_candidate", False):
            special_data["graph"][field] = None

    # 2. Suppression des colonnes spéciales dans les docs avant tabularisation
    columns_to_remove = (
        list(special_data["embedding"].keys()) + 
        list(special_data["image"].keys()) + 
        list(special_data["graph"].keys())
    )

    docs_cleaned = []
    for doc in docs:
        cleaned = {k: v for k, v in doc.items() if k not in columns_to_remove}
        docs_cleaned.append(cleaned)

    # 3. Conversion tabulaire classique
    df = json_normalize(
        docs_cleaned,
        sep=config['sep'],
        meta=config['meta_fields'],
        errors='ignore'
    )

    if config['flatten_nested']:
        df = flatten_nested_objects(df, config['sep'])

    # 4. Convert list columns to string for usability
    list_cols = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, list)).any()]
    for col in list_cols:
        df[col] = df[col].apply(lambda x: ", ".join(map(str, x)) if isinstance(x, list) else x)

    # 5. Construction des DataFrames spécialisés avec ID
    df_full = pd.json_normalize(docs, sep=config['sep'])  # version complète
    id_col = df_full["_id"].astype(str) if "_id" in df_full.columns else df_full.index.astype(str)

    for kind in ["embedding", "image", "graph"]:
        for col in special_data[kind]:
            if col in df_full.columns:
                special_data[kind][col] = pd.DataFrame({
                    "id": id_col,
                    "column": col,
                    "value": df_full[col]
                })

    return df, special_data


