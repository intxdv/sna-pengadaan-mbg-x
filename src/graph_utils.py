"""
Graph building utilities to eliminate duplicate code.
Single source of truth for graph construction logic.
"""

import ast
import logging
from typing import Dict, Tuple, List
import pandas as pd
import networkx as nx
import numpy as np


def parse_mentions(mentions_value) -> List[str]:
    """
    Parse mentions column value (handles string or list format).
    
    Args:
        mentions_value: Raw value from DataFrame (could be string repr of list or actual list)
        
    Returns:
        List of mention strings, empty list if parsing fails
        
    Raises:
        ValueError: If parsing encounters critical error
    """
    if mentions_value is None:
        return []
    
    # Already a list
    if isinstance(mentions_value, list):
        return mentions_value
    
    # String representation of a list
    if isinstance(mentions_value, str):
        try:
            parsed = ast.literal_eval(mentions_value)
            if isinstance(parsed, list):
                return parsed
            else:
                raise ValueError(f"Expected list, got {type(parsed).__name__}")
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Failed to parse mentions string '{mentions_value}': {e}")
    
    return []


def build_mention_network(
    df: pd.DataFrame,
    logger: logging.Logger = None
) -> nx.Graph:
    """
    Build undirected weighted mention network from DataFrame.
    
    This is the SINGLE SOURCE OF TRUTH for graph construction.
    Used by: network_analysis.py, visualize.py, and notebook
    
    Args:
        df: DataFrame with columns ['user', 'mentions']
        logger: Optional logger for tracking
        
    Returns:
        NetworkX Graph with:
        - Nodes: User accounts
        - Edges: Mention relationships
        - Edge weights: Mention frequency (repeated mentions increase weight)
        
    Raises:
        ValueError: If DataFrame doesn't have required columns
    """
    if 'user' not in df.columns or 'mentions' not in df.columns:
        raise ValueError("DataFrame must have 'user' and 'mentions' columns")
    
    G = nx.Graph()
    parse_errors = 0
    edges_added = 0
    self_mentions_skipped = 0
    
    for row_num, (_, row) in enumerate(df.iterrows(), start=2):
        source = row['user']
        
        if pd.isna(source) or source == '':
            if logger:
                logger.warning(f"Row {row_num}: Empty source user")
            continue
        
        try:
            mentions = parse_mentions(row['mentions'])
        except ValueError as e:
            parse_errors += 1
            if logger and parse_errors <= 5:  # Log first 5 errors only
                logger.warning(f"Row {row_num}: {e}")
            continue
        
        # Build edges
        for target in mentions:
            if target == source:
                self_mentions_skipped += 1
                continue
            
            if pd.isna(target) or target == '':
                continue
            
            # Add or update edge with weight
            if G.has_edge(source, target):
                G[source][target]['weight'] += 1
            else:
                G.add_edge(source, target, weight=1)
                edges_added += 1
    
    # Log summary
    if logger:
        logger.info(f"Network built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        if parse_errors > 0:
            logger.warning(f"Parsing errors: {parse_errors} (First 5 logged above)")
        if self_mentions_skipped > 0:
            logger.debug(f"Self-mentions skipped: {self_mentions_skipped}")
    
    return G


def detect_communities_and_metrics(
    G: nx.Graph,
    seed: int = 42,
    logger: logging.Logger = None
) -> Tuple[Dict, float, Dict]:
    """
    Detect communities using Louvain algorithm and compute centrality metrics.
    
    Args:
        G: NetworkX Graph
        seed: Random seed for reproducibility
        logger: Optional logger
        
    Returns:
        Tuple of:
        - partition: Dict mapping node -> community_id
        - modularity: Float modularity score
        - metrics: Dict with 'betweenness_centrality' and 'degree_centrality'
        
    Raises:
        ValueError: If graph is empty or invalid
    """
    import community as community_louvain
    
    if G.number_of_nodes() == 0:
        raise ValueError("Cannot detect communities in empty graph")
    
    # Community detection
    partition = community_louvain.best_partition(G, weight='weight')
    modularity = community_louvain.modularity(partition, G)
    
    # Centrality metrics
    # Using weighted metrics since edges have weights
    betweenness_cent = nx.betweenness_centrality(G, weight='weight')
    degree_cent = nx.degree_centrality(G)
    closeness_cent = nx.closeness_centrality(G, distance='weight')
    
    metrics = {
        'betweenness_centrality': betweenness_cent,
        'degree_centrality': degree_cent,
        'closeness_centrality': closeness_cent,
    }
    
    if logger:
        num_communities = len(set(partition.values()))
        logger.info(f"Detected {num_communities} communities with modularity {modularity:.4f}")
    
    return partition, modularity, metrics


def calculate_mention_sentiment(
    df: pd.DataFrame,
    text_col: str = 'cleaned_text',
    logger: logging.Logger = None
) -> Dict[str, float]:
    """
    Calculate sentiment scores for mentions.
    
    Args:
        df: DataFrame with text column
        text_col: Name of text column to analyze
        logger: Optional logger
        
    Returns:
        Dict mapping row_index -> sentiment_score (-1.0 to 1.0)
    """
    try:
        from src.sentiment_analyzer import get_sentiment_analyzer
    except ImportError:
        if logger:
            logger.warning("sentiment_analyzer not available, returning neutral scores")
        return {i: 0.0 for i in range(len(df))}
    
    analyzer = get_sentiment_analyzer(logger=logger)
    sentiments = {}
    
    for idx, row in df.iterrows():
        text = row.get(text_col, "")
        
        if pd.isna(text) or text == "":
            sentiments[idx] = 0.0
            continue
        
        try:
            score = analyzer.analyze_sentiment(str(text))
            sentiments[idx] = score
        except Exception as e:
            if logger and idx < 5:  # Log first 5 errors only
                logger.debug(f"Row {idx}: Error analyzing sentiment: {e}")
            sentiments[idx] = 0.0
    
    if logger:
        logger.info(f"Sentiment analysis complete: {len(sentiments)} items processed")
    
    return sentiments
