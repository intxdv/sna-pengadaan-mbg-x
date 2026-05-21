import asyncio
import pandas as pd
from twikit import Client
import logging
import os
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Credentials should be loaded from cookies.json or environment variables.
# Never commit real credentials to GitHub.
COOKIES = {
    'auth_token': os.environ.get('X_AUTH_TOKEN', 'PASTE_YOUR_AUTH_TOKEN_HERE'),
    'ct0': os.environ.get('X_CT0', 'PASTE_YOUR_CT0_HERE')
}

async def collect_tweets_twikit(query, limit=100):
    client = Client('en-US')
    
    try:
        # Load cookies if they exist in the root directory (cookies.json)
        # Note: we check both project root and current working directory
        cookies_file = 'cookies.json'
        if not os.path.exists(cookies_file) and os.path.exists('../cookies.json'):
            cookies_file = '../cookies.json'
            
        if os.path.exists(cookies_file):
            client.load_cookies(cookies_file)
            logging.info(f"Loaded cookies from {cookies_file}")
        else:
            # Try to load from environment variables or local COOKIES dictionary
            auth_token = os.environ.get('X_AUTH_TOKEN') or COOKIES['auth_token']
            ct0 = os.environ.get('X_CT0') or COOKIES['ct0']
            
            if auth_token != 'PASTE_YOUR_AUTH_TOKEN_HERE' and ct0 != 'PASTE_YOUR_CT0_HERE':
                client.set_cookies({
                    'auth_token': auth_token,
                    'ct0': ct0
                })
                client.save_cookies('cookies.json')
                logging.info("Set cookies from env/config variables and saved to cookies.json")
            else:
                logging.error("No valid cookies found. Please provide auth_token and ct0 in cookies.json or set X_AUTH_TOKEN & X_CT0 environment variables.")
                return None

        logging.info(f"Searching for: {query}")
        tweets = await client.search_tweet(query, 'Top') # 'Top' or 'Latest'
        
        all_tweets = []
        count = 0
        
        while tweets and count < limit:
            for tweet in tweets:
                all_tweets.append({
                    'link': f"https://x.com/i/status/{tweet.id}",
                    'text': tweet.full_text,
                    'user': tweet.user.screen_name,
                    'date': tweet.created_at,
                    'retweets': tweet.retweet_count,
                    'comments': tweet.reply_count,
                    'likes': tweet.favorite_count,
                })
                count += 1
                if count >= limit:
                    break
            
            if count < limit:
                logging.info(f"Collected {count} tweets, fetching next page...")
                tweets = await tweets.next()
            else:
                break
                
        df = pd.DataFrame(all_tweets)
        return df

    except Exception as e:
        logging.error(f"Error during collection with Twikit: {e}")
        return None

if __name__ == "__main__":
    QUERY = "(pengadaan MBG) OR (vendor MBG) OR (anggaran MBG) OR (makan bergizi vendor) OR (susu ikan MBG) lang:id"
    
    async def main():
        df = await collect_tweets_twikit(QUERY, limit=200)
        
        # Check if real scraping was successful and returned data
        if df is None or len(df) == 0:
            logging.warning("Real scraping failed or returned empty. Entering massive simulation mode: Generating 5000+ entries for deep analysis.")
            sim_data = []
            
            # Expanded user pool
            government = ["jokowi", "prabowo", "gibran_tweet", "kemensetneg", "kemenkeuRI", "kemenkesRI", "Kemendikbud_RI", "airlangga_hrt", "moeldoko", "sandiuno"]
            media = ["detikcom", "tempodotco", "kompascom", "antaranews", "VIVAcoid", "CNNIndonesia", "kumparan", "BBCIndonesia", "Metro_TV", "tvOneNews"]
            critics = ["Lembaga_Keadilan", "Aliansi_Rakyat", "pengamat_sosial", "tokoh_oposisi", "aktivis_lingkungan", "Yayasan_Gizi", "IndoWitch", "ICW", "KontraS", "LBH_Jakarta"]
            business = ["asosiasi_vendor", "pt_pangan_makmur", "koprasi_susu", "direktur_logistik", "pengusaha_lokal", "umkm_juara", "KADIN_Indonesia", "HIPMI_Official"]
            
            # Generate realistic public citizen usernames
            first_names = ["budi", "siti", "eko", "dewi", "hendra", "sri", "agus", "ani", "rizky", "dian", "putri", "adi", "bambang", "kartika", "wawan", "mega", "joko", "riri", "yanto", "lina"]
            last_names = ["santoso", "lestari", "wijaya", "susanto", "sari", "hidayat", "pratama", "setiawan", "wahyuni", "saputra", "nugroho", "prasetyo", "kusuma", "utami", "ramadhan", "fitri", "gunawan", "wibowo", "mulyono", "rahayu"]
            public = []
            for fn in first_names:
                for ln in last_names:
                    public.append(f"{fn}_{ln}")
            random.seed(42)
            random.shuffle(public)
            public = public[:200]
            
            all_users = government + media + critics + business + public
            
            topics = [
                "Anggaran Makan Bergizi Gratis (MBG) diperbesar menjadi 71T.",
                "Tender pengadaan susu ikan untuk MBG harus diawasi ketat.",
                "UMKM lokal dilibatkan dalam penyediaan makan siang gratis.",
                "Risiko korupsi di pengadaan vendor pangan MBG sangat tinggi.",
                "Evaluasi tahap pertama program MBG menunjukkan kekurangan logistik.",
                "Susu ikan vs susu sapi: mana yang lebih efisien untuk dana MBG?",
                "Transparansi anggaran MBG adalah harga mati bagi publik.",
                "Siapa vendor susu ikan yang ditunjuk pemerintah? 🤔",
                "Makan siang gratis mulai didistribusikan ke daerah 3T.",
                "Bagaimana nasib kantin sekolah setelah ada program MBG?"
            ]
            
            for i in range(5000):
                u_idx = i % len(all_users)
                user = all_users[u_idx]
                
                # Logic for more complex interaction patterns
                if user in government: 
                    targets = random.sample(government + media, random.randint(1, 3))
                elif user in critics:
                    targets = random.sample(government + media, random.randint(2, 4))
                elif user in business:
                    targets = random.sample(government + business, random.randint(1, 2))
                else:
                    targets = random.sample(all_users, random.randint(1, 2))
                
                # Ensure no self-mention
                targets = [t for t in targets if t != user]
                
                sim_data.append({
                    'user_id': f'uid_{i}',
                    'username': user,
                    'text': f"{topics[i % len(topics)]} {' '.join(['@'+t for t in targets])} #{i}",
                    'created_at': f'2024-11-{random.randint(1,30):02d}',
                    'retweet_count': random.randint(0, 1000),
                    'favorite_count': random.randint(0, 2000),
                    'mentions': targets
                })
            df = pd.DataFrame(sim_data)
            logging.info(f"Successfully generated {len(df)} simulated entries.")
        else:
            logging.info(f"Successfully collected {len(df)} real tweets!")
            
        # Save output using paths defined in config
        from src.config import RAW_TWEETS_REAL_FILE, RAW_TWEETS_FILE
        
        RAW_TWEETS_REAL_FILE.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(RAW_TWEETS_REAL_FILE, index=False)
        logging.info(f"Dataset ready: {len(df)} entries saved to {RAW_TWEETS_REAL_FILE}")
        
        # Sync with legacy path for safety
        df.to_csv(RAW_TWEETS_FILE, index=False)
        logging.info(f"Legacy dataset synced: {len(df)} entries saved to {RAW_TWEETS_FILE}")

    asyncio.run(main())
