"""
Narrative Detector
Clusters signals into coherent narratives and scores their momentum
"""

import re
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from typing import List, Dict, Set
import math

class NarrativeDetector:
    def __init__(self):
        self.narrative_keywords = {
            "AI & Automation": [
                "ai", "artificial intelligence", "agent", "automation", "bot", 
                "machine learning", "neural", "gpt", "llm", "autonomous"
            ],
            "DeFi Evolution": [
                "defi", "yield", "staking", "liquidity", "amm", "dex", 
                "lending", "borrowing", "derivatives", "perps", "swap"
            ],
            "NFT & Digital Assets": [
                "nft", "collection", "art", "pfp", "digital asset", "metadata",
                "royalty", "mint", "drop", "creator"
            ],
            "Gaming & Metaverse": [
                "gaming", "game", "metaverse", "virtual", "avatar", "item",
                "play to earn", "p2e", "guild", "tournament"
            ],
            "Memecoins & Culture": [
                "memecoin", "meme", "pump", "fun", "viral", "community",
                "shitcoin", "ape", "diamond hands", "moon"
            ],
            "Infrastructure": [
                "rpc", "node", "validator", "infrastructure", "scaling",
                "performance", "bandwidth", "latency", "throughput"
            ],
            "Mobile & Payments": [
                "mobile", "wallet", "payment", "pay", "saga", "phone",
                "mainstream", "adoption", "commerce", "merchant"
            ],
            "Cross-Chain & Bridges": [
                "bridge", "cross-chain", "multichain", "interoperability",
                "ethereum", "polygon", "arbitrum", "wormhole"
            ]
        }
        
    def detect(self, signals: List[Dict]) -> List[Dict]:
        """Detect narratives from aggregated signals"""
        if not signals:
            return []
        
        # Cluster signals by narrative
        narrative_clusters = self._cluster_signals(signals)
        
        # Score and rank narratives
        narratives = []
        for narrative_name, clustered_signals in narrative_clusters.items():
            narrative = self._create_narrative(narrative_name, clustered_signals)
            narratives.append(narrative)
        
        # Sort by momentum score
        narratives.sort(key=lambda x: x['momentum_score'], reverse=True)
        
        return narratives
    
    def _cluster_signals(self, signals: List[Dict]) -> Dict[str, List[Dict]]:
        """Cluster signals into narrative categories"""
        clusters = defaultdict(list)
        unmatched_signals = []
        
        for signal in signals:
            signal_text = signal['signal'].lower()
            matched = False
            
            # Try to match to existing narrative keywords
            for narrative, keywords in self.narrative_keywords.items():
                if any(keyword in signal_text for keyword in keywords):
                    clusters[narrative].append(signal)
                    matched = True
                    break
            
            if not matched:
                unmatched_signals.append(signal)
        
        # Try to create new narratives from unmatched signals
        new_narratives = self._discover_new_narratives(unmatched_signals)
        clusters.update(new_narratives)
        
        # Filter out narratives with too few signals
        return {name: signals for name, signals in clusters.items() 
                if len(signals) >= 2}
    
    def _discover_new_narratives(self, signals: List[Dict]) -> Dict[str, List[Dict]]:
        """Discover new narratives from unmatched signals"""
        if len(signals) < 3:
            return {}
        
        # Extract keywords from signals
        all_keywords = []
        for signal in signals:
            keywords = self._extract_keywords(signal['signal'])
            all_keywords.extend(keywords)
        
        # Find most common keywords
        keyword_counts = Counter(all_keywords)
        common_keywords = [kw for kw, count in keyword_counts.most_common(10) 
                          if count >= 2]
        
        if not common_keywords:
            return {}
        
        # Group signals by common keywords
        new_clusters = defaultdict(list)
        for signal in signals:
            signal_text = signal['signal'].lower()
            for keyword in common_keywords:
                if keyword in signal_text:
                    narrative_name = f"Emerging: {keyword.title()}"
                    new_clusters[narrative_name].append(signal)
                    break
        
        return dict(new_clusters)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        # Clean text
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Filter out common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'will', 'would', 'could', 'should', 'may', 'might',
            'this', 'that', 'these', 'those', 'from', 'up', 'down', 'over', 'under'
        }
        
        keywords = [word for word in words 
                   if len(word) > 3 and word not in stop_words]
        
        return keywords
    
    def _create_narrative(self, name: str, signals: List[Dict]) -> Dict:
        """Create narrative summary from clustered signals"""
        
        # Calculate momentum score
        momentum_score = self._calculate_momentum(signals)
        
        # Determine momentum trend
        momentum_trend = self._determine_trend(signals)
        
        # Extract top signals
        top_signals = sorted(signals, key=lambda x: x['strength'], reverse=True)[:5]
        
        # Generate narrative description
        description = self._generate_description(name, signals)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(signals)
        
        return {
            'name': name,
            'description': description,
            'momentum_score': momentum_score,
            'momentum_trend': momentum_trend,
            'confidence': confidence,
            'signal_count': len(signals),
            'top_signals': [s['signal'] for s in top_signals],
            'sources': list(set(s['source'] for s in signals)),
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'signal_types': Counter(s['type'] for s in signals),
                'avg_strength': sum(s['strength'] for s in signals) / len(signals),
                'time_span': self._calculate_time_span(signals)
            }
        }
    
    def _calculate_momentum(self, signals: List[Dict]) -> float:
        """Calculate momentum score for a narrative"""
        if not signals:
            return 0.0
        
        # Factors: signal count, strength, recency, source diversity
        signal_count_score = min(len(signals) / 10, 1.0)
        avg_strength = sum(s['strength'] for s in signals) / len(signals)
        
        # Recency bonus - more recent signals get higher weight
        now = datetime.now()
        recency_scores = []
        
        for signal in signals:
            try:
                signal_time = datetime.fromisoformat(signal['timestamp'].replace('Z', ''))
                hours_ago = (now - signal_time).total_seconds() / 3600
                recency_score = max(0, 1 - (hours_ago / 168))  # Decay over 1 week
                recency_scores.append(recency_score)
            except:
                recency_scores.append(0.5)  # Default if timestamp parsing fails
        
        avg_recency = sum(recency_scores) / len(recency_scores)
        
        # Source diversity bonus
        unique_sources = len(set(s['source'] for s in signals))
        diversity_bonus = min(unique_sources / 3, 1.0)
        
        # Combined momentum score
        momentum = (signal_count_score * 0.3 + 
                   avg_strength * 0.4 + 
                   avg_recency * 0.2 + 
                   diversity_bonus * 0.1)
        
        return round(momentum, 3)
    
    def _determine_trend(self, signals: List[Dict]) -> str:
        """Determine if narrative is accelerating, stable, or declining"""
        if len(signals) < 3:
            return "emerging"
        
        # Sort signals by timestamp
        try:
            sorted_signals = sorted(signals, 
                key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '')))
        except:
            return "stable"
        
        # Split into early and recent halves
        mid_point = len(sorted_signals) // 2
        early_signals = sorted_signals[:mid_point]
        recent_signals = sorted_signals[mid_point:]
        
        early_avg_strength = sum(s['strength'] for s in early_signals) / len(early_signals)
        recent_avg_strength = sum(s['strength'] for s in recent_signals) / len(recent_signals)
        
        strength_ratio = recent_avg_strength / early_avg_strength if early_avg_strength > 0 else 1
        
        if strength_ratio > 1.2:
            return "accelerating"
        elif strength_ratio < 0.8:
            return "declining" 
        else:
            return "stable"
    
    def _calculate_confidence(self, signals: List[Dict]) -> float:
        """Calculate confidence score for narrative detection"""
        
        # More signals = higher confidence
        signal_count_factor = min(len(signals) / 5, 1.0)
        
        # Higher average strength = higher confidence 
        avg_strength = sum(s['strength'] for s in signals) / len(signals)
        
        # Multiple source types = higher confidence
        source_types = set(s['source'] for s in signals)
        source_diversity = min(len(source_types) / 3, 1.0)
        
        # Combine factors
        confidence = (signal_count_factor * 0.4 + 
                     avg_strength * 0.4 + 
                     source_diversity * 0.2)
        
        return round(confidence, 3)
    
    def _generate_description(self, name: str, signals: List[Dict]) -> str:
        """Generate a narrative description"""
        signal_count = len(signals)
        sources = set(s['source'] for s in signals)
        
        # Extract key themes from signals
        all_text = ' '.join(s['signal'] for s in signals[:5])
        keywords = self._extract_keywords(all_text)
        top_keywords = Counter(keywords).most_common(3)
        
        theme_text = ', '.join([kw for kw, _ in top_keywords])
        
        description = (f"Emerging narrative detected from {signal_count} signals across "
                      f"{len(sources)} sources. Key themes include: {theme_text}.")
        
        return description
    
    def _calculate_time_span(self, signals: List[Dict]) -> Dict:
        """Calculate time span of signals"""
        try:
            timestamps = []
            for signal in signals:
                ts = datetime.fromisoformat(signal['timestamp'].replace('Z', ''))
                timestamps.append(ts)
            
            if timestamps:
                earliest = min(timestamps)
                latest = max(timestamps)
                span_hours = (latest - earliest).total_seconds() / 3600
                
                return {
                    'earliest': earliest.isoformat(),
                    'latest': latest.isoformat(), 
                    'span_hours': round(span_hours, 1)
                }
        except:
            pass
        
        return {'span_hours': 0}