"""
Social Signals Fetcher
Monitors KOL activity and social sentiment around Solana ecosystem
"""

import asyncio
import subprocess
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict

class SocialSignalFetcher:
    def __init__(self):
        self.kols = [
            "mertmumtaz",  # Mert
            "aeyakovenko",  # Toly (Anatoly)
            "rajgokal",     # Raj  
            "steveluscher", # Steve
            "armaniferrante", # Armani
            "jstrry",       # Jstrry
            "0xMert_"       # Alt Mert account
        ]
        
    async def fetch(self) -> List[Dict]:
        """Fetch social signals from KOLs and general Solana chatter"""
        signals = []
        
        # Fetch KOL tweets
        signals.extend(await self._fetch_kol_tweets())
        
        # Search for trending Solana topics
        signals.extend(await self._search_solana_trends())
        
        return signals
    
    async def _fetch_kol_tweets(self) -> List[Dict]:
        """Fetch recent tweets from key Solana KOLs"""
        signals = []
        
        for handle in self.kols:
            try:
                # Get recent tweets from this user (last 3 days)
                cmd = f'bird user-tweets {handle} --json --limit 10'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    tweets_data = json.loads(result.stdout)
                    
                    for tweet in tweets_data.get('tweets', []):
                        # Filter for recent tweets (last 3 days)
                        tweet_date = datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00'))
                        if (datetime.now() - tweet_date.replace(tzinfo=None)).days <= 3:
                            # Extract signal from tweet content
                            signal_text = self._extract_signal_from_tweet(tweet['text'], handle)
                            if signal_text:
                                signals.append({
                                    'type': 'social_kol',
                                    'source': 'twitter',
                                    'timestamp': tweet['created_at'],
                                    'signal': signal_text,
                                    'metadata': {
                                        'handle': handle,
                                        'tweet_id': tweet['id'],
                                        'engagement': tweet.get('public_metrics', {})
                                    },
                                    'strength': self._calculate_tweet_strength(tweet, handle)
                                })
            except Exception as e:
                print(f"Error fetching tweets for {handle}: {e}")
                continue
        
        return signals
    
    async def _search_solana_trends(self) -> List[Dict]:
        """Search for trending Solana-related content"""
        signals = []
        
        search_terms = [
            "solana defi",
            "solana memecoin", 
            "solana nft",
            "solana ai",
            "solana gaming",
            "pump.fun",
            "jupiter exchange",
            "raydium",
            "drift protocol"
        ]
        
        for term in search_terms:
            try:
                # Search for recent mentions
                cmd = f'bird search "{term}" --json --limit 5'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    search_data = json.loads(result.stdout)
                    
                    for tweet in search_data.get('tweets', []):
                        # Only include tweets from last 24 hours
                        tweet_date = datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00'))
                        if (datetime.now() - tweet_date.replace(tzinfo=None)).hours <= 24:
                            signals.append({
                                'type': 'social_trend',
                                'source': 'twitter',
                                'timestamp': tweet['created_at'],
                                'signal': f"Trending: {term} - {tweet['text'][:100]}...",
                                'metadata': {
                                    'search_term': term,
                                    'tweet_id': tweet['id'],
                                    'author': tweet.get('author', {}).get('username', 'unknown')
                                },
                                'strength': self._calculate_trend_strength(tweet, term)
                            })
            except Exception as e:
                print(f"Error searching for {term}: {e}")
                continue
        
        return signals
    
    def _extract_signal_from_tweet(self, text: str, handle: str) -> str:
        """Extract meaningful signals from tweet content"""
        text_lower = text.lower()
        
        # Look for key narrative indicators
        narrative_keywords = [
            'ai', 'artificial intelligence', 'agent', 'bot',
            'defi', 'yield', 'staking', 'liquidity',
            'nft', 'collection', 'art', 'pfp',
            'gaming', 'game', 'metaverse',
            'memecoin', 'meme', 'pump',
            'bridge', 'cross-chain', 'multichain',
            'mobile', 'wallet', 'payments'
        ]
        
        found_keywords = [kw for kw in narrative_keywords if kw in text_lower]
        
        if found_keywords:
            return f"{handle}: mentions {', '.join(found_keywords[:3])}"
        
        # Look for excitement indicators
        excitement_indicators = ['🔥', '🚀', '💎', '⚡', 'bullish', 'massive', 'huge', 'incredible']
        if any(indicator in text_lower for indicator in excitement_indicators):
            return f"{handle}: excited about Solana development"
        
        return None
    
    def _calculate_tweet_strength(self, tweet: Dict, handle: str) -> float:
        """Calculate signal strength based on engagement and KOL influence"""
        metrics = tweet.get('public_metrics', {})
        
        # Base strength from KOL influence
        kol_weights = {
            'mertmumtaz': 1.0,
            'aeyakovenko': 1.0, 
            'rajgokal': 0.9,
            'steveluscher': 0.8,
            'armaniferrante': 0.8,
            'jstrry': 0.7,
            '0xMert_': 0.9
        }
        
        base_strength = kol_weights.get(handle, 0.5)
        
        # Engagement multiplier
        likes = metrics.get('like_count', 0)
        retweets = metrics.get('retweet_count', 0)
        replies = metrics.get('reply_count', 0)
        
        engagement_score = (likes + retweets * 3 + replies * 2) / 1000
        engagement_multiplier = min(engagement_score, 2.0)
        
        return min(base_strength * (1 + engagement_multiplier), 1.0)
    
    def _calculate_trend_strength(self, tweet: Dict, term: str) -> float:
        """Calculate strength of trending signal"""
        metrics = tweet.get('public_metrics', {})
        
        # Higher engagement = stronger signal
        total_engagement = (
            metrics.get('like_count', 0) + 
            metrics.get('retweet_count', 0) * 2 + 
            metrics.get('reply_count', 0)
        )
        
        # Normalize to 0-1 scale
        return min(total_engagement / 500, 1.0)