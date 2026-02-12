"""
JSON Output Generator
Formats narrative detection results into structured JSON
"""

import json
from datetime import datetime
from typing import List, Dict, Any

class JSONOutputGenerator:
    def __init__(self):
        self.output_version = "1.0.0"
    
    def generate(self, narratives: List[Dict]) -> Dict[str, Any]:
        """Generate structured JSON output from narratives"""
        
        output = {
            "metadata": {
                "version": self.output_version,
                "generated_at": datetime.now().isoformat(),
                "tool": "Solana Narrative Detection & Idea Generation Tool",
                "author": "Sterling Rhodes",
                "bounty": "Superteam Earn - $3,500 Prize Pool",
                "total_narratives": len(narratives)
            },
            "summary": self._generate_summary(narratives),
            "narratives": self._format_narratives(narratives),
            "insights": self._generate_insights(narratives)
        }
        
        return output
    
    def _generate_summary(self, narratives: List[Dict]) -> Dict[str, Any]:
        """Generate executive summary of detected narratives"""
        if not narratives:
            return {
                "status": "No narratives detected",
                "top_trend": None,
                "momentum_distribution": {}
            }
        
        # Find top narrative by momentum
        top_narrative = max(narratives, key=lambda x: x['momentum_score'])
        
        # Momentum trend distribution
        momentum_counts = {}
        for narrative in narratives:
            trend = narrative['momentum_trend']
            momentum_counts[trend] = momentum_counts.get(trend, 0) + 1
        
        # Calculate average confidence
        avg_confidence = sum(n['confidence'] for n in narratives) / len(narratives)
        
        return {
            "status": f"{len(narratives)} narratives detected",
            "top_trend": {
                "name": top_narrative['name'],
                "momentum_score": top_narrative['momentum_score'],
                "confidence": top_narrative['confidence']
            },
            "momentum_distribution": momentum_counts,
            "average_confidence": round(avg_confidence, 3),
            "signal_sources": self._get_unique_sources(narratives)
        }
    
    def _format_narratives(self, narratives: List[Dict]) -> List[Dict[str, Any]]:
        """Format narratives for JSON output"""
        formatted = []
        
        for i, narrative in enumerate(narratives, 1):
            formatted_narrative = {
                "rank": i,
                "name": narrative['name'],
                "description": narrative['description'],
                "confidence": narrative['confidence'],
                "momentum": {
                    "score": narrative['momentum_score'],
                    "trend": narrative['momentum_trend'],
                    "explanation": self._explain_momentum(narrative)
                },
                "signals": {
                    "count": narrative['signal_count'],
                    "sources": narrative['sources'],
                    "top_signals": narrative['top_signals'][:3],  # Top 3 only for readability
                    "diversity_score": len(set(narrative['sources']))
                },
                "product_ideas": narrative.get('ideas', []),
                "timestamps": {
                    "detected_at": narrative['timestamp'],
                    "signal_timespan": narrative['metadata'].get('time_span', {})
                },
                "technical_details": {
                    "signal_types": dict(narrative['metadata']['signal_types']),
                    "average_signal_strength": round(narrative['metadata']['avg_strength'], 3)
                }
            }
            
            formatted.append(formatted_narrative)
        
        return formatted
    
    def _generate_insights(self, narratives: List[Dict]) -> Dict[str, Any]:
        """Generate insights and recommendations from the data"""
        if not narratives:
            return {"recommendations": []}
        
        insights = {
            "key_observations": [],
            "recommendations": [],
            "market_opportunities": [],
            "risk_factors": []
        }
        
        # Key observations
        accelerating_narratives = [n for n in narratives if n['momentum_trend'] == 'accelerating']
        if accelerating_narratives:
            insights["key_observations"].append(
                f"{len(accelerating_narratives)} narratives showing strong acceleration"
            )
        
        high_confidence = [n for n in narratives if n['confidence'] > 0.8]
        if high_confidence:
            insights["key_observations"].append(
                f"{len(high_confidence)} narratives with high confidence (>0.8)"
            )
        
        # Recommendations
        if accelerating_narratives:
            top_accelerating = max(accelerating_narratives, key=lambda x: x['momentum_score'])
            insights["recommendations"].append(
                f"Prioritize development in '{top_accelerating['name']}' - showing strongest momentum"
            )
        
        # Check for emerging patterns
        if len(narratives) > 3:
            insights["recommendations"].append(
                "Multiple narratives detected - consider cross-narrative opportunities"
            )
        
        # Market opportunities
        for narrative in narratives[:3]:  # Top 3 narratives
            if narrative['confidence'] > 0.7:
                insights["market_opportunities"].append({
                    "narrative": narrative['name'],
                    "opportunity": f"First-mover advantage in {narrative['name'].lower()}",
                    "confidence": narrative['confidence']
                })
        
        # Risk factors
        declining_narratives = [n for n in narratives if n['momentum_trend'] == 'declining']
        if declining_narratives:
            insights["risk_factors"].append(
                f"{len(declining_narratives)} narratives showing declining momentum"
            )
        
        low_diversity = [n for n in narratives if len(n['sources']) < 2]
        if low_diversity:
            insights["risk_factors"].append(
                f"{len(low_diversity)} narratives based on limited signal sources"
            )
        
        return insights
    
    def _explain_momentum(self, narrative: Dict) -> str:
        """Generate human-readable momentum explanation"""
        score = narrative['momentum_score']
        trend = narrative['momentum_trend']
        signal_count = narrative['signal_count']
        
        if score > 0.8:
            intensity = "Very strong"
        elif score > 0.6:
            intensity = "Strong"
        elif score > 0.4:
            intensity = "Moderate"
        else:
            intensity = "Weak"
        
        explanation = f"{intensity} momentum ({score:.2f}) with {signal_count} supporting signals. "
        
        if trend == "accelerating":
            explanation += "Recent signals show increasing strength."
        elif trend == "declining":
            explanation += "Recent signals show weakening strength."
        else:
            explanation += "Maintaining steady signal strength."
        
        return explanation
    
    def _get_unique_sources(self, narratives: List[Dict]) -> List[str]:
        """Get list of all unique signal sources"""
        all_sources = set()
        for narrative in narratives:
            all_sources.update(narrative['sources'])
        return sorted(list(all_sources))
    
    def save_to_file(self, data: Dict[str, Any], filepath: str) -> None:
        """Save JSON data to file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def format_as_markdown(self, data: Dict[str, Any]) -> str:
        """Convert JSON data to markdown report"""
        md = []
        
        # Header
        md.append("# Solana Ecosystem Narrative Report")
        md.append(f"*Generated on {data['metadata']['generated_at']}*")
        md.append("")
        
        # Summary
        summary = data['summary']
        md.append("## Executive Summary")
        md.append(f"**Status:** {summary['status']}")
        
        if summary['top_trend']:
            top = summary['top_trend']
            md.append(f"**Leading Narrative:** {top['name']} (momentum: {top['momentum_score']}, confidence: {top['confidence']})")
        
        md.append(f"**Average Confidence:** {summary['average_confidence']}")
        md.append("")
        
        # Narratives
        md.append("## Detected Narratives")
        md.append("")
        
        for narrative in data['narratives']:
            md.append(f"### {narrative['rank']}. {narrative['name']}")
            md.append(f"**Confidence:** {narrative['confidence']}")
            md.append(f"**Momentum:** {narrative['momentum']['score']} ({narrative['momentum']['trend']})")
            md.append(f"**Description:** {narrative['description']}")
            md.append("")
            
            # Product Ideas
            md.append("**Product Ideas:**")
            for idea in narrative['product_ideas']:
                md.append(f"- {idea}")
            md.append("")
            
            # Top Signals  
            md.append("**Key Signals:**")
            for signal in narrative['signals']['top_signals']:
                md.append(f"- {signal}")
            md.append("")
        
        # Insights
        if data['insights']['recommendations']:
            md.append("## Recommendations")
            for rec in data['insights']['recommendations']:
                md.append(f"- {rec}")
            md.append("")
        
        return "\n".join(md)