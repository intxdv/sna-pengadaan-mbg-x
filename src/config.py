"""
Configuration and path management for SNA project.
Centralizes all configuration to prevent inconsistencies.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
LOGS_DIR = PROJECT_ROOT / "logs"

# Data files
RAW_TWEETS_FILE = DATA_DIR / "raw_tweets.csv"  # Legacy/default raw tweets path
RAW_TWEETS_REAL_FILE = DATA_DIR / "raw_tweets_real.csv"
RAW_TWEETS_CENSORED_FILE = DATA_DIR / "raw_tweets_censored.csv"

# Preprocessed files
PREPROCESSED_TWEETS_REAL_FILE = DATA_DIR / "preprocessed_tweets_real.csv"
PREPROCESSED_TWEETS_CENSORED_FILE = DATA_DIR / "preprocessed_tweets_censored.csv"
PREPROCESSED_TWEETS_FILE = PREPROCESSED_TWEETS_CENSORED_FILE  # Default to censored

# Network communities analysis results
NETWORK_COMMUNITIES_REAL_FILE = DATA_DIR / "network_communities_real.csv"
NETWORK_COMMUNITIES_CENSORED_FILE = DATA_DIR / "network_communities_censored.csv"
NETWORK_COMMUNITIES_FILE = NETWORK_COMMUNITIES_CENSORED_FILE  # Default to censored

# Report files
NETWORK_VISUALIZATION_PNG = REPORTS_DIR / "community_visualization.png"  # Default/legacy path
NETWORK_VISUALIZATION_REAL_PNG = REPORTS_DIR / "community_visualization_real.png"
NETWORK_VISUALIZATION_CENSORED_PNG = REPORTS_DIR / "community_visualization_censored.png"
NETWORK_INTERACTIVE_HTML = NOTEBOOKS_DIR / "network_interactive.html"

# Whitelist of official/public accounts that should not be anonymized (case-insensitive)
OFFICIAL_ACCOUNTS = {
    # Government
    "jokowi", "prabowo", "gibran_tweet", "kemensetneg", "kemenkeuri", "kemenkesri", "kemendikbud_ri", "airlangga_hrt", "moeldoko", "sandiuno",
    # Media
    "detikcom", "tempodotco", "kompascom", "antaranews", "vivacoid", "cnnindonesia", "kumparan", "bbcindonesia", "metro_tv", "tvonenews",
    # Critics / NGOs
    "lembaga_keadilan", "aliansi_rakyat", "pengamat_sosial", "tokoh_oposisi", "aktivis_lingkungan", "yayasan_gizi", "indowitch", "icw", "kontras", "lbh_jakarta",
    # Business / Vendor
    "asosiasi_vendor", "pt_pangan_makmur", "koprasi_susu", "direktur_logistik", "pengusaha_lokal", "umkm_juara", "kadin_indonesia", "hipmi_official"
}


# Network parameters
NETWORK_CONFIG = {
    "directed": False,
    "weighted": True,
    "weight_field": "weight",
}

# Visualization parameters
VISUALIZATION_CONFIG = {
    "figure_size": (15, 12),
    "dpi": 300,
    "spring_layout_k": 0.6,
    "spring_layout_seed": 42,
    "plotly_spring_k": 0.15,
    "node_size_scale": 15000,
    "node_size_min": 200,
    "edge_opacity": 0.03,
    "edge_color": "rgba(255,255,255,0.03)",
    "background_color": "#1a1a1a",
    "font_color": "#ffffff",
}

# Color palette (accessible and consistent)
COLOR_PALETTE = {
    "community_0": "#FF6B6B",      # Coral Red
    "community_1": "#4ECDC4",      # Turquoise
    "community_2": "#45B7D1",      # Sky Blue
    "community_3": "#FBD38D",      # Orange
    "community_4": "#D6BCFA",      # Lavender
}

# Community detection parameters
LOUVAIN_CONFIG = {
    "seed": 42,
    "weight": "weight",
}

# Centrality analysis thresholds
CENTRALITY_CONFIG = {
    "percentile_threshold": 75,     # Top 25% for influential actors
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S",
}

# Create directories if they don't exist
for directory in [DATA_DIR, REPORTS_DIR, NOTEBOOKS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def get_data_file(filename: str) -> Path:
    """Get full path to data file with validation."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    return filepath


def get_output_file(filename: str, output_dir: str = "data") -> Path:
    """Get full path to output file, creating directory if needed."""
    if output_dir == "data":
        target_dir = DATA_DIR
    elif output_dir == "reports":
        target_dir = REPORTS_DIR
    elif output_dir == "notebooks":
        target_dir = NOTEBOOKS_DIR
    else:
        raise ValueError(f"Unknown output directory: {output_dir}")
    
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / filename
