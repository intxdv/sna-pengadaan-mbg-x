# Analisis Jaringan Sosial (SNA) - Deteksi Komunitas Diskusi Pengadaan MBG di X/Twitter

**Status:** ✅ Production Ready for Phase 1 & 2 | ⚠️ Phase 3 Incomplete/Experimental  
**Last Updated:** 22 Mei 2026  
**Python:** 3.8+

---

## 📋 Daftar Isi

- [Ringkasan Proyek](#-ringkasan-proyek)
- [Fokus Topik & Kata Kunci](#-fokus-topik--kata-kunci)
- [Pipeline Dual-Dataset (Asli vs Sensor)](#-pipeline-dual-dataset-asli-vs-sensor)
- [Status Phase 3 (Sentiment Analysis)](#-status-phase-3-sentiment-analysis)
- [Fitur Utama](#-fitur-utama)
- [Instalasi & Setup](#-instalasi--setup)
- [Quick Start](#-quick-start)
- [Struktur Folder](#-struktur-folder)
- [Interpretasi Hasil](#-interpretasi-hasil)
- [FAQ & Troubleshooting](#-faq--troubleshooting)
- [Dokumentasi Lengkap](#-dokumentasi-lengkap)

---

## 📊 Ringkasan Proyek

Proyek ini melakukan **Social Network Analysis (SNA)** komprehensif terhadap percakapan seputar **Pengadaan program Makan Bergizi Gratis (MBG)** di platform X/Twitter. Analisis ini ditujukan untuk memetakan hubungan antarkomunitas, melacak penyebaran informasi, serta mengidentifikasi aktor-aktor kunci (influencer) yang menjembatani kelompok-kelompok wacana.

### Dimensi Analisis
```
5.000+ Interaksi → 238 Aktor Unik → 3 Komunitas Diskusi → 4 Centrality Metrics
```

### Hasil Utama (Berdasarkan Simulasi Data)

| Metric | Value | Interpretation |
|--------|-------|-----------------|
| **Nodes** | 238 | Jumlah akun unik dalam jaringan |
| **Edges** | 6.205 | Hubungan penyebutan (mention) antar-akun |
| **Communities** | 3 | Kelompok wacana/komunitas terdeteksi |
| **Modularity** | 0.22 | Fragmentasi percakapan sedang-tinggi |
| **Top Influencer** | kompascom | Aktor penghubung utama (*Betweenness*) |
| **Connectedness** | Yes (98%) | Mayoritas node saling terhubung |

---

## 🔍 Fokus Topik & Kata Kunci

Analisis ini **tidak mencakup opini publik MBG secara umum** (seperti rasa makanan atau kegembiraan siswa), melainkan berfokus pada **ekosistem ekonomi, pengadaan, dan kebijakan logistik**.

Kata kunci (*query*) pencarian yang ditargetkan di platform X/Twitter meliputi:
*   Aspek Finansial & Tender: `pengadaan MBG`, `anggaran MBG`
*   Aspek Bisnis & Kemitraan: `vendor MBG`, `makan bergizi vendor`
*   Kontroversi & Substitusi: `susu ikan MBG`

Fokus ini dipilih karena menyajikan dinamika polarisasi opini yang sangat cocok dianalisis menggunakan SNA, memisahkan faksi pendukung pemerintah, pihak swasta/vendor, kelompok oposisi/aktivis gizi, dan media massa.

---

## 🔒 Pipeline Dual-Dataset (Asli vs Sensor)

Untuk menjaga **kredibilitas ilmiah riset akademis** sekaligus mematuhi undang-undang **Pelindungan Data Pribadi (UU PDP)**, proyek ini mengimplementasikan jalur data ganda (*dual-dataset pipeline*):

```
                       [ RAW DATA: raw_tweets_real.csv ]
                                      │
                                      ▼
                             [ preprocess.py ]
                                      │
                  ┌───────────────────┴───────────────────┐
                  ▼                                       ▼
        [ DATA REAL / ASLI ]                   [ DATA CENSORED / SENSOR ]
   preprocessed_tweets_real.csv           preprocessed_tweets_censored.csv
  (Nama akun publik asli terjaga)       (Akun sipil menjadi warga_indonesia_x)
                                         (Akun resmi pemerintah & media aman)
```

1.  **Data Real (Asli):** Menggunakan nama pengguna Twitter asli. Digunakan untuk keperluan verifikasi riset internal dan validasi kredibilitas aktor.
2.  **Data Censored (Sensor):** Akun warga sipil (publik biasa) disamarkan secara konsisten menjadi `warga_indonesia_1`, `warga_indonesia_2`, dsb. di seluruh kolom penulis, isi teks (sebutan `@username`), dan daftar mentions. Akun resmi organisasi, media massa, kritikus publik, dan instansi pemerintah yang masuk dalam *whitelist* (`OFFICIAL_ACCOUNTS`) di [src/config.py](file:///d:/Dev/Project%20AJS/sna-pengadaan-mbg-x/src/config.py) dibiarkan asli untuk mempertahankan konteks struktural jaringan.

**Penting:** Kedua visualisasi dan analisis metrics menghasilkan struktur topologi jaringan (modularity, tingkat centrality) yang **100% identik secara matematis**.

---

## ⚠️ Status Phase 3 (Sentiment Analysis)

> [!WARNING]
> **Tahap 3 Analisis Sentimen berstatus Ekspresimental & Belum Selesai.**
> 
> *   **Masalah Saat Ini:** Mesin leksikon bawaan (**VADER** & **TextBlob**) hanya mendukung bahasa Inggris. Menganalisis tweet bahasa Indonesia akan menghasilkan skor default `0.0` (100% Netral).
> *   **Solusi Mendatang:** Rencana integrasi mencakup penerjemahan teks via API Google Translate sebelum dianalisis, atau menerapkan model transformer lokal seperti **IndoBERT** untuk analisis bahasa Indonesia asli.

---

## ✨ Fitur Utama

### 1. **Visualisasi Ganda (Real & Censored)**
*   📊 Grafik PNG statis siap presentasi: [community_visualization_real.png](file:///d:/Dev/Project%20AJS/sna-pengadaan-mbg-x/reports/community_visualization_real.png) & [community_visualization_censored.png](file:///d:/Dev/Project%20AJS/sna-pengadaan-mbg-x/reports/community_visualization_censored.png).
*   🌐 Visualisasi interaktif interaktif via Pyvis HTML.
*   📈 Plotly grafik interaktif untuk eksplorasi Jupyter Notebook.

### 2. **Metrik Jaringan Mendalam**
*   **Betweenness Centrality:** Menemukan broker informasi.
*   **Degree Centrality:** Mengukur tingkat popularitas langsung akun.
*   **Closeness Centrality:** Mengukur kecepatan penyebaran informasi ke seluruh jaringan.

---

## 🚀 Instalasi & Setup

### Prasyarat
*   Python 3.8 ke atas
*   Pip (Manajer paket Python)

### Step 1: Clone & Setup Ruang Kerja
```bash
# Masuk ke folder proyek
cd sna-pengadaan-mbg-x

# Buat virtual environment
python -m venv .venv

# Aktifkan virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### Step 2: Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### Step 3: Setup Kredensial Twitter (Opsional)
Salin file `.env.example` menjadi `.env` dan masukkan token otentikasi X (`X_AUTH_TOKEN`, `X_CT0`) Anda, atau simpan file sesi `cookies.json` di root direktori proyek agar crawler dapat berjalan. Jika kredensial kosong, crawler akan otomatis masuk ke **mode simulasi data**.

---

## ⚡ Quick Start

Jalankan rangkaian perintah berikut di terminal Anda untuk memproses data dari awal hingga menghasilkan visualisasi grafis:

```bash
# 1. Jalankan crawler (otomatis membuat data simulasi jika cookies tidak ada)
python -m src.crawler_twikit

# 2. Lakukan preprocessing & pembagian dataset (Real vs Sensor)
python -m src.preprocess

# 3. Jalankan analisis jaringan Louvain & penghitungan centrality
python -m src.network_analysis

# 4. Gambar visualisasi jaringan statis (PNG)
python -m src.visualize
```

Setelah selesai, visualisasi grafik dapat ditemukan di direktori `reports/` dan analisis data interaktif dapat dieksplorasi menggunakan Jupyter Notebook:
```bash
jupyter notebook notebooks/main_analysis.ipynb
```

---

## 📁 Struktur Folder

```
sna-pengadaan-mbg-x/
├── README.md                          # Dokumentasi proyek ini
├── requirements.txt                   # Dependensi Python
├── .gitignore                         # Konfigurasi pengabaian Git (mengamankan cookies & csv)
├── .env.example                       # Templat variabel lingkungan
│
├── src/                               # Kode sumber
│   ├── __init__.py
│   ├── config.py                      # Konfigurasi jalur file & whitelist akun resmi
│   ├── logging_utils.py               # Utilitas pencatatan log
│   ├── graph_utils.py                 # Utilitas pembangunan graf
│   ├── crawler_twikit.py              # Crawler X/Twitter dengan fallback simulasi
│   ├── preprocess.py                  # Pembersihan teks & penyensoran PDP
│   ├── network_analysis.py            # Kalkulasi algoritma Louvain & Centrality
│   ├── sentiment_analyzer.py          # Analisis sentimen (lexicon warning)
│   └── visualize.py                   # Render grafik jaringan PNG
│
├── data/                              # File data (diabaikan oleh git, kecuali .gitkeep)
│   ├── raw_tweets_real.csv
│   ├── preprocessed_tweets_real.csv
│   ├── preprocessed_tweets_censored.csv
│   ├── network_communities_real.csv
│   ├── network_communities_censored.csv
│   └── .gitkeep
│
├── notebooks/                         # Jupyter Notebooks
│   ├── main_analysis.ipynb            # Lembar eksplorasi analisis
│   └── network_interactive.html       # Visualisasi HTML interaktif
│
├── reports/                           # Output grafik (diabaikan oleh git, kecuali .gitkeep)
│   ├── community_visualization_real.png
│   ├── community_visualization_censored.png
│   └── .gitkeep
│
└── docs/                              # Dokumentasi metodologi & kamus data
    ├── DATA_DICTIONARY.md
    └── METHODOLOGY.md
```

---

## 📈 Interpretasi Hasil

### Karakteristik Komunitas Terdeteksi (Simulasi)

| ID Komunitas | Jumlah Anggota | Karakteristik Utama | Top Influencer |
| :---: | :---: | :--- | :--- |
| **0** | 39 | **Klaster Media & Instansi Resmi:** Diskusi searah menyampaikan fakta anggaran dan kebijakan. | `kompascom` |
| **1** | 90 | **Klaster Stakeholder & Bisnis:** Diskusi terfokus pada kesiapan UMKM, logistik, dan pasokan susu ikan. | `warga_indonesia_4` |
| **2** | 109 | **Klaster Sipil/Oposisi:** Debat kritis mengenai anggaran, kekhawatiran gizi susu ikan, dan pengawasan korupsi. | `warga_indonesia_187` |

---

## 📚 Dokumentasi Lengkap
1. **[docs/DATA_DICTIONARY.md](file:///d:/Dev/Project%20AJS/sna-pengadaan-mbg-x/docs/DATA_DICTIONARY.md)** 📖 — Definisi kolom data dan struktur file CSV.
2. **[docs/METHODOLOGY.md](file:///d:/Dev/Project%20AJS/sna-pengadaan-mbg-x/docs/METHODOLOGY.md)** 🔬 — Penjelasan matematis algoritma Louvain dan Centrality.

---

*Maintainer: Antigravity AI*  
*Status Keamanan: **Terverifikasi Aman (Akses Kredensial & Data Mentah Terfilter Git)***
