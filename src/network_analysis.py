import pandas as pd
import networkx as nx
import community as community_louvain
import os
from src.config import (
    PREPROCESSED_TWEETS_REAL_FILE, 
    PREPROCESSED_TWEETS_CENSORED_FILE,
    NETWORK_COMMUNITIES_REAL_FILE, 
    NETWORK_COMMUNITIES_CENSORED_FILE,
    NETWORK_COMMUNITIES_FILE
)
from src.logging_utils import setup_logging, validate_dataframe_structure
from src.graph_utils import build_mention_network, detect_communities_and_metrics, calculate_mention_sentiment

logger = setup_logging(__name__)

def detect_communities(G):
    """
    Detect communities using the Louvain algorithm and calculate network metrics.
    """
    if G.number_of_nodes() == 0:
        logger.error("Cannot detect communities: graph is empty")
        return None, 0, None
        
    # Use centralized function
    partition, modularity, metrics = detect_communities_and_metrics(G, logger=logger)
    
    return partition, modularity, metrics

def analyze_dataset(preprocessed_path, output_path):
    """
    Build mention network, detect communities, calculate centrality and sentiment,
    and save results to output_path.
    """
    logger.info(f"Running network analysis on: {preprocessed_path}")
    
    if not preprocessed_path.exists():
        logger.error(f"Input file not found: {preprocessed_path}")
        raise FileNotFoundError(f"File {preprocessed_path} not found")
        
    df = pd.read_csv(preprocessed_path)
    logger.info(f"Loaded {len(df)} rows from {preprocessed_path}")
    
    # Validate data structure
    validate_dataframe_structure(df, ['user', 'mentions'], logger)
    
    # Build network using centralized function
    G = build_mention_network(df, logger)
    
    if G.number_of_nodes() == 0:
        logger.error("Network is empty! Check data quality.")
        raise ValueError("Network has no nodes")
        
    # Detect communities
    partition, mod, metrics = detect_communities(G)
    
    if partition is None:
        logger.error("Community detection failed")
        raise ValueError("Community detection returned None")
        
    # Calculate sentiment scores
    logger.info("Calculating sentiment scores...")
    sentiment_scores = calculate_mention_sentiment(df, text_col='cleaned_text', logger=logger)
    
    # Group sentiment by node (average sentiment of mentions from that node)
    node_sentiment = {}
    for node in G.nodes():
        node_mentions = df[df['user'] == node]
        if len(node_mentions) > 0:
            indices = node_mentions.index.tolist()
            sentiments = [sentiment_scores.get(idx, 0.0) for idx in indices]
            node_sentiment[node] = sum(sentiments) / len(sentiments)
        else:
            node_sentiment[node] = 0.0
            
    # Save results
    node_results = []
    for node in G.nodes():
        node_results.append({
            'node': node,
            'community': partition[node],
            'degree_centrality': metrics['degree_centrality'][node],
            'betweenness_centrality': metrics['betweenness_centrality'][node],
            'closeness_centrality': metrics['closeness_centrality'][node],
            'sentiment_score': node_sentiment[node],
        })
        
    node_df = pd.DataFrame(node_results)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    node_df.to_csv(output_path, index=False)
    logger.info(f"Community & Centrality data saved to {output_path}")

if __name__ == "__main__":
    try:
        logger.info("Starting network analysis pipeline...")
        
        # 1. Analyze REAL dataset
        analyze_dataset(PREPROCESSED_TWEETS_REAL_FILE, NETWORK_COMMUNITIES_REAL_FILE)
        
        # 2. Analyze CENSORED dataset
        analyze_dataset(PREPROCESSED_TWEETS_CENSORED_FILE, NETWORK_COMMUNITIES_CENSORED_FILE)
        
        # Sync with legacy/default path if different
        if NETWORK_COMMUNITIES_CENSORED_FILE.exists() and NETWORK_COMMUNITIES_CENSORED_FILE.resolve() != NETWORK_COMMUNITIES_FILE.resolve():
            import shutil
            shutil.copy(NETWORK_COMMUNITIES_CENSORED_FILE, NETWORK_COMMUNITIES_FILE)
            logger.info(f"Legacy file synced: copied {NETWORK_COMMUNITIES_CENSORED_FILE} to {NETWORK_COMMUNITIES_FILE}")
            
        logger.info("Network analysis pipeline completed successfully!")
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        exit(1)
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        exit(1)
