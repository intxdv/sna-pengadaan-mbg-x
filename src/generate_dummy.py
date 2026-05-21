import pandas as pd
import numpy as np
import random
import os

def generate_dummy_data(output_path, num_tweets=50):
    users = ['user_pro1', 'user_pro2', 'user_con1', 'user_con2', 'news_bot', 'expert_A', 'expert_B', 'politician_X', 'citizen_Y', 'citizen_Z']
    
    topics = [
        "Anggaran MBG harus transparan! #MBG #Pengadaan",
        "Vendor pengadaan MBG kok itu-itu aja? Ada apa ini?",
        "Susu ikan solusi protein untuk MBG? Menarik.",
        "Program Makan Bergizi Gratis sangat membantu anak sekolah.",
        "Kenapa proyek MBG tidak melibatkan UMKM lokal?",
        "Data pengadaan MBG harusnya dibuka ke publik.",
        "Korupsi pengadaan bisa hancurkan program MBG.",
        "Dukung penuh program Makan Bergizi Gratis!",
        "Kajian ekonomi MBG masih meragukan.",
        "Siapa vendor susu ikan untuk MBG?"
    ]
    
    data = []
    for i in range(num_tweets):
        user = random.choice(users)
        text = random.choice(topics)
        
        # Randomly add mentions
        if random.random() > 0.5:
            mention = random.choice(users)
            if mention != user:
                text += f" cc: @{mention}"
        
        data.append({
            'link': f'https://x.com/tweet/{i}',
            'text': text,
            'user': user,
            'date': 'May 21, 2026',
            'retweets': random.randint(0, 100),
            'comments': random.randint(0, 50),
            'likes': random.randint(0, 500),
            'quotes': random.randint(0, 20)
        })
    
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {num_tweets} dummy tweets at {output_path}")

if __name__ == "__main__":
    generate_dummy_data('data/raw_tweets.csv')
