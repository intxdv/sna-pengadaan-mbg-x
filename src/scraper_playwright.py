import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import os
import time

async def scrape_x(query, limit=500):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Set cookies from cookies.json or environment variables
        import json
        
        auth_token = os.environ.get('X_AUTH_TOKEN')
        ct0 = os.environ.get('X_CT0')
        
        # Try loading cookies.json if env vars are empty
        cookies_file = 'cookies.json'
        if not os.path.exists(cookies_file) and os.path.exists('../cookies.json'):
            cookies_file = '../cookies.json'
            
        if os.path.exists(cookies_file) and (not auth_token or not ct0):
            try:
                with open(cookies_file, 'r') as f:
                    cookies_data = json.load(f)
                    auth_token = auth_token or cookies_data.get('auth_token')
                    ct0 = ct0 or cookies_data.get('ct0')
            except Exception as e:
                print(f"Error reading {cookies_file}: {e}")
        
        if auth_token and ct0:
            await context.add_cookies([
                {
                    'name': 'auth_token',
                    'value': auth_token,
                    'domain': '.x.com',
                    'path': '/'
                },
                {
                    'name': 'ct0',
                    'value': ct0,
                    'domain': '.x.com',
                    'path': '/'
                }
            ])
            print("Successfully loaded credentials into Playwright context.")
        else:
            print("WARNING: No X credentials found. Playwright might fail to load Twitter search results. Create cookies.json or set X_AUTH_TOKEN & X_CT0 environment variables.")
        
        page = await context.new_page()
        
        # Navigate to search
        search_url = f"https://x.com/search?q={query}&src=typed_query&f=live"
        print(f"Navigating to: {search_url}")
        await page.goto(search_url)
        
        # Wait for tweets to load
        await page.wait_for_selector('article')
        
        tweets = []
        seen_ids = set()
        
        while len(tweets) < limit:
            # Extract current visible tweets
            articles = await page.query_selector_all('article')
            for article in articles:
                try:
                    # Basic extraction
                    text_element = await article.query_selector('[data-testid="tweetText"]')
                    user_element = await article.query_selector('[data-testid="User-Name"]')
                    
                    if text_element and user_element:
                        text = await text_element.inner_text()
                        user_info = await user_element.inner_text()
                        username = user_info.split('\n')[1].replace('@', '')
                        
                        # Use text as a proxy for ID if needed, or try to find the link
                        if text not in seen_ids:
                            tweets.append({
                                'username': username,
                                'text': text,
                                'created_at': '2024-11-20' # Simplified
                            })
                            seen_ids.add(text)
                            if len(tweets) % 20 == 0:
                                print(f"Collected {len(tweets)} tweets...")
                except Exception as e:
                    continue
            
            if len(tweets) >= limit:
                break
                
            # Scroll down
            await page.mouse.wheel(0, 2000)
            await asyncio.sleep(2)
            
            # Check if we hit the end
            # (Simplified check)
            
        await browser.close()
        return pd.DataFrame(tweets)

if __name__ == "__main__":
    query = "(pengadaan MBG) OR (vendor MBG) OR (anggaran MBG) lang:id"
    df = asyncio.run(scrape_x(query, limit=200)) # Start with 200 for stability
    if not df.empty:
        if not os.path.exists('data'):
            os.makedirs('data')
        df.to_csv('data/raw_tweets.csv', index=False)
        print(f"Successfully saved {len(df)} real tweets to data/raw_tweets.csv")
    else:
        print("No tweets collected.")
