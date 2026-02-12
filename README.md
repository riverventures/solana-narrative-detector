# Solana Narrative Detection & Idea Generation Tool

🏆 **Superteam Earn Bounty Submission** - $3,500 Prize Pool

A real-time tool that monitors the Solana ecosystem to detect emerging narratives and generate concrete product ideas.

## Features

- 📈 **Signal Monitoring**: GitHub trends, KOL activity, onchain data, market reports
- 🧠 **Narrative Detection**: AI-powered clustering and momentum scoring
- 💡 **Idea Generation**: 3-5 concrete product ideas per detected narrative
- 🌐 **Web Dashboard**: Simple, clean interface for exploring results
- 📊 **Data Export**: JSON and markdown reports

## Architecture

```
Raw Signals → Aggregation → Clustering → Scoring → Ideas → Output
```

## Data Sources

- **GitHub**: Trending Solana repositories and developer activity
- **Social**: KOL monitoring (Mert, Akshay, Toly) via Twitter API
- **Reports**: Electric Capital, Messari, Helius research
- **Onchain**: Solana program activity and usage metrics

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run narrative detection
python src/main.py detect

# Start web dashboard
python src/main.py serve
```

## Output Example

```json
{
  "narratives": [
    {
      "name": "AI Agent Trading",
      "confidence": 0.87,
      "momentum": "accelerating",
      "signals": ["GitHub: +45% Solana AI repos", "Twitter: Mert mentions 'agent trading'"],
      "ideas": [
        "Agent-to-agent DEX for autonomous trading",
        "AI portfolio manager using Jupiter aggregation",
        "Sentiment-driven trading bot marketplace"
      ]
    }
  ]
}
```

Built by Sterling Rhodes for Superteam Earn bounty.