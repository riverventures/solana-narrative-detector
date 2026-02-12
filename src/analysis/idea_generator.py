"""
Idea Generator
Generates 3-5 concrete product ideas for each detected narrative
"""

import random
from typing import List, Dict

class IdeaGenerator:
    def __init__(self):
        # Product idea templates for different narrative types
        self.idea_templates = {
            "AI & Automation": [
                "AI trading bot that {specific_feature} using Solana's {tech_advantage}",
                "Automated portfolio manager for {target_market} with {unique_value}",
                "AI-powered prediction market for {domain} built on Solana",
                "Smart contract automation tool for {use_case} with {benefit}",
                "AI agent marketplace where agents can {capability} autonomously"
            ],
            "DeFi Evolution": [
                "Next-gen DEX with {innovative_feature} for {target_users}",
                "Yield optimization protocol that {unique_mechanism}",
                "Cross-protocol lending platform with {advantage}",
                "Derivatives platform for {asset_type} with {risk_feature}",
                "DeFi insurance protocol covering {risk_category}"
            ],
            "NFT & Digital Assets": [
                "Dynamic NFT platform where assets {change_mechanism}",
                "Creator economy marketplace with {monetization_model}",
                "NFT utility platform for {real_world_use_case}",
                "Fractionalized asset protocol for {asset_type}",
                "NFT gaming infrastructure with {technical_feature}"
            ],
            "Gaming & Metaverse": [
                "Play-to-earn game focused on {game_genre} with {economy_model}",
                "Metaverse asset exchange for {virtual_goods}",
                "Gaming guild management platform with {unique_feature}",
                "VR-native social platform with {interaction_model}",
                "Game developer toolkit for {specific_need}"
            ],
            "Memecoins & Culture": [
                "Community-driven launchpad with {governance_feature}",
                "Meme creation platform with {monetization_method}",
                "Viral marketing tool for {target_audience}",
                "Social trading app focused on {community_aspect}",
                "Culture prediction market for {trend_category}"
            ],
            "Infrastructure": [
                "RPC optimization service with {performance_benefit}",
                "Developer analytics platform for {metrics_focus}",
                "Node-as-a-Service with {unique_offering}",
                "Solana monitoring dashboard for {user_type}",
                "Infrastructure automation tool for {specific_task}"
            ],
            "Mobile & Payments": [
                "Mobile-first wallet with {user_experience_feature}",
                "Point-of-sale solution for {merchant_type}",
                "P2P payment app with {social_feature}",
                "Merchant onboarding platform with {simplification}",
                "Mobile DeFi app for {underserved_market}"
            ],
            "Cross-Chain & Bridges": [
                "Universal bridge aggregator with {safety_feature}",
                "Cross-chain yield farming platform for {strategy_type}",
                "Multi-chain portfolio tracker with {analytics_feature}",
                "Interoperability protocol for {specific_use_case}",
                "Cross-chain governance platform with {participation_model}"
            ]
        }
        
        # Context-specific variables for templates
        self.template_variables = {
            "specific_feature": [
                "analyzes social sentiment", "tracks whale movements", "optimizes gas costs",
                "predicts market volatility", "manages risk automatically", "executes arbitrage"
            ],
            "tech_advantage": [
                "fast transaction speeds", "low fees", "high throughput", "parallel execution",
                "composable smart contracts", "mobile-first design"
            ],
            "target_market": [
                "retail investors", "institutions", "DAOs", "content creators",
                "gaming guilds", "DeFi protocols", "small businesses"
            ],
            "unique_value": [
                "zero-knowledge privacy", "social trading features", "predictive analytics",
                "community governance", "gamified experience", "educational tools"
            ],
            "innovative_feature": [
                "intent-based trading", "MEV protection", "social order books",
                "AI-powered routing", "dynamic fees", "privacy pools"
            ],
            "monetization_model": [
                "revenue sharing with fans", "subscription tiers", "usage-based pricing",
                "success fees", "freemium model", "advertising revenue"
            ],
            "game_genre": [
                "strategy", "racing", "puzzle", "adventure", "simulation",
                "battle royale", "city building", "card games"
            ],
            "performance_benefit": [
                "99.9% uptime", "50% faster responses", "auto-scaling",
                "geographic distribution", "predictive caching", "failover protection"
            ]
        }
    
    def generate_ideas(self, narrative: Dict) -> List[str]:
        """Generate 3-5 product ideas for a narrative"""
        narrative_name = narrative['name']
        
        # Handle emerging narratives
        if narrative_name.startswith("Emerging:"):
            return self._generate_emerging_ideas(narrative)
        
        # Use templates for known narrative types
        if narrative_name in self.idea_templates:
            templates = self.idea_templates[narrative_name]
            return self._fill_templates(templates, narrative)
        
        # Fallback for unknown narrative types
        return self._generate_generic_ideas(narrative)
    
    def _fill_templates(self, templates: List[str], narrative: Dict) -> List[str]:
        """Fill templates with context-appropriate variables"""
        ideas = []
        
        # Select 4-5 templates (or all if fewer)
        selected_templates = random.sample(templates, min(len(templates), 5))
        
        for template in selected_templates:
            filled_template = template
            
            # Replace each variable placeholder
            for var_name, options in self.template_variables.items():
                placeholder = f"{{{var_name}}}"
                if placeholder in template:
                    # Choose option based on narrative context
                    chosen_option = self._choose_contextual_option(
                        options, narrative, var_name
                    )
                    filled_template = filled_template.replace(placeholder, chosen_option)
            
            # Replace any remaining unreplaced placeholders with generic alternatives
            import re
            filled_template = re.sub(r'{[^}]+}', lambda m: {
                '{monetization_method}': 'subscription model',
                '{governance_feature}': 'community voting',
                '{trend_category}': 'crypto trends',
                '{community_aspect}': 'social features',
                '{target_audience}': 'retail traders'
            }.get(m.group(), 'innovative features'), filled_template)
            
            ideas.append(filled_template)
        
        return ideas
    
    def _choose_contextual_option(self, options: List[str], narrative: Dict, var_type: str) -> str:
        """Choose option that best fits the narrative context"""
        
        # Analyze narrative signals for context clues
        signals_text = ' '.join(narrative.get('top_signals', [])).lower()
        
        # Score options based on relevance to signals
        scored_options = []
        for option in options:
            score = 0
            option_words = option.lower().split()
            
            for word in option_words:
                if word in signals_text:
                    score += 1
            
            scored_options.append((option, score))
        
        # Return highest scoring option, or random if tied
        scored_options.sort(key=lambda x: x[1], reverse=True)
        top_score = scored_options[0][1]
        top_options = [opt for opt, score in scored_options if score == top_score]
        
        return random.choice(top_options)
    
    def _generate_emerging_ideas(self, narrative: Dict) -> List[str]:
        """Generate ideas for emerging narratives"""
        emerging_theme = narrative['name'].replace("Emerging: ", "")
        signals = narrative.get('top_signals', [])
        
        ideas = [
            f"{emerging_theme} analytics dashboard for Solana ecosystem tracking",
            f"Community platform focused on {emerging_theme} discussions and insights",
            f"Educational content hub about {emerging_theme} in crypto",
            f"Investment tracking tool for {emerging_theme}-related assets",
            f"API service providing {emerging_theme} data to developers"
        ]
        
        # Customize based on signals
        if any('trading' in signal.lower() for signal in signals):
            ideas.append(f"Trading bot optimized for {emerging_theme} opportunities")
        
        if any('social' in signal.lower() for signal in signals):
            ideas.append(f"Social sentiment analyzer for {emerging_theme} trends")
        
        return random.sample(ideas, min(len(ideas), 5))
    
    def _generate_generic_ideas(self, narrative: Dict) -> List[str]:
        """Generate generic product ideas when no specific templates exist"""
        narrative_name = narrative['name']
        
        generic_ideas = [
            f"Platform connecting {narrative_name} enthusiasts and builders",
            f"Analytics dashboard tracking {narrative_name} metrics",
            f"Educational resources for {narrative_name} adoption", 
            f"Developer tools for building {narrative_name} applications",
            f"Marketplace for {narrative_name}-related services"
        ]
        
        return generic_ideas
    
    def _enhance_ideas_with_context(self, ideas: List[str], narrative: Dict) -> List[str]:
        """Enhance ideas with specific context from the narrative"""
        enhanced_ideas = []
        
        # Extract context from narrative metadata
        sources = narrative.get('sources', [])
        momentum_trend = narrative.get('momentum_trend', 'stable')
        
        for idea in ideas:
            enhanced_idea = idea
            
            # Add urgency if momentum is accelerating
            if momentum_trend == "accelerating":
                enhanced_idea = f"[High Priority] {enhanced_idea}"
            
            # Add source context if relevant
            if 'github' in sources:
                enhanced_idea += " (Strong developer interest detected)"
            if 'twitter' in sources:
                enhanced_idea += " (Social momentum building)"
                
            enhanced_ideas.append(enhanced_idea)
        
        return enhanced_ideas