# Data Dictionary

Dokumentasi lengkap struktur data untuk project SNA MBG.

## CSV Files

### 1. `data/preprocessed_tweets.csv`

Dataset utama berisi 5.000 interaksi yang telah dipreproses.

| Column | Type | Description | Example | Notes |
|--------|------|-------------|---------|-------|
| **user** | string | Username/akun yang membuat tweet | `jokowi` | Unique identifier untuk source node |
| **mentions** | string | List mentions dalam tweet (string repr) | `['kemenkesRI', 'airlangga_hrt', 'CNNIndonesia']` | Diparse menggunakan `ast.literal_eval()` |
| **cleaned_text** | string | Teks tweet yang sudah dinormalisasi | `"Anggaran MBG diperbesar..."` | Whitespace & URL sudah dihapus |

**Data Quality:**
- Total rows: 5.000 (data interaksi)
- No null values detected
- All mentions properly formatted as list strings
- No duplicate records

**Usage:**
- Input untuk graph construction (user → mentions relationships)
- Source untuk edge weighting (repeated mentions = higher weight)
- Dapat dianalisis lebih lanjut untuk sentiment/topic extraction

---

### 2. `data/network_communities.csv`

Hasil dari community detection dan centrality analysis.

| Column | Type | Description | Range | Interpretation |
|--------|------|-------------|-------|-----------------|
| **node** | string | Username/akun identifier | varies | Same as 'user' in preprocessed_tweets.csv |
| **community** | integer | Community ID hasil Louvain algorithm | 0-2 | 0, 1, 2 = tiga komunitas terdeteksi |
| **degree_centrality** | float | Degree centrality score (normalized) | 0.0 - 1.0 | Higher = more direct connections |
| **betweenness_centrality** | float | Betweenness centrality score | 0.0 - X | Higher = more "bridge" role; not normalized |
| **closeness_centrality** | float | Closeness centrality score (weighted) | 0.0 - 1.0 | Higher = closer to all other nodes |
| **sentiment_score** | float | Sentiment score (Phase 3 - Experimental) | -1.0 - 1.0 | Average sentiment of mentions from/to node |

**Network Statistics:**
- Total unique nodes: 238 (akun)
- Total edges: 6.187 (mention relationships)
- Communities detected: 3 (Louvain algorithm)
- Modularity: ~0.21 (moderate fragmentation)

**Community Breakdown:**
| Community | Size | Internal Edges | Density | Top Influencer |
|-----------|------|----------------|---------|-----------------|
| 0 | 39 nodes | 450 | 0.607 | kompascom |
| 1 | 90 nodes | 1.123 | 0.280 | warga_indonesia_4 |
| 2 | 109 nodes | 1.519 | 0.258 | warga_indonesia_187 |

**Centrality Interpretation:**

**Betweenness Centrality:**
- **High (>0.04)**: Bridge/gateway actor connecting multiple communities
- **Medium (0.01-0.04)**: Secondary bridges within network
- **Low (<0.01)**: Peripheral or terminal nodes
- Examples: Media outlets typically have high betweenness

**Degree Centrality:**
- **High (>0.05)**: Many direct connections (hub/popular target)
- **Medium (0.02-0.05)**: Moderate connectivity
- **Low (<0.02)**: Few connections
- Examples: Government officials often have high degree (polarizing figures)

**Closeness Centrality:**
- **High (>0.3)**: Close to most other nodes in network
- **Medium (0.2-0.3)**: Moderate distance
- **Low (<0.2)**: Far from most nodes
- Indicates global centrality vs local centrality (betweenness/degree)

---

### 3. `data/raw_tweets.csv` (If applicable)

Original untouched data sebelum preprocessing (opsional).

**Expected columns (if exists):**
- `user`: Original username
- `tweet_id`: Unique tweet identifier
- `created_at`: Timestamp
- `text`: Original tweet text (unclean)
- `mentions`: Raw mentions (may have formatting variations)
- `retweet_count`, `like_count`: Engagement metrics

---

## Network Graph Structure

### Graph Properties

```
Type: Undirected, Weighted Graph
Nodes: 238 unique actors (users)
Edges: 6.187 mention relationships
Weight: Mention frequency (1-N, where N=repeat mentions)
```

### Node Attributes

Each node represents a Twitter account with:
- `community`: Assigned community ID (0, 1, or 2)
- `degree`: Number of direct connections
- `betweenness_centrality`: Shortest-path betweenness score
- `closeness_centrality`: Average distance to all nodes
- `weight`: Sum of edge weights (incoming + outgoing mentions)
- `sentiment_score`: average sentiment score (Phase 3 - Experimental, defaults to 0.0 for Indonesian)

### Edge Attributes

Each edge represents:
- `weight`: How many times A mentioned B + how many times B mentioned A
- `source`: Originating user
- `target`: Mentioned user

---

## Centrality Metrics Definitions

See [METHODOLOGY.md](METHODOLOGY.md) for math formulas and details.

---

## Data Quality Notes

### Issues Handled

1. **Self-mentions**: Filtered out (User A mentioning User A)
2. **Null values**: Already removed in preprocessing
3. **Duplicates**: No exact duplicates found
4. **Formatting variations**: Standardized in parsing

### Potential Improvements

1. **Temporal dimension**: Add timestamp for tracking network evolution
2. **Sentiment Analysis (Native)**: Implement native Indonesian models like IndoBERT instead of English lexicon tools.
3. **Bot detection**: Remove automated/spam mentions
4. **Language**: Standardize translation/transliteration
5. **Hashtags**: Extract and analyze popular themes

---

## Reproducibility

### To Recreate All Outputs

```bash
# 1. Generate data (if not using real tweets)
python src/generate_dummy.py

# 2. Preprocess
python src/preprocess.py

# 3. Build network and detect communities
python src/network_analysis.py

# 4. Visualize
python src/visualize.py

# 5. Run notebook for detailed analysis
jupyter notebook notebooks/main_analysis.ipynb
```

### Expected File State After Running

- `data/preprocessed_tweets.csv`: 5000 rows ✓
- `data/network_communities.csv`: 238 rows ✓
- `reports/community_visualization.png`: 300 DPI PNG ✓
- `notebooks/network_interactive.html`: Pyvis interactive ✓

---

## Known Limitations

> [!WARNING]
> **Phase 3 Sentiment Analysis Limitation:**
> The current sentiment analysis implementation is **Incomplete & Experimental**. 
> Lexicon engines VADER and TextBlob are trained on English text. When run on Indonesian tweets, they fail to recognize vocabulary and return `0.0` (Neutral). This results in a 100% neutral sentiment distribution. 
> To obtain accurate sentiment analysis, a future implementation must use a trained Indonesian model (such as IndoBERT) or translate the corpus to English before applying VADER/TextBlob.

1. **Static Analysis**: Snapshot at one point in time
2. **Simulation Data**: 5000 records are generated for demo (not real tweets)
3. **Weighted but Undirected**: Doesn't distinguish A→B vs B→A direction
4. **One-time Partition**: Community assignments don't change even if network updates
5. **No Temporal**: Cannot track how communities form/dissolve over time

---

*Last Updated: 22 Mei 2026*  
*Reviewed by: Antigravity AI*
