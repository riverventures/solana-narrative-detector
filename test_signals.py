#!/usr/bin/env python3
"""
Quick test script to debug signal collection
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sources.github_signals import GitHubSignalFetcher
from sources.social_signals import SocialSignalFetcher 
from sources.report_signals import ReportSignalFetcher

async def test_signals():
    print("🧪 Testing signal collection...")
    
    # Test GitHub signals
    print("\n📈 Testing GitHub signals...")
    github_fetcher = GitHubSignalFetcher()
    try:
        github_signals = await github_fetcher.fetch()
        print(f"  Fetched {len(github_signals)} GitHub signals")
        for signal in github_signals[:3]:  # Show first 3
            print(f"  - {signal['signal'][:80]}...")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test Social signals (may be slow/rate-limited)
    print("\n🐦 Testing Social signals...")
    social_fetcher = SocialSignalFetcher()
    try:
        social_signals = await social_fetcher.fetch()
        print(f"  Fetched {len(social_signals)} social signals")
        for signal in social_signals[:3]:  # Show first 3
            print(f"  - {signal['signal'][:80]}...")
    except Exception as e:
        print(f"  Error: {e}")
        
    # Test Report signals
    print("\n📊 Testing Report signals...")
    report_fetcher = ReportSignalFetcher()
    try:
        report_signals = await report_fetcher.fetch()
        print(f"  Fetched {len(report_signals)} report signals")
        for signal in report_signals[:3]:  # Show first 3
            print(f"  - {signal['signal'][:80]}...")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == '__main__':
    asyncio.run(test_signals())