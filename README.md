# Analisis Jaringan Sosial (SNA) - Deteksi Komunitas Diskusi MBG di X/Twitter

**Status:** ✅ Production Ready for Phase 1 & 2 | ⚠️ Phase 3 Incomplete/Experimental  
**Last Updated:** 22 Mei 2026  
**Python:** 3.8+

---

## 📋 Daftar Isi

- [Ringkasan Proyek](#ringkasan-proyek)
- [Status Phase 3 (Sentiment Analysis)](#-status-phase-3-sentiment-analysis)
- [Fitur Utama](#-fitur-utama)
- [Instalasi & Setup](#-instalasi--setup)
- [Quick Start](#-quick-start)
- [Struktur Folder](#-struktur-folder)
- [Pipeline Lengkap](#-pipeline-lengkap)
- [Interpretasi Hasil](#-interpretasi-hasil)
- [FAQ & Troubleshooting](#-faq--troubleshooting)
- [Dokumentasi Lengkap](#-dokumentasi-lengkap)

---

## 📊 Ringkasan Proyek

Proyek ini melakukan **Social Network Analysis (SNA)** komprehensif terhadap diskusi Program Makan Bergizi Gratis (MBG) di platform X/Twitter.

### Apa yang kami analisis?

```
5.000+ interaksi → 238 aktor → 3 komunitas terdeteksi → 4 centrality metrics
```

### Hasil Utama

| Metric | Value | Interpretation |
|--------|-------|-----------------|
| **Nodes** | 238 | Unique Twitter accounts |
| **Edges** | 6.187 | Mention relationships |
| **Communities** | 3 | Distinct discourse clusters |
| **Modularity** | 0.21 | Moderate fragmentation |
| **Top Influencer** | kompascom | Highest betweenness centrality |
| **Connected** | Yes (98%) | Network mostly connected |

---

## ⚠️ Status Phase 3 (Sentiment Analysis)

> [!WARNING]
> **Phase 3 Sentiment Analysis is Incomplete and Experimental.**
> 
> **The Problem:**
> The current sentiment analysis implementation integrates **VADER** and **TextBlob**. Both tools are **lexicon-based** models that rely on **English** dictionaries. 
> Since our dataset consists of **Indonesian** text, these lexicons do not recognize the vocabulary and classify almost all texts with a sentiment polarity score of `0.0`. This produces an incorrect result of **100% Neutral** sentiment.
>
> **The Planned Solution:**
> A future release will address this limitation through:
> 1. **Translation Pipeline:** Translating Indonesian tweets into English (e.g. using Google Translate API) before passing them to the sentiment analyzers.
> 2. **Native Indonesian NLP Models:** Replacing lexicon engines with trained Indonesian language transformers, such as **IndoBERT**, or native Indonesian lexicon libraries (e.g., InSet).

---

## ✨ Fitur Utama

### 1. **Multiple Visualizations**
- 📊 Static PNG (presentation-ready)
- 🖱️ Interactive Pyvis HTML (exploratory)
- 📈 Plotly in-notebook (analysis)

### 2. **Deep Analytics**
- 🔵 Betweenness Centrality (information bridges)
- 📍 Degree Centrality (popularity hubs)
- 🌐 Closeness Centrality (global centrality)
- 🔗 PageRank (iterative importance)
- 🎯 Combined Influence Score

### 3. **Community Insights**
- Size, density, internal/external edges
- Top influencers per community
- Cross-community bridges
- Community-specific patterns

### 4. **Network Robustness**
- Connectivity analysis
- Impact of node removal
- Fragility assessment
- Critical actors identification

---

## 🚀 Instalasi & Setup

### Prasyarat

- Python 3.8 atau lebih baru
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone & Setup

```bash
# Navigate to the workspace folder
cd sna-twitter-community

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Install packages from requirements
pip install -r requirements.txt
```

### Step 3: Setup Environment & Credentials

To fetch real data or configure credentials without committing secrets:
1. Copy `.env.example` to `.env`
2. Populate the Twitter session variables (`X_AUTH_TOKEN`, `X_CT0`) or place a valid `cookies.json` file in the root.

---

## ⚡ Quick Start

### Opsi A: Use Generated Data (Recommended untuk pertama kali)

```bash
# 1. Generate simulated data (5000 interactions)
python src/generate_dummy.py
# Output: data/preprocessed_tweets.csv

# 2. Build network & detect communities
python src/network_analysis.py
# Output: data/network_communities.csv

# 3. Create static visualization
python src/visualize.py
# Output: reports/community_visualization.png

# 4. Explore in notebook
jupyter notebook notebooks/main_analysis.ipynb
```

### Opsi B: Use Real Twitter Data

1. **Setup Twitter Credentials**:
   - Provide a `cookies.json` or write environment variables in `.env`.

2. **Run Pipeline**:
   ```bash
   python src/crawler_twikit.py      # Collect data
   python src/preprocess.py           # Clean data
   python src/network_analysis.py    # Analyze network (emits Phase 3 warnings)
   python src/visualize.py            # Create visualizations
   jupyter notebook notebooks/main_analysis.ipynb  # Explore
   ```

---

## 📁 Struktur Folder

```
sna-twitter-community/
├── README.md                          # File ini
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules (ignores cookies, datasets, .env)
├── .env.example                       # Environment template
│
├── src/                               # Source code
│   ├── __init__.py
│   ├── config.py                      # Centralized configuration
│   ├── logging_utils.py              # Logging setup
│   ├── graph_utils.py                # Shared graph building
│   ├── crawler_twikit.py             # Twitter data collector (credential-secured)
│   ├── generate_dummy.py             # Generate simulated data
│   ├── preprocess.py                 # Data cleaning
│   ├── network_analysis.py           # Network construction & analysis (secured)
│   ├── sentiment_analyzer.py         # Sentiment analysis module (warnings injected)
│   └── visualize.py                  # Static PNG visualization
│
├── data/                              # Data files (ignored by git, except .gitkeep)
│   └── .gitkeep
│
├── notebooks/                         # Jupyter notebooks
│   ├── main_analysis.ipynb           # Main analysis & exploration
│   └── network_interactive.html      # Pyvis interactive visualization
│
├── reports/                           # Output reports (ignored by git, except .gitkeep)
│   └── .gitkeep
│
└── docs/                              # Documentation
    ├── DATA_DICTIONARY.md            # Data structure & definitions
    └── METHODOLOGY.md                # Detailed methodology & algorithms
```

---

## 🔄 Pipeline Lengkap

### Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Data Collection & Preprocessing                    │
├─────────────────────────────────────────────────────────────┤
│  Input:  Live X/Twitter data OR simulated data              │
│  Process: Clean, normalize, remove noise                    │
│  Output: data/preprocessed_tweets.csv (5000 rows)          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Network Construction & Analysis                    │
├─────────────────────────────────────────────────────────────┤
│  Input:  preprocessed_tweets.csv                           │
│  Build:  238-node, 6187-edge undirected weighted graph     │
│  Analyze: 3 communities, centrality metrics                │
│  Sentiment: Lexicon analysis (⚠️ Experimental/Incomplete)    │
│  Output: data/network_communities.csv                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Visualization & Interpretation                     │
├─────────────────────────────────────────────────────────────┤
│  Static PNG:     reports/community_visualization.png       │
│  Interactive:    notebooks/network_interactive.html        │
│  Notebook:       notebooks/main_analysis.ipynb             │
│  Output:         3 different visual representations        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 Interpretasi Hasil

### Network Statistics

```
Nodes: 238         → Unique accounts participating
Edges: 6,187       → Mention relationships
Density: 0.0011    → Sparse network (typical for social media)
Avg Degree: 52     → Average 52 connections per account
```

### Communities (3 detected)

| ID | Size | Density | Characteristics | Top Influencer |
|----|------|---------|-----------------|-----------------|
| 0 | 39 | 0.607 | **Tight Media/Official** - closely connected group | kompascom |
| 1 | 90 | 0.280 | **Mixed Stakeholders** - moderate interaction | warga_indonesia_4 |
| 2 | 109 | 0.258 | **Grassroots Citizens** - dispersed network | warga_indonesia_187 |

---

## ❓ FAQ & Troubleshooting

### Q1: "ModuleNotFoundError: No module named 'community'"
**A:** Install python-louvain: `pip install python-louvain`

### Q2: "Why are all my sentiment scores 0.0 (Neutral)?"
**A:** The analysis runs on Indonesian text, while VADER/TextBlob only support English. See [Status Phase 3](#-status-phase-3-sentiment-analysis) for context and workarounds.

### Q3: "Different results when I run again?"
**A:** Check random seeds in `config.py`. They are locked at `42` for Louvain and spring layout.

---

## 📚 Dokumentasi Lengkap

1. **docs/DATA_DICTIONARY.md** 📖
   - Column meanings, data types, and file structure definitions.
2. **docs/METHODOLOGY.md** 🔬
   - Louvain, PageRank, and Centrality mathematical formulas and parameters.

---

## 🎯 Roadmap

### Phase 1 ✅ (Completed)
- [x] Path consistency fixes
- [x] Error logging system
- [x] Empty graph validation

### Phase 2 ✅ (Completed)
- [x] Requirements.txt Setup
- [x] Data dictionary documentation
- [x] Centrality metrics integration
- [x] Code refactoring & directory structure

### Phase 3 📋 (Under Redesign / Incomplete)
- [ ] **Sentiment analysis (Indonesian compatible)** ⚠️
- [ ] Statistical confidence intervals
- [ ] Unit testing framework

### Phase 4 🎨 (Future)
- [ ] Temporal analysis
- [ ] Web dashboard

---

*Last Updated: 22 Mei 2026*  
*Status: Production Ready (Phases 1-2) | Under Redesign (Phase 3)*  
*Maintainer: Antigravity AI*
