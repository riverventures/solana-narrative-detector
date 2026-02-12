"""
GitHub Signals Fetcher
Monitors Solana-related GitHub activity for emerging development trends
"""

import asyncio
import aiohttp
import subprocess
import json
from datetime import datetime, timedelta
from typing import List, Dict

class GitHubSignalFetcher:
    def __init__(self):
        self.base_url = "https://api.github.com"
        
    async def fetch(self) -> List[Dict]:
        """Fetch GitHub signals related to Solana ecosystem"""
        signals = []
        
        # Use GitHub CLI for authenticated requests
        signals.extend(await self._fetch_trending_repos())
        signals.extend(await self._fetch_solana_activity())
        
        return signals
    
    async def _fetch_trending_repos(self) -> List[Dict]:
        """Fetch trending Solana repositories"""
        signals = []
        
        # Search for trending Solana repos in last 7 days
        query = "solana language:rust created:>2026-02-05"
        cmd = f'gh api search/repositories -q "{query}" --jq ".items[] | {{name: .name, full_name: .full_name, stars: .stargazers_count, created_at: .created_at, description: .description}}"'
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        repo_data = json.loads(line)
                        signals.append({
                            'type': 'github_trending',
                            'source': 'github',
                            'timestamp': datetime.now().isoformat(),
                            'signal': f"New Solana repo: {repo_data['full_name']} ({repo_data['stars']} stars)",
                            'metadata': repo_data,
                            'strength': min(repo_data['stars'] / 100, 1.0)  # Normalize strength
                        })
        except Exception as e:
            print(f"Error fetching trending repos: {e}")
        
        return signals
    
    async def _fetch_solana_activity(self) -> List[Dict]:
        """Fetch activity from key Solana ecosystem repos"""
        signals = []
        
        key_repos = [
            "solana-labs/solana",
            "solana-labs/solana-program-library", 
            "coral-xyz/anchor",
            "project-serum/serum-dex",
            "metaplex-foundation/metaplex",
            "jup-ag/jupiter-core"
        ]
        
        for repo in key_repos:
            try:
                # Get recent commits (last 7 days)
                since = (datetime.now() - timedelta(days=7)).isoformat()
                cmd = f'gh api repos/{repo}/commits --field since={since} --jq "length"'
                
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    commit_count = int(result.stdout.strip())
                    if commit_count > 0:
                        signals.append({
                            'type': 'github_activity',
                            'source': 'github',
                            'timestamp': datetime.now().isoformat(),
                            'signal': f"{repo}: {commit_count} commits this week",
                            'metadata': {'repo': repo, 'commits': commit_count},
                            'strength': min(commit_count / 50, 1.0)  # Normalize
                        })
            except Exception as e:
                print(f"Error fetching activity for {repo}: {e}")
        
        return signals
    
    async def _search_repositories(self, query: str, sort: str = "updated") -> List[Dict]:
        """Search GitHub repositories with a specific query"""
        cmd = f'gh api search/repositories -q "{query}" --field sort={sort} --jq ".items[0:10]"'
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"Error searching repos: {e}")
            
        return []