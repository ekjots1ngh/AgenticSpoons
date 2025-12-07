"""
Real-time news feed aggregator
Like Bloomberg News Terminal
"""
import feedparser
import requests
from datetime import datetime, timedelta
import json
from collections import defaultdict

class NewsAggregator:
    """
    Aggregate crypto news from multiple sources
    Filter and rank by relevance
    """
    
    def __init__(self):
        self.feeds = {
            'CoinDesk': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
            'CoinTelegraph': 'https://cointelegraph.com/rss',
            'Decrypt': 'https://decrypt.co/feed',
            'TheBlock': 'https://www.theblockcrypto.com/rss.xml',
        }
        
        self.keywords = ['neo', 'volatility', 'options', 'defi', 'oracle', 'derivatives']
        
    def fetch_news(self, hours=24):
        """Fetch news from all sources"""
        
        all_articles = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for source, feed_url in self.feeds.items():
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:20]:  # Limit to 20 per source
                    # Parse published time
                    pub_time = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()
                    
                    if pub_time > cutoff_time:
                        article = {
                            'source': source,
                            'title': entry.title,
                            'link': entry.link,
                            'published': pub_time.isoformat(),
                            'summary': entry.get('summary', '')[:200],
                            'relevance_score': self._calculate_relevance(entry.title + ' ' + entry.get('summary', ''))
                        }
                        all_articles.append(article)
                
                print(f"OK Fetched {len([a for a in all_articles if a['source'] == source])} articles from {source}")
                
            except Exception as e:
                print(f"Error fetching from {source}: {e}")
        
        # Sort by relevance and time
        all_articles.sort(key=lambda x: (x['relevance_score'], x['published']), reverse=True)
        
        return all_articles
    
    def _calculate_relevance(self, text):
        """Calculate relevance score based on keywords"""
        text_lower = text.lower()
        score = 0
        
        for keyword in self.keywords:
            if keyword in text_lower:
                score += 1
                if keyword in ['neo', 'volatility', 'oracle']:
                    score += 2  # Boost for key topics
        
        return score
    
    def get_top_headlines(self, limit=10):
        """Get top headlines"""
        articles = self.fetch_news(hours=24)
        return articles[:limit]
    
    def get_neo_news(self):
        """Get Neo-specific news"""
        articles = self.fetch_news(hours=48)
        neo_articles = [a for a in articles if 'neo' in a['title'].lower() or 'neo' in a['summary'].lower()]
        return neo_articles
    
    def generate_news_html(self, articles):
        """Generate HTML for news display"""
        
        html = """
        <div style="font-family: 'Courier New', monospace; background-color: #1a1a1a; color: #e0e0e0; padding: 20px;">
            <h2 style="color: #ff8c00; border-bottom: 2px solid #ff8c00; padding-bottom: 10px;">
                LATEST CRYPTO NEWS
            </h2>
        """
        
        for i, article in enumerate(articles[:15], 1):
            pub_time = datetime.fromisoformat(article['published']).strftime('%H:%M')
            
            relevance_indicator = '*' * min(article['relevance_score'], 5)
            
            html += f"""
            <div style="margin: 15px 0; padding: 15px; background-color: #2a2a2a; border-left: 3px solid #00bfff;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #ff8c00; font-weight: bold;">[{article['source']}]</span>
                    <span style="color: #666; font-size: 12px;">{pub_time} | {relevance_indicator}</span>
                </div>
                <h3 style="margin: 10px 0; color: #00bfff;">
                    <a href="{article['link']}" target="_blank" style="color: #00bfff; text-decoration: none;">
                        {article['title']}
                    </a>
                </h3>
                <p style="color: #999; font-size: 14px; margin: 5px 0;">{article['summary']}</p>
            </div>
            """
        
        html += "</div>"
        
        return html
    
    def save_to_json(self, filename='outputs/crypto_news.json'):
        """Save news to JSON file"""
        articles = self.fetch_news(hours=24)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'article_count': len(articles),
                'articles': articles
            }, f, indent=2)
        
        print(f"OK News saved to: {filename}")
        return filename

# Demo
if __name__ == "__main__":
    print("="*70)
    print("CRYPTO NEWS AGGREGATOR")
    print("="*70)
    
    aggregator = NewsAggregator()
    
    # Fetch and display top headlines
    print("\nTOP HEADLINES (Last 24 hours):\n")
    headlines = aggregator.get_top_headlines(limit=10)
    
    for i, article in enumerate(headlines, 1):
        print(f"{i}. [{article['source']}] {article['title']}")
        print(f"   Relevance: {'*' * article['relevance_score']}")
        print(f"   {article['link']}\n")
    
    # Generate HTML preview
    html = aggregator.generate_news_html(headlines)
    with open('outputs/news_feed.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("OK News feed HTML saved to: outputs/news_feed.html")
    
    # Save JSON
    aggregator.save_to_json()
    
    print("\n" + "="*70)
