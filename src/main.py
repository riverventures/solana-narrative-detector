#!/usr/bin/env python3
"""
Solana Narrative Detection & Idea Generation Tool
Sterling Rhodes - Superteam Earn Bounty
"""

import click
import json
import asyncio
from datetime import datetime
from pathlib import Path

from sources.github_signals import GitHubSignalFetcher
from sources.social_signals import SocialSignalFetcher 
from sources.report_signals import ReportSignalFetcher
from analysis.narrative_detector import NarrativeDetector
from analysis.idea_generator import IdeaGenerator
from output.json_output import JSONOutputGenerator
from output.web_dashboard import WebDashboard

@click.group()
def cli():
    """Solana Narrative Detection & Idea Generation Tool"""
    pass

@cli.command()
@click.option('--output', '-o', default='data/narratives.json', help='Output file path')
@click.option('--format', '-f', default='json', type=click.Choice(['json', 'markdown']), help='Output format')
@click.option('--signals', '-s', multiple=True, default=['github', 'social', 'reports'], help='Signal sources to use')
def detect(output, format, signals):
    """Detect emerging narratives from Solana ecosystem signals"""
    click.echo("🔍 Starting Solana narrative detection...")
    
    # Run async detection
    narratives = asyncio.run(run_detection(signals))
    
    # Generate output
    output_gen = JSONOutputGenerator()
    result = output_gen.generate(narratives)
    
    # Save to file
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    click.echo(f"✅ Detected {len(narratives)} narratives → {output}")
    
    # Print summary
    for narrative in narratives[:3]:  # Top 3
        click.echo(f"📈 {narrative['name']} (confidence: {narrative['confidence']:.2f})")

@cli.command()
@click.option('--port', '-p', default=8080, help='Server port')
@click.option('--data', '-d', default='data/narratives.json', help='Data file to serve')
def serve(port, data):
    """Start web dashboard server"""
    dashboard = WebDashboard(data)
    click.echo(f"🌐 Starting dashboard at http://localhost:{port}")
    dashboard.serve(port=port)

async def run_detection(signal_types):
    """Run the full detection pipeline"""
    all_signals = []
    
    # Fetch signals from different sources
    if 'github' in signal_types:
        github_fetcher = GitHubSignalFetcher()
        github_signals = await github_fetcher.fetch()
        all_signals.extend(github_signals)
    
    if 'social' in signal_types:
        social_fetcher = SocialSignalFetcher()
        social_signals = await social_fetcher.fetch()
        all_signals.extend(social_signals)
    
    if 'reports' in signal_types:
        report_fetcher = ReportSignalFetcher()
        report_signals = await report_fetcher.fetch()
        all_signals.extend(report_signals)
    
    # Detect narratives
    detector = NarrativeDetector()
    narratives = detector.detect(all_signals)
    
    # Generate ideas for each narrative
    idea_gen = IdeaGenerator()
    for narrative in narratives:
        narrative['ideas'] = idea_gen.generate_ideas(narrative)
    
    return narratives

if __name__ == '__main__':
    cli()