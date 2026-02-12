#!/usr/bin/env python3
"""
Solana Narrative Detection Engine
Uses NLP clustering to extract semantic themes and track frequency over time
"""

import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

@dataclass
class Narrative:
    """A detected narrative with metadata"""
    name: str
    keywords: List[str]
    confidence: float
    frequency: int
    momentum: str  # 'accelerating', 'steady', 'declining'
    source_breakdown: Dict[str, int]
    sample_content: List[str]
    timespan_data: List[Dict]  # Time-series data points

class NarrativeDetector:
    """Core narrative detection engine using NLP clustering"""
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        
        # Add Solana-specific stop words
        self.stop_words.update([
            'solana', 'sol', 'blockchain', 'crypto', 'cryptocurrency',
            'tweet', 'twitter', 'says', 'said', 'new', 'just', 'today',
            'https', 'http', 'www', 'com', 't', 'co'
        ])
        
        # Known Solana narrative keywords for validation
        self.known_narratives = {
            'autonomous_agents': ['agent', 'autonomous', 'ai', 'bot', 'automation', 'hackathon', 'superteam', 'earn'],
            'payments_stablecoins': ['payment', 'stablecoin', 'usdc', 'contra', 'volume', 'transaction', 'transfer'],
            'rwa_tokenization': ['rwa', 'real world asset', 'tokenization', 'institutional', 'visa', 'catherine gu'],
            'consumer_crypto': ['consumer', 'mobile', 'wallet', 'consumer day', 'app', 'user', 'experience'],
            'defi_yield': ['defi', 'yield', 'farming', 'liquidity', 'jupiter', 'raydium', 'drift'],
            'memecoins': ['memecoin', 'meme', 'pump', 'fun', 'bonk', 'wen', 'culture'],
            'nft_gaming': ['nft', 'game', 'gaming', 'metaverse', 'collection', 'play']
        }
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs, mentions, hashtags
        text = re.sub(r'http\S+|@\w+|#\w+', '', text)
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Tokenize and remove stop words
        tokens = word_tokenize(text)
        tokens = [self.stemmer.stem(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)
    
    def extract_narratives_from_content(self, content_items: List[Dict]) -> List[Narrative]:
        """Extract narratives using NLP clustering"""
        if not content_items:
            return []
        
        print("🧠 Starting narrative extraction...")
        
        # Preprocess all content
        processed_texts = []
        for item in content_items:
            processed = self.preprocess_text(item['content'])
            if len(processed.split()) >= 3:  # Filter very short texts
                processed_texts.append(processed)
        
        if len(processed_texts) < 5:
            print("❌ Not enough content for clustering")
            return self._fallback_narrative_detection(content_items)
        
        # Vectorize text using TF-IDF
        print(f"📊 Vectorizing {len(processed_texts)} content items...")
        vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        
        tfidf_matrix = vectorizer.fit_transform(processed_texts)
        feature_names = vectorizer.get_feature_names_out()
        
        # Perform clustering
        print("🔍 Performing DBSCAN clustering...")
        clustering = DBSCAN(eps=0.3, min_samples=3, metric='cosine')
        cluster_labels = clustering.fit_predict(tfidf_matrix)
        
        # Extract narratives from clusters
        narratives = self._extract_narratives_from_clusters(
            cluster_labels, tfidf_matrix, feature_names, content_items, processed_texts
        )
        
        # Add time-series data
        narratives = self._add_timespan_data(narratives, content_items)
        
        print(f"✅ Detected {len(narratives)} narratives")
        return narratives
    
    def _extract_narratives_from_clusters(self, cluster_labels, tfidf_matrix, feature_names, content_items, processed_texts):
        """Extract meaningful narratives from clusters"""
        narratives = []
        unique_clusters = set(cluster_labels)
        
        for cluster_id in unique_clusters:
            if cluster_id == -1:  # Skip noise cluster
                continue
            
            # Get items in this cluster
            cluster_indices = [i for i, label in enumerate(cluster_labels) if label == cluster_id]
            
            if len(cluster_indices) < 3:  # Skip small clusters
                continue
            
            # Get representative keywords
            cluster_tfidf = tfidf_matrix[cluster_indices].mean(axis=0).A1
            top_feature_indices = cluster_tfidf.argsort()[-10:][::-1]
            keywords = [feature_names[i] for i in top_feature_indices if cluster_tfidf[i] > 0.01]
            
            # Match against known narratives
            narrative_name = self._match_known_narrative(keywords)
            
            if not narrative_name:
                # Generate name from top keywords
                narrative_name = " ".join(keywords[:2]).title()
            
            # Get source breakdown
            cluster_content = [content_items[i] for i in cluster_indices]
            source_breakdown = Counter(item['source_type'] for item in cluster_content)
            
            # Sample content for display
            sample_content = [item['content'][:100] + "..." 
                            for item in cluster_content[:3]]
            
            # Calculate confidence based on cluster cohesion
            confidence = min(len(cluster_indices) / 10.0, 1.0)
            
            narrative = Narrative(
                name=narrative_name,
                keywords=keywords,
                confidence=confidence,
                frequency=len(cluster_indices),
                momentum='steady',  # Will be calculated later
                source_breakdown=dict(source_breakdown),
                sample_content=sample_content,
                timespan_data=[]  # Will be filled later
            )
            
            narratives.append(narrative)
        
        return sorted(narratives, key=lambda n: n.frequency, reverse=True)
    
    def _match_known_narrative(self, keywords: List[str]) -> str:
        """Match extracted keywords against known narratives"""
        best_match = ""
        best_score = 0
        
        for narrative_name, narrative_keywords in self.known_narratives.items():
            # Calculate overlap score
            overlap = len(set(keywords) & set(narrative_keywords))
            score = overlap / len(narrative_keywords)
            
            if score > best_score and score > 0.3:  # Minimum threshold
                best_score = score
                best_match = narrative_name.replace('_', ' ').title()
        
        return best_match
    
    def _fallback_narrative_detection(self, content_items: List[Dict]) -> List[Narrative]:
        """Fallback method when clustering fails"""
        print("📝 Using fallback keyword-based detection...")
        
        narratives = []
        all_text = " ".join(item['content'].lower() for item in content_items)
        
        for narrative_name, keywords in self.known_narratives.items():
            count = sum(all_text.count(keyword) for keyword in keywords)
            
            if count >= 3:  # Minimum mentions
                sample_content = [
                    item['content'][:100] + "..."
                    for item in content_items
                    if any(keyword in item['content'].lower() for keyword in keywords)
                ][:3]
                
                source_breakdown = Counter(
                    item['source_type'] 
                    for item in content_items 
                    if any(keyword in item['content'].lower() for keyword in keywords)
                )
                
                narrative = Narrative(
                    name=narrative_name.replace('_', ' ').title(),
                    keywords=keywords[:5],
                    confidence=min(count / 20.0, 1.0),
                    frequency=count,
                    momentum='steady',
                    source_breakdown=dict(source_breakdown),
                    sample_content=sample_content,
                    timespan_data=[]
                )
                
                narratives.append(narrative)
        
        return sorted(narratives, key=lambda n: n.frequency, reverse=True)
    
    def _add_timespan_data(self, narratives: List[Narrative], content_items: List[Dict]) -> List[Narrative]:
        """Add time-series data to narratives"""
        print("📊 Calculating time-series data...")
        
        # Create time buckets (daily for last week)
        now = datetime.now()
        time_buckets = []
        
        for i in range(7):
            bucket_date = now - timedelta(days=i)
            time_buckets.append({
                'date': bucket_date.strftime('%Y-%m-%d'),
                'timestamp': bucket_date
            })
        
        for narrative in narratives:
            timespan_data = []
            
            for bucket in time_buckets:
                # Count mentions of narrative keywords in this time bucket
                bucket_start = bucket['timestamp']
                bucket_end = bucket_start + timedelta(days=1)
                
                count = 0
                for item in content_items:
                    item_time = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00')).replace(tzinfo=None)
                    
                    if bucket_start <= item_time < bucket_end:
                        if any(keyword in item['content'].lower() for keyword in narrative.keywords):
                            count += 1
                
                timespan_data.append({
                    'date': bucket['date'],
                    'count': count
                })
            
            # Calculate momentum
            recent_count = sum(day['count'] for day in timespan_data[:3])  # Last 3 days
            older_count = sum(day['count'] for day in timespan_data[3:])   # Previous 4 days
            
            if recent_count > older_count * 1.5:
                narrative.momentum = 'accelerating'
            elif recent_count < older_count * 0.5:
                narrative.momentum = 'declining'
            else:
                narrative.momentum = 'steady'
            
            narrative.timespan_data = timespan_data
        
        return narratives

class NarrativeAnalyzer:
    """Analyze and process detected narratives"""
    
    def __init__(self):
        self.detector = NarrativeDetector()
    
    def analyze_content(self, content_file: str = "data/raw_content.json") -> Dict:
        """Main analysis pipeline"""
        print("🔍 Starting narrative analysis...")
        
        # Load content
        with open(content_file, 'r') as f:
            raw_data = json.load(f)
        
        content_items = raw_data['content']
        print(f"📚 Loaded {len(content_items)} content items")
        
        # Detect narratives
        narratives = self.detector.extract_narratives_from_content(content_items)
        
        # Create analysis report
        analysis_result = {
            'analysis_timestamp': datetime.now().isoformat(),
            'total_content_analyzed': len(content_items),
            'narratives_detected': len(narratives),
            'narratives': [asdict(narrative) for narrative in narratives],
            'source_summary': self._create_source_summary(content_items),
            'rising_narratives': self._identify_rising_narratives(narratives)
        }
        
        return analysis_result
    
    def _create_source_summary(self, content_items: List[Dict]) -> Dict:
        """Create summary of content sources"""
        source_counts = Counter(item['source_type'] for item in content_items)
        
        return {
            'total_sources': len(set(item['source_handle'] for item in content_items)),
            'source_breakdown': dict(source_counts),
            'top_accounts': list(Counter(item['source_handle'] for item in content_items).most_common(5))
        }
    
    def _identify_rising_narratives(self, narratives: List[Narrative]) -> List[Dict]:
        """Identify narratives with highest momentum"""
        rising = [
            {
                'name': n.name,
                'momentum_score': self._calculate_momentum_score(n),
                'frequency': n.frequency,
                'confidence': n.confidence
            }
            for n in narratives 
            if n.momentum == 'accelerating'
        ]
        
        return sorted(rising, key=lambda x: x['momentum_score'], reverse=True)[:5]
    
    def _calculate_momentum_score(self, narrative: Narrative) -> float:
        """Calculate numerical momentum score"""
        if not narrative.timespan_data:
            return 0.0
        
        recent_days = narrative.timespan_data[:3]
        older_days = narrative.timespan_data[3:]
        
        recent_avg = sum(day['count'] for day in recent_days) / len(recent_days)
        older_avg = sum(day['count'] for day in older_days) / len(older_days) if older_days else 1
        
        return (recent_avg / max(older_avg, 1)) * narrative.confidence

if __name__ == "__main__":
    analyzer = NarrativeAnalyzer()
    results = analyzer.analyze_content()
    
    # Save results
    with open("data/narrative_analysis.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Analysis complete. Found {results['narratives_detected']} narratives")
    print("💾 Results saved to data/narrative_analysis.json")