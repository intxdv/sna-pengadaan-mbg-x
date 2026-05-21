import pandas as pd
import re
import logging
import os
import ast
from src.config import (
    RAW_TWEETS_REAL_FILE, 
    PREPROCESSED_TWEETS_REAL_FILE, 
    PREPROCESSED_TWEETS_CENSORED_FILE, 
    PREPROCESSED_TWEETS_FILE, 
    OFFICIAL_ACCOUNTS
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(text):
    """
    Basic text cleaning for tweets.
    """
    if pd.isna(text):
        return ""
    # Remove URLs
    text = re.sub(r'http\S+', '', str(text))
    # Remove mentions (@user)
    text = re.sub(r'@\w+', '', text)
    # Remove hashtags (#tag)
    text = re.sub(r'#\w+', '', text)
    # Remove newlines and extra spaces
    text = text.replace('\n', ' ').strip()
    return text

def extract_mentions(text):
    """
    Extract usernames mentioned in the tweet.
    """
    if pd.isna(text):
        return []
    return re.findall(r'@(\w+)', str(text))

def censor_usernames(df, official_accounts):
    """
    Anonymize private public citizens to 'warga_indonesia_x' while keeping
    official accounts from the whitelist intact. Keeps the network topology identical.
    """
    logging.info("Starting username anonymization/censoring...")
    
    # Find all unique usernames in the dataset
    all_users = set()
    for _, row in df.iterrows():
        if not pd.isna(row['user']):
            all_users.add(row['user'])
        
        mentions_val = row.get('mentions', [])
        if isinstance(mentions_val, str):
            try:
                mentions_list = ast.literal_eval(mentions_val)
                if isinstance(mentions_list, list):
                    all_users.update(mentions_list)
            except Exception:
                pass
        elif isinstance(mentions_val, list):
            all_users.update(mentions_val)

    # Build mapping for non-official accounts
    mapping = {}
    counter = 1
    
    # Sort accounts to make the mapping deterministic for reproducibility
    sorted_users = sorted(list(all_users))
    
    for username in sorted_users:
        if pd.isna(username) or username == '':
            continue
        u_lower = username.lower()
        if u_lower in official_accounts:
            mapping[username] = username  # Keep original official account
        elif u_lower.startswith('warga_indonesia_'):
            # Already simulated/anonymized, keep it
            mapping[username] = username
        else:
            mapping[username] = f"warga_indonesia_{counter}"
            counter += 1

    logging.info(f"Anonymized {counter - 1} private citizen accounts. Kept {len(all_users) - (counter - 1)} official/existing accounts intact.")

    # Apply mapping
    censored_df = df.copy()
    censored_df['user'] = censored_df['user'].map(lambda u: mapping.get(u, u))
    
    # Replace in text, cleaned_text, and mentions
    def anonymize_text_and_mentions(row):
        text = str(row['text'])
        cleaned_text = str(row['cleaned_text'])
        mentions = row['mentions']
        
        # Anonymize mentions in the list
        if isinstance(mentions, str):
            try:
                mentions_list = ast.literal_eval(mentions)
            except Exception:
                mentions_list = []
        elif isinstance(mentions, list):
            mentions_list = mentions
        else:
            mentions_list = []
            
        new_mentions = [mapping.get(m, m) for m in mentions_list]
        
        # Replace mentions in text (case-insensitively replace @username with @mapped_username)
        # To avoid partial matches (e.g. @budi replacing part of @budi_jakarta), we sort keys by length descending
        sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
        for original in sorted_keys:
            mapped = mapping[original]
            if original != mapped:
                # Replace case-insensitively
                pattern = re.compile(rf'@{re.escape(original)}\b', re.IGNORECASE)
                text = pattern.sub(f'@{mapped}', text)
                cleaned_text = pattern.sub(f'@{mapped}', cleaned_text)
                
        return pd.Series([text, cleaned_text, new_mentions], index=['text', 'cleaned_text', 'mentions'])

    censored_df[['text', 'cleaned_text', 'mentions']] = censored_df.apply(anonymize_text_and_mentions, axis=1)
    
    return censored_df

def preprocess_data(input_path, output_path_real, output_path_censored, official_accounts):
    """
    Load raw tweets, clean them, extract interaction edges, and create both real and censored versions.
    """
    try:
        if not os.path.exists(input_path):
            logging.error(f"Input file {input_path} not found!")
            return None
            
        df = pd.read_csv(input_path)
        logging.info(f"Loaded {len(df)} raw tweets from {input_path}.")

        # Rename columns for consistency if needed
        if 'username' in df.columns:
            df = df.rename(columns={'username': 'user'})

        # Extract mentions before cleaning the text
        df['mentions'] = df['text'].apply(extract_mentions)
        
        # Clean the tweet text
        df['cleaned_text'] = df['text'].apply(clean_text)
        
        # Drop duplicates based on text
        df = df.drop_duplicates(subset=['text']).reset_index(drop=True)
        logging.info(f"Data count after removing duplicates: {len(df)}")

        # 1. Save real preprocessed version
        df.to_csv(output_path_real, index=False)
        logging.info(f"Preprocessed REAL data saved to {output_path_real}")

        # 2. Generate censored version
        censored_df = censor_usernames(df, official_accounts)

        # 3. Save censored preprocessed version
        censored_df.to_csv(output_path_censored, index=False)
        logging.info(f"Preprocessed CENSORED data saved to {output_path_censored}")
        
        # Sync with legacy/default path for safety
        censored_df.to_csv(PREPROCESSED_TWEETS_FILE, index=False)
        logging.info(f"Preprocessed default path synced to {PREPROCESSED_TWEETS_FILE}")

        return df

    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")
        return None

if __name__ == "__main__":
    preprocess_data(
        RAW_TWEETS_REAL_FILE, 
        PREPROCESSED_TWEETS_REAL_FILE, 
        PREPROCESSED_TWEETS_CENSORED_FILE, 
        OFFICIAL_ACCOUNTS
    )
