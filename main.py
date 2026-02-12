#!/usr/bin/env python3
"""
Solana Narrative Detector v2 - Main Entry Point
Sterling Rhodes - Superteam Earn Bounty Submission

Google Trends for Solana Narratives
"""

import asyncio
import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

from data_ingestion import DataIngestionOrchestrator
from narrative_engine import NarrativeAnalyzer

class SolanaNarrativeDetector:
    """Main orchestrator for the Solana Narrative Detector v2"""
    
    def __init__(self):
        self.ingestion = DataIngestionOrchestrator()
        self.analyzer = NarrativeAnalyzer()
        self.ensure_setup()
    
    def ensure_setup(self):
        """Ensure proper setup and dependencies"""
        # Create data directory
        Path("data").mkdir(exist_ok=True)
        
        print("🔧 Solana Narrative Detector v2 Setup")
        print("=" * 50)
    
    async def run_full_pipeline(self):
        """Run the complete narrative detection pipeline"""
        print("🚀 Starting Solana Narrative Detection Pipeline")
        print("=" * 50)
        
        try:
            # Step 1: Data Ingestion
            print("\n📡 STEP 1: Data Ingestion")
            print("-" * 30)
            content = await self.ingestion.ingest_all_content()
            
            if not content:
                print("❌ No content ingested. Check your bird CLI setup and internet connection.")
                return False
            
            self.ingestion.save_raw_data(content)
            print(f"✅ Ingested {len(content)} content items")
            
            # Step 2: Narrative Analysis
            print("\n🧠 STEP 2: Narrative Analysis")
            print("-" * 30)
            analysis_result = self.analyzer.analyze_content()
            
            # Save analysis results
            analysis_file = "data/narrative_analysis.json"
            with open(analysis_file, 'w') as f:
                json.dump(analysis_result, f, indent=2)
            
            print(f"✅ Analysis complete: {analysis_result['narratives_detected']} narratives detected")
            print(f"💾 Results saved to {analysis_file}")
            
            # Step 3: Generate Report
            print("\n📊 STEP 3: Generate Report")
            print("-" * 30)
            self.generate_report(analysis_result)
            
            # Step 4: Display Summary
            print("\n🎯 NARRATIVE DETECTION SUMMARY")
            print("=" * 50)
            self.display_summary(analysis_result)
            
            return True
            
        except Exception as e:
            print(f"❌ Pipeline failed: {e}")
            return False
    
    def generate_report(self, analysis_result):
        """Generate markdown report"""
        report_content = self.create_markdown_report(analysis_result)
        
        report_file = f"data/narrative_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        print(f"📝 Report generated: {report_file}")
    
    def create_markdown_report(self, analysis_result):
        """Create formatted markdown report"""
        timestamp = datetime.fromisoformat(analysis_result['analysis_timestamp']).strftime('%B %d, %Y at %H:%M')
        
        report = f"""# Solana Narrative Detection Report
*Generated on {timestamp}*

## Executive Summary

- **Total Content Analyzed**: {analysis_result['total_content_analyzed']:,} items
- **Narratives Detected**: {analysis_result['narratives_detected']}
- **Rising Narratives**: {len(analysis_result['rising_narratives'])}
- **Source Coverage**: {analysis_result['source_summary']['total_sources']} unique sources

## 🚀 Rising Narratives

"""
        
        for narrative in analysis_result['rising_narratives'][:3]:
            report += f"### {narrative['name']}\n"
            report += f"- **Momentum Score**: {narrative['momentum_score']:.1f}x\n"
            report += f"- **Frequency**: {narrative['frequency']} mentions\n"
            report += f"- **Confidence**: {narrative['confidence']:.0%}\n\n"
        
        report += "## 📊 All Detected Narratives\n\n"
        
        for i, narrative in enumerate(analysis_result['narratives'], 1):
            report += f"### {i}. {narrative['name']}\n\n"
            report += f"**Confidence**: {narrative['confidence']:.0%} | **Frequency**: {narrative['frequency']} mentions | **Trend**: {narrative['momentum']}\n\n"
            
            report += f"**Keywords**: {', '.join(narrative['keywords'][:5])}\n\n"
            
            if narrative['sample_content']:
                report += "**Sample Content**:\n"
                for content in narrative['sample_content'][:2]:
                    report += f"> {content}\n\n"
            
            report += "---\n\n"
        
        report += f"""## 📱 Source Breakdown

"""
        
        for source, count in analysis_result['source_summary']['source_breakdown'].items():
            percentage = (count / analysis_result['total_content_analyzed']) * 100
            report += f"- **{source.title()}**: {count} items ({percentage:.1f}%)\n"
        
        report += f"""

## 🏆 Top Contributing Accounts

"""
        
        for account, count in analysis_result['source_summary']['top_accounts'][:5]:
            report += f"- **@{account}**: {count} items\n"
        
        report += f"""

---
*Generated by Solana Narrative Detector v2*  
*Sterling Rhodes - Superteam Earn Bounty*
"""
        
        return report
    
    def display_summary(self, analysis_result):
        """Display summary in terminal"""
        print(f"📊 Content Analyzed: {analysis_result['total_content_analyzed']:,}")
        print(f"🔍 Narratives Found: {analysis_result['narratives_detected']}")
        print(f"🚀 Rising Trends: {len(analysis_result['rising_narratives'])}")
        
        print("\n🔝 TOP NARRATIVES:")
        for i, narrative in enumerate(analysis_result['narratives'][:5], 1):
            momentum_icon = "🔺" if narrative['momentum'] == 'accelerating' else "🔻" if narrative['momentum'] == 'declining' else "▶️"
            print(f"  {i}. {narrative['name']} {momentum_icon}")
            print(f"     Confidence: {narrative['confidence']:.0%} | Mentions: {narrative['frequency']}")
        
        print("\n🚀 RISING NARRATIVES:")
        for narrative in analysis_result['rising_narratives'][:3]:
            print(f"  • {narrative['name']} ({narrative['momentum_score']:.1f}x momentum)")
    
    def start_server(self, port=8000):
        """Start the web server"""
        print(f"🌐 Starting dashboard server on port {port}...")
        print(f"📊 Dashboard: http://localhost:{port}")
        print(f"🔗 API docs: http://localhost:{port}/docs")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            subprocess.run([sys.executable, "server.py"], check=True)
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
        except subprocess.CalledProcessError as e:
            print(f"❌ Server failed to start: {e}")
    
    def check_dependencies(self):
        """Check if required tools are available"""
        print("🔍 Checking dependencies...")
        
        # Check Python packages
        required_packages = [
            'fastapi', 'uvicorn', 'scikit-learn', 'nltk', 'pandas', 'numpy'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing packages: {', '.join(missing_packages)}")
            print("📦 Run: pip install -r requirements.txt")
            return False
        
        # Check bird CLI
        try:
            result = subprocess.run(['bird', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ bird CLI found")
            else:
                print("❌ bird CLI not working properly")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ bird CLI not found - required for Twitter data")
            print("📦 Install from: https://github.com/travisbrown/bird")
            return False
        
        print("✅ All dependencies check passed")
        return True

async def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Solana Narrative Detector v2")
    parser.add_argument('action', choices=['detect', 'server', 'check'], 
                       help='Action to perform')
    parser.add_argument('--port', type=int, default=8000, 
                       help='Port for web server (default: 8000)')
    parser.add_argument('--force', action='store_true', 
                       help='Force fresh data ingestion')
    
    args = parser.parse_args()
    
    detector = SolanaNarrativeDetector()
    
    if args.action == 'check':
        detector.check_dependencies()
    
    elif args.action == 'detect':
        success = await detector.run_full_pipeline()
        if success:
            print("\n🎉 Pipeline completed successfully!")
            print("🌐 Start the dashboard with: python main.py server")
        else:
            print("\n❌ Pipeline failed")
            sys.exit(1)
    
    elif args.action == 'server':
        # Check if analysis data exists
        if not Path("data/narrative_analysis.json").exists() and not args.force:
            print("⚠️  No analysis data found. Running detection first...")
            success = await detector.run_full_pipeline()
            if not success:
                print("❌ Failed to generate initial data")
                sys.exit(1)
        
        detector.start_server(args.port)

if __name__ == "__main__":
    asyncio.run(main())