from ntscraper import Nitter
import pandas as pd
import os

def test_nitter_instances():
    instances = ["nitter.poast.org", "nitter.privacydev.net", "nitter.projectsegfau.lt", "nitter.perennialte.ch"]
    scraper = Nitter()
    query = "(pengadaan MBG) OR (vendor MBG) lang:id"
    
    for instance in instances:
        print(f"Testing instance: {instance}")
        try:
            # ntscraper uses a random instance by default, but we can try to force one or just let it try
            # Actually, Nitter() selects one from a list.
            tweets = scraper.get_tweets(query, mode='term', number=50, instance=instance)
            if tweets and 'tweets' in tweets and len(tweets['tweets']) > 0:
                print(f"Success with {instance}! Found {len(tweets['tweets'])} tweets.")
                return tweets['tweets']
        except Exception as e:
            print(f"Failed {instance}: {e}")
            continue
    return None

if __name__ == "__main__":
    real_tweets = test_nitter_instances()
    if real_tweets:
        data = []
        for t in real_tweets:
            data.append({
                'username': t['user']['username'],
                'text': t['text'],
                'created_at': t['date'],
                'retweet_count': t['stats']['retweets'],
                'favorite_count': t['stats']['likes'],
                'mentions': [m['username'] for m in t['user_mentions']]
            })
        df = pd.DataFrame(data)
        if not os.path.exists('data'):
            os.makedirs('data')
        df.to_csv('data/raw_tweets.csv', index=False)
        print(f"Saved {len(df)} REAL tweets from Nitter.")
    else:
        print("All Nitter instances failed.")
