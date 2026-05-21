import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import ast
from src.config import (
    PREPROCESSED_TWEETS_REAL_FILE, PREPROCESSED_TWEETS_CENSORED_FILE,
    NETWORK_COMMUNITIES_REAL_FILE, NETWORK_COMMUNITIES_CENSORED_FILE,
    NETWORK_VISUALIZATION_PNG, NETWORK_VISUALIZATION_REAL_PNG, NETWORK_VISUALIZATION_CENSORED_PNG,
    VISUALIZATION_CONFIG, COLOR_PALETTE
)
from src.logging_utils import setup_logging
from src.graph_utils import build_mention_network

logger = setup_logging(__name__)

def visualize_dataset(edge_path, node_path, output_png_path, title) -> None:
    """
    Visualize the social network with communities highlighted and node sized by centrality.
    """
    try:
        logger.info(f"Visualizing network for: {node_path} -> {output_png_path}")
        
        # Load data
        if not edge_path.exists() or not node_path.exists():
            logger.error("Required data files not found")
            raise FileNotFoundError(
                f"Missing files: {edge_path} or {node_path}"
            )
        
        edge_df = pd.read_csv(edge_path)
        node_df = pd.read_csv(node_path)
        logger.info(f"Loaded {len(edge_df)} edges and {len(node_df)} nodes")

        # Build graph using centralized function
        G = build_mention_network(edge_df, logger)
        
        if G.number_of_nodes() == 0:
            logger.error("Network is empty!")
            raise ValueError("Network has no nodes")

        # Community and Centrality mapping
        community_map = node_df.set_index('node')['community'].to_dict()
        betweenness_map = node_df.set_index('node')['betweenness_centrality'].to_dict()
        
        # Ensure all nodes in graph have attributes
        missing_nodes = 0
        for node in G.nodes():
            if node not in community_map:
                logger.warning(f"Node '{node}' not in community map, assigning to community -1")
                community_map[node] = -1
                betweenness_map[node] = 0.001
                missing_nodes += 1
        
        if missing_nodes > 0:
            logger.warning(f"Fixed {missing_nodes} nodes missing from community data")

        # Create visualization
        plt.figure(figsize=VISUALIZATION_CONFIG["figure_size"])
        
        # Use spring layout for better node separation
        pos = nx.spring_layout(
            G, 
            k=VISUALIZATION_CONFIG["spring_layout_k"],
            seed=VISUALIZATION_CONFIG["spring_layout_seed"]
        )
        
        # Node sizes based on betweenness centrality
        node_sizes = [
            (betweenness_map.get(n, 0) * VISUALIZATION_CONFIG["node_size_scale"]) + 
            VISUALIZATION_CONFIG["node_size_min"] 
            for n in G.nodes()
        ]
        
        # Node colors based on community
        communities = [community_map.get(n, -1) for n in G.nodes()]
        
        # Draw nodes
        nx.draw_networkx_nodes(
            G, pos, 
            node_color=communities, 
            node_size=node_sizes,
            cmap=plt.cm.Set3, 
            alpha=0.9,
            edgecolors='white',
            linewidths=1
        )
        
        # Draw edges
        nx.draw_networkx_edges(
            G, pos, 
            alpha=VISUALIZATION_CONFIG["edge_opacity"], 
            width=1.0, 
            edge_color='silver'
        )
        
        # Labeling - only label top 15 nodes by centrality for clarity
        top_centrality = (
            node_df
            .sort_values('betweenness_centrality', ascending=False)
            .head(15)['node']
            .tolist()
        )
        labels = {n: f"@{n}" for n in G.nodes() if n in top_centrality}
        
        nx.draw_networkx_labels(
            G, pos, 
            labels, 
            font_size=9, 
            font_weight='bold', 
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1)
        )
        
        plt.title(
            title, 
            fontsize=18, 
            fontweight='bold'
        )
        plt.axis("off")
        
        # Add note about node size
        plt.text(
            0.95, 0.01, 
            "*Ukuran node menunjukkan Betweenness Centrality (kemampuan menjembatani informasi)", 
            horizontalalignment='right', 
            verticalalignment='bottom', 
            transform=plt.gca().transAxes,
            fontsize=10, 
            style='italic', 
            color='gray'
        )

        # Save figure
        output_png_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            output_png_path, 
            dpi=VISUALIZATION_CONFIG["dpi"], 
            bbox_inches='tight'
        )
        logger.info(f"Visualization saved to {output_png_path}")
        
        plt.close()
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        raise
    except ValueError as e:
        logger.error(f"Data error: {e}")
        raise
    except Exception as e:
        logger.exception(f"Visualization error: {e}")
        raise

if __name__ == "__main__":
    try:
        # 1. Visualize REAL dataset
        visualize_dataset(
            PREPROCESSED_TWEETS_REAL_FILE, 
            NETWORK_COMMUNITIES_REAL_FILE, 
            NETWORK_VISUALIZATION_REAL_PNG,
            "Visualisasi Jaringan & Deteksi Komunitas: Isu Pengadaan MBG (Data Asli)"
        )
        
        # 2. Visualize CENSORED dataset
        visualize_dataset(
            PREPROCESSED_TWEETS_CENSORED_FILE, 
            NETWORK_COMMUNITIES_CENSORED_FILE, 
            NETWORK_VISUALIZATION_CENSORED_PNG,
            "Visualisasi Jaringan & Deteksi Komunitas: Isu Pengadaan MBG (Data Sensor)"
        )
        
        # Sync with legacy/default path
        if NETWORK_VISUALIZATION_CENSORED_PNG.exists():
            import shutil
            shutil.copy(NETWORK_VISUALIZATION_CENSORED_PNG, NETWORK_VISUALIZATION_PNG)
            logger.info(f"Legacy visualization synced: copied {NETWORK_VISUALIZATION_CENSORED_PNG} to {NETWORK_VISUALIZATION_PNG}")
            
        logger.info("All visualizations completed successfully!")
    except Exception:
        logger.exception("Visualization failed")
        exit(1)
