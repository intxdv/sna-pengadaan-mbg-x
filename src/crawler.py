import pandas as pd
from ntscraper import Nitter
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def collect_tweets(query, mode='term', limit=1000):
    """
    Collect tweets using Nitter scraper.
    """
    # Try multiple instances if one fails
    scraper = Nitter(log_level=1, skip_instance_check=False)
    
    logging.info(f"Starting data collection for query: {query}")
    
    try:
        # Manually specify a known working Nitter instance if auto-select fails
        # or use skip_instance_check=True to skip testing
        scraper = Nitter(log_level=1, skip_instance_check=True)
        
        # Simple query
        test_query = "Makan Bergizi Gratis"
        logging.info(f"Trying with simple query: {test_query} and skip_instance_check=True")
        
        # Try specifically with a known instance
        tweets = scraper.get_tweets(test_query, mode=mode, number=limit, instance='https://nitter.net')
        
        if not tweets['tweets']:
            logging.warning("No tweets found.")
            return None
            
        data = []
        for tweet in tweets['tweets']:
            data.append({
                'link': tweet['link'],
                'text': tweet['text'],
                'user': tweet['user']['username'],
                'date': tweet['date'],
                'retweets': tweet['stats']['retweets'],
                'comments': tweet['stats']['comments'],
                'likes': tweet['stats']['likes'],
                'quotes': tweet['stats']['quotes']
            })
            
        df = pd.DataFrame(data)
        return df
        
    except Exception as e:
        logging.error(f"Error during collection: {e}")
        return None

if __name__ == "__main__":
    # Keywords related to MBG procurement and budget controversy
    keywords = "(pengadaan MBG) OR (vendor MBG) OR (anggaran MBG) OR (susu ikan MBG)"
    
    # Target 1000 tweets for initial analysis
    df_tweets = collect_tweets(keywords, limit=1000)
    
    if df_tweets is not None:
        if not os.path.exists('data'):
            os.makedirs('data')
            
        output_file = 'data/raw_tweets.csv'
        df_tweets.to_csv(output_file, index=False)
        logging.info(f"Successfully saved {len(df_tweets)} tweets to {output_file}")
    else:
        logging.error("Failed to collect tweets.")
