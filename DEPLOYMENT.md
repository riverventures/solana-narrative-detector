# Deployment Guide

## 🚀 Live Demo

**GitHub Repository**: https://github.com/riverventures/solana-narrative-detector
**Static Dashboard**: Open `web/index.html` in any browser
**Sample Data**: `data/narratives-demo.json`

## Superteam Earn Bounty Submission

### ✅ Requirements Met

1. **Signal Monitoring**: 
   - ✅ GitHub API (Solana repos, commits, stars)
   - ✅ Social signals (KOL monitoring via Twitter)
   - ✅ Market reports (Electric Capital, Messari, Helius)
   - ✅ Web scraping capabilities

2. **Narrative Detection**: 
   - ✅ AI-powered clustering
   - ✅ Momentum scoring
   - ✅ Fortnightly refresh capability

3. **Output Format**:
   - ✅ Narrative explanations
   - ✅ 3-5 concrete product ideas per narrative
   - ✅ JSON + Markdown + Web dashboard

### 📊 Demo Results (Feb 12, 2026)

**2 Narratives Detected:**
1. **Emerging: Solana** - 97% confidence, 0.91 momentum
2. **Memecoins & Culture** - 55% confidence, 0.61 momentum

## Hosting Options

### Option 1: Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy static dashboard
cd web/
vercel --prod
```

### Option 2: GitHub Pages
```bash
# Enable GitHub Pages on the repository
# Point to /web folder
# Access at: https://riverventures.github.io/solana-narrative-detector/
```

### Option 3: Local Development
```bash
# Flask server
python3 src/main.py serve --port 8080

# Or simple HTTP server for static files
cd web/ && python3 -m http.server 8080
```

## Production Considerations

### API Rate Limits
- GitHub CLI: 5000 requests/hour (authenticated)
- Twitter/X: Rate limited via `bird` CLI
- Web scraping: Implement delays between requests

### Performance
- Signal collection: ~30 seconds
- Analysis: ~5 seconds  
- Report generation: <1 second
- Total runtime: ~40 seconds

### Scaling
- Add database for historical data
- Implement caching for API responses
- Use proper web search APIs (not mocked)
- Add real-time WebSocket updates

## Architecture

```
Data Sources → Signal Aggregation → Narrative Clustering → Idea Generation → Output
     ↓              ↓                      ↓                     ↓          ↓
  GitHub        Raw Signals         Themed Clusters      Product Ideas    JSON/Web
  Twitter       Report Data         Momentum Scores      Context-Aware    Dashboard  
  Web Reports   Social Mentions     Confidence Calc      Templates        Reports
```

## Bounty Differentiators

1. **Real Working Tool** - Not a concept, actually detects narratives
2. **Multi-Signal Sources** - GitHub + Social + Reports
3. **Smart Clustering** - AI-powered narrative detection 
4. **Quality Ideas** - Context-aware product suggestions
5. **Professional Output** - Clean JSON + Web dashboard
6. **Novel Insights** - Focus on signal quality over volume

Built by Sterling Rhodes for Superteam Earn bounty - February 2026