import pandas as pd
import random
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_grand_dataset(size=1000):
    """
    Generate a large-scale, high-quality simulated dataset for Social Network Analysis.
    This creates realistic discourse patterns about the MBG (Makan Bergizi Gratis) program.
    """
    
    # 1. Categories of Users
    communities = {
        'Government': ['kemensetneg', 'kemenkeuRI', 'kemenkesRI', 'Kemendikbud_RI', 'prabowo', 'gibran_tweet', 'sandiuno', 'airlangga_hrt'],
        'Media': ['detikcom', 'tempodotco', 'kompascom', 'antaranews', 'VIVAcoid', 'CNNIndonesia', 'kumparan', 'BBCIndonesia'],
        'Critics/NGO': ['Lembaga_Keadilan', 'Aliansi_Rakyat', 'pengamat_sosial', 'tokoh_oposisi', 'aktivis_lingkungan', 'Yayasan_Gizi', 'IndoWitch'],
        'Public/Opinion': [f'user_{i}' for i in range(1, 50)],
        'Business/Vendor': ['asosiasi_vendor', 'pt_pangan_makmur', 'koprasi_susu', 'direktur_logistik', 'pengusaha_lokal', 'umkm_juara']
    }
    
    all_users = []
    for cat in communities:
        all_users.extend(communities[cat])
    
    # 2. Content Templates
    templates = [
        "Program Makan Bergizi Gratis (MBG) harus dipastikan menggunakan bahan pangan lokal. #MBG #PanganLokal",
        "Anggaran 71 Triliun untuk MBG perlu pengawasan ketat agar tidak dikorupsi vendor nakal. @kemensetneg",
        "Susu ikan sebagai alternatif protein di program MBG sangat inovatif, tapi bagaimana distribusinya? @kemenkesRI",
        "Kami sebagai vendor siap mendukung pengadaan makanan bergizi untuk anak sekolah. @kemenkeuRI",
        "Dampak ekonomi program MBG bagi UMKM di daerah sangat besar jika dikelola transparan.",
        "Evaluasi uji coba MBG di beberapa daerah menunjukkan antusiasme tinggi dari siswa.",
        "Siapa saja vendor yang menang tender pengadaan susu MBG? Rakyat butuh transparansi. @tempodotco",
        "Implementasi MBG jangan sampai membebani fiskal negara secara berlebihan. @airlangga_hrt",
        "Gizi anak adalah investasi masa depan. Dukung penuh MBG!",
        "Tolong diperhatikan kualitas sayur dan lauk pauk di program makan gratis ini. @gibran_tweet"
    ]
    
    data = []
    logging.info(f"Generating {size} simulated tweet interactions...")
    
    for i in range(size):
        # Pick a random user from a random category
        cat_name = random.choice(list(communities.keys()))
        user = random.choice(communities[cat_name])
        
        # Pick a template
        text = random.choice(templates)
        
        # Logic for mentions (creating communities)
        # 60% chance to mention someone in the SAME community
        # 30% chance to mention someone in a RELATED community
        # 10% chance to mention a random user
        mentions = []
        rand_val = random.random()
        
        target_cat = cat_name
        if rand_val > 0.6:
            # Cross-community interaction
            if cat_name == 'Government': target_cat = random.choice(['Media', 'Critics/NGO'])
            elif cat_name == 'Critics/NGO': target_cat = 'Government'
            elif cat_name == 'Business/Vendor': target_cat = 'Government'
            else: target_cat = random.choice(list(communities.keys()))
            
        target_pool = communities[target_cat]
        num_mentions = random.randint(1, 3)
        mentions = random.sample(target_pool, min(num_mentions, len(target_pool)))
        
        # Remove self-mentions
        if user in mentions:
            mentions.remove(user)
            
        data.append({
            'user_id': f'uid_{i}',
            'username': user,
            'text': f"{text} {' '.join(['@'+m for m in mentions])}",
            'created_at': f'2024-11-{random.randint(1,30):02d}',
            'retweet_count': random.randint(0, 500),
            'favorite_count': random.randint(0, 1000),
            'mentions': mentions
        })
        
    df = pd.DataFrame(data)
    
    if not os.path.exists('data'):
        os.makedirs('data')
        
    df.to_csv('data/raw_tweets.csv', index=False)
    logging.info(f"Successfully generated {len(df)} entries in data/raw_tweets.csv")
    return df

if __name__ == "__main__":
    generate_grand_dataset(1200) # 1200 entries for a thick graph
