import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from typing import Union

def build_graph_from_edges(edge_list: list[dict]) -> nx.Graph:
    """Construit un graphe NetworkX à partir d'une liste d'arêtes avec 'source' et 'target'"""
    G = nx.Graph()
    for edge in edge_list:
        if 'source' in edge and 'target' in edge:
            G.add_edge(edge['source'], edge['target'], **{k: v for k, v in edge.items() if k not in ['source', 'target']})
    return G

def compute_graph_stats(G: nx.Graph) -> dict:
    """Retourne des statistiques de base sur un graphe NetworkX"""
    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": nx.density(G),
        "connected_components": nx.number_connected_components(G),
        "average_degree": sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0,
        "average_clustering": nx.average_clustering(G) if not G.is_directed() else None
    }

def compute_node_centrality(G: nx.Graph) -> pd.DataFrame:
    """Retourne la centralité (closeness et degree) de chaque noeud"""
    closeness = nx.closeness_centrality(G)
    degree = dict(G.degree())
    df = pd.DataFrame({
        "node": list(G.nodes()),
        "degree": [degree[n] for n in G.nodes()],
        "closeness": [closeness[n] for n in G.nodes()]
    })
    return df.sort_values(by="degree", ascending=False)

def plot_graph_networkx(G: nx.Graph, layout: str = "spring") -> go.Figure:
    """Génère un graphique interactif Plotly à partir d'un graphe NetworkX"""
    if layout == "spring":
        pos = nx.spring_layout(G, seed=42)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G)
    else:
        pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    labels = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        labels.append(str(node))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=labels,
        textposition="top center",
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            color=[G.degree(n) for n in G.nodes()],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Degré des noeuds',
                xanchor='left',
                titleside='right'
            )
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Visualisation du graphe',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))
    return fig

def extract_edge_list_from_dataframe(df: pd.DataFrame, col: str = "value") -> list[dict]:
    """Extrait la première liste d'arêtes valides depuis la colonne graph"""
    for i, row in df.iterrows():
        v = row[col]
        if isinstance(v, list) and all(isinstance(e, dict) and 'source' in e and 'target' in e for e in v):
            return v
    return []
