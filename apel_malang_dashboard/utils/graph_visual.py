import networkx as nx
import plotly.graph_objects as go
import pandas as pd

def plot_gnn_graph():
    """Visualisasi interaktif Graph Neural Network faktor."""
    G = nx.Graph()
    
    nodes = [
        ('Hasil Panen', 'Output', '#00ffcc'),
        ('Kualitas Fisik', 'Kualitas', '#ff3366'),
        ('Persepsi Konsumen', 'Pasar', '#ffcc00'),
        ('Cuaca', 'Numerik', '#0099ff'),
        ('Pupuk', 'Numerik', '#cc66ff'),
        ('Penyakit', 'Kualitas', '#ff3333'),
        ('Harga', 'Output', '#00ffcc')
    ]
    
    for node, group, color in nodes:
        G.add_node(node, group=group, color=color)
        
    edges = [
        ('Cuaca', 'Hasil Panen', 0.8),
        ('Pupuk', 'Hasil Panen', 0.6),
        ('Penyakit', 'Kualitas Fisik', 0.9),
        ('Cuaca', 'Penyakit', 0.5),
        ('Hasil Panen', 'Harga', 0.7),
        ('Kualitas Fisik', 'Harga', 0.85),
        ('Persepsi Konsumen', 'Harga', 0.75),
        ('Kualitas Fisik', 'Persepsi Konsumen', 0.65)
    ]
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
        
    pos = nx.spring_layout(G, seed=42)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='rgba(0, 0, 0, 0.3)'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"<b>{node}</b><br>{G.nodes[node]['group']}")
        node_color.append(G.nodes[node]['color'])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=list(G.nodes()),
        textposition="top center",
        textfont=dict(color="#1f2937", size=12),
        marker=dict(
            showscale=False,
            color=node_color,
            size=35,
            line_width=3,
            line_color='#1f2937',
            symbol='circle-dot'
        ))

    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<b>Integrasi Multi-Faktor (GNN)</b><br><sup><i>Interdependensi Data Agraria & Ekonomi Kaggle</i></sup>',
                title_font_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=60),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                template='plotly_white',
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff'
                ))
    return fig

def plot_gnn_centrality(centrality_dict):
    """Plot bar chart untuk nilai Eigenvector Centrality dari node di GNN."""
    nodes = list(centrality_dict.keys())
    values = list(centrality_dict.values())
    
    fig = go.Figure(go.Bar(
        x=values, y=nodes, orientation='h',
        marker=dict(
            color=values,
            colorscale='Magenta',
            line=dict(color='#1f2937', width=1)
        ),
        text=[f"{v:.2f}" for v in values],
        textposition='auto'
    ))
    fig.update_layout(
        title='<b>Analisis Sentralitas Node (Eigenvector)</b><br><sup><i>Pengaruh Fitur terhadap Output Global</i></sup>',
        xaxis_title='Nilai Sentralitas (Kepentingan Node)',
        yaxis_title='Node Graf',
        yaxis={'categoryorder':'total ascending'},
        template='plotly_white',
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff'
    )
    return fig

def plot_gnn_edge_weights():
    """Plot heatmap bobot hubungan/edges di dalam GNN."""
    edges = [
        {'Source': 'Cuaca', 'Target': 'Hasil Panen', 'Bobot': 0.8},
        {'Source': 'Pupuk', 'Target': 'Hasil Panen', 'Bobot': 0.6},
        {'Source': 'Penyakit', 'Target': 'Kualitas Fisik', 'Bobot': 0.9},
        {'Source': 'Cuaca', 'Target': 'Penyakit', 'Bobot': 0.5},
        {'Source': 'Hasil Panen', 'Target': 'Harga', 'Bobot': 0.7},
        {'Source': 'Kualitas Fisik', 'Target': 'Harga', 'Bobot': 0.85},
        {'Source': 'Persepsi Konsumen', 'Target': 'Harga', 'Bobot': 0.75},
        {'Source': 'Kualitas Fisik', 'Target': 'Persepsi Konsumen', 'Bobot': 0.65}
    ]
    df = pd.DataFrame(edges)
    matrix = df.pivot(index='Source', columns='Target', values='Bobot').fillna(0)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix.values,
        x=matrix.columns,
        y=matrix.index,
        colorscale='Hot',
        text=matrix.values,
        texttemplate="%{text:.2f}",
    ))
    fig.update_layout(
        title='<b>Heatmap Bobot Edge Probabilistik (GNN)</b><br><sup><i>Korelasi Sebab-Akibat antar Node Makro</i></sup>',
        template='plotly_white',
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff'
    )
    return fig

