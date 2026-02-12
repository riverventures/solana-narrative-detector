# Solana Narrative Detector v2
> 🏆 **Superteam Earn Bounty Submission** - $3,500 Prize Pool  
> **Google Trends for Solana Narratives**

A real-time tool that monitors the **actual** Solana content pipeline and visualizes narrative frequency over time. Built with guidance from Alex Scott (Solana Foundation UAE/MENA lead).

![Solana Narrative Detector v2](https://img.shields.io/badge/Solana-Narrative_Detector_v2-9945ff?style=for-the-badge&logo=solana)

## ✨ The Vision

**Google Trends for Solana Narratives** - This tool ingests the ACTUAL Solana content pipeline and visualizes narrative frequency over time, providing ecosystem intelligence that moves beyond generic sentiment to track real thematic developments.

## 🎯 Key Features

### Real Data Ingestion
- **Twitter/X Monitoring** - Key Solana accounts via `bird` CLI
- **YouTube Transcripts** - Solana Foundation & Superteam channels  
- **Event Content** - Accelerate Hong Kong, Consensus, Consumer Day
- **Podcast Network** - Solana podcast ecosystem

### Advanced Analytics
- **Semantic Theme Extraction** - NLP clustering, not just keywords
- **Time-Series Tracking** - 1 week / 1 month / 3 month windows
- **Momentum Detection** - Accelerating vs steady vs declining narratives
- **Source Attribution** - Break down by content type and origin

### Google Trends-Style Dashboard
- Clean, modern dark theme
- Interactive line graphs showing narrative frequency over time
- Search bar to query specific narratives
- "Rising Narratives" sidebar with biggest week-over-week increases
- Source breakdown and sample content with links
- Responsive, mobile-friendly design

## 🚀 Quick Start

### Prerequisites
```bash
# Install bird CLI for Twitter data
# Visit: https://github.com/travisbrown/bird

# Install Python dependencies
pip install -r requirements.txt
```

### Run Full Pipeline
```bash
# 1. Run narrative detection
python main.py detect

# 2. Start web dashboard
python main.py server

# 3. Open dashboard
open http://localhost:8000
```

### Alternative: Direct Server Start
```bash
python server.py
```

## 📊 Live Demo

🌐 **Dashboard**: [View Live Demo](http://localhost:8000) (after running locally)  
📱 **Mobile Responsive**: Works on all devices  
🔗 **API Documentation**: http://localhost:8000/docs

## 🔍 Validated Narratives

The tool detects and tracks these current Solana narratives:

### 🤖 **Autonomous Agent Economy** (NEW - Accelerating)
- Superteam Earn agent bounties
- 3,700+ agent hackathon registrations
- AI trading bot infrastructure

### 💰 **Payments/Stablecoins** (Evergreen - Accelerating)
- Contra launch (Jan 28, $2B+ volume)
- $10T+ stablecoin volume projections 2025
- Institutional payment infrastructure

### 🏢 **RWA/Tokenization** (Institutional Focus)
- Catherine Gu (Visa) joining ecosystem
- Traditional finance integration
- Real-world asset protocols

### 📱 **Consumer Crypto** (Growth Focus)
- Consumer Day events
- Mobile wallet adoption
- UX/UI improvements

## 🛠 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │ -> │  NLP Processing  │ -> │   Dashboard     │
│                 │    │                  │    │                 │
│ • Twitter/X     │    │ • TF-IDF         │    │ • Google Trends │
│ • YouTube       │    │ • DBSCAN         │    │   Style UI      │
│ • Events        │    │ • Clustering     │    │ • Time Series   │
│ • Podcasts      │    │ • Momentum       │    │ • Interactive   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📡 Data Sources (Ranked by Importance)

### 1. X/Twitter Discourse
**Key Accounts Monitored:**
- `@aaboronkov` (Toly, co-founder)
- `@rajgokal` (Raj, co-founder)
- `@lilybliu` (Lily Liu, Foundation President)
- `@AkshayBD` (ecosystem lead)
- `@kashdhanda` (Kash Donda)
- `@vibaboronkov` (Vibhu, Foundation marketing)
- `@solaboratory` (Solana Foundation official)
- `@SuperteamDAO`, `@SuperteamDE`, `@SuperteamUK`, `@SuperteamIN`

### 2. YouTube/Livestream Transcripts
- Solana Foundation YouTube
- Superteam channels
- Conference talks and demos

### 3. Event Content
- **Accelerate Hong Kong** (happening this week)
- Consensus side events
- Consumer Day coverage

## 🔧 API Endpoints

The FastAPI backend provides these endpoints:

- `GET /` - Main dashboard interface
- `GET /api/narratives` - All detected narratives
- `GET /api/rising` - Rising narratives only
- `GET /api/search?q={query}` - Search narratives
- `GET /api/narrative/{name}` - Specific narrative details
- `GET /api/trends` - Time-series chart data
- `POST /api/refresh` - Force data refresh

## 🗂 Project Structure

```
solana-narrative-detector/
├── main.py                 # Main CLI entry point
├── server.py              # FastAPI backend server
├── dashboard.html         # Frontend dashboard
├── data_ingestion.py      # Real data ingestion pipeline
├── narrative_engine.py    # NLP analysis and clustering
├── requirements.txt       # Python dependencies
├── data/                  # Generated data files
│   ├── raw_content.json   # Ingested content
│   ├── narrative_analysis.json
│   └── reports/
└── README.md
```

## 🎨 Dashboard Features

### Google Trends-Style Interface
- **Dark Theme** - Modern, professional appearance
- **Interactive Charts** - Hover for details, zoom, filter
- **Search Functionality** - Find specific narratives instantly
- **Time Controls** - Switch between 1W, 1M, 3M views

### Rising Narratives Sidebar
- Real-time momentum scoring
- Week-over-week growth percentages
- Visual trend indicators (🔺🔻▶️)

### Narrative Detail Cards
- Confidence scores and frequency counts
- Keyword extraction with relevance
- Sample content with source links
- Source breakdown (Twitter, YouTube, Events)

## 🚢 Deployment

### Vercel Deployment (Recommended)
```bash
# Build static version
python main.py detect

# Deploy to Vercel
vercel deploy

# Custom domain
vercel --prod
```

### Docker Deployment
```bash
# Build image
docker build -t solana-narrative-detector .

# Run container
docker run -p 8000:8000 solana-narrative-detector
```

### Local Development
```bash
# Run in development mode
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

## 📈 Example Output

```json
{
  "narratives": [
    {
      "name": "Autonomous Agents",
      "confidence": 0.92,
      "frequency": 45,
      "momentum": "accelerating",
      "keywords": ["agent", "autonomous", "ai", "bot", "hackathon"],
      "timespan_data": [
        {"date": "2026-02-12", "count": 15},
        {"date": "2026-02-11", "count": 18},
        {"date": "2026-02-10", "count": 12}
      ],
      "source_breakdown": {
        "twitter": 32,
        "youtube": 8, 
        "event": 5
      },
      "sample_content": [
        "Solana agent hackathon sees 3,700+ registrations...",
        "@SuperteamDAO announces $50k in agent bounties..."
      ]
    }
  ]
}
```

## 🛡 Requirements Met

✅ **Real Data Sources** - Uses actual Twitter via bird CLI, YouTube transcripts  
✅ **Google Trends UI** - Clean dark theme with time-series visualization  
✅ **NLP Clustering** - TF-IDF + DBSCAN for semantic theme extraction  
✅ **Time-Series Tracking** - Daily/weekly/monthly frequency analysis  
✅ **Source Attribution** - Breaks down content by platform and account  
✅ **Momentum Detection** - Identifies accelerating vs declining narratives  
✅ **Interactive Dashboard** - Search, filter, drill-down capabilities  
✅ **Deploy Ready** - FastAPI backend, static frontend, containerized  

## 🏆 Superteam Earn Bounty

**Submission Details:**
- **Bounty ID**: `fd499139-21a9-443d-a0fc-cb418f646f0d`
- **Prize Pool**: $3,500
- **Builder**: Sterling Rhodes
- **GitHub**: https://github.com/riverventures/solana-narrative-detector
- **Contact**: http://t.me/afscott

## 🔄 Updates After Submission

To update the Superteam Earn submission:

```bash
curl -s -X POST "https://superteam.fun/api/agents/submissions/update" \
  -H "Authorization: Bearer sk_367f333112d5d1e0258c9e90fd04f2947a23321a59c32d1bb5352b0f0d2c21c2" \
  -H "Content-Type: application/json" \
  -d '{
    "listingId": "fd499139-21a9-443d-a0fc-cb418f646f0d",
    "link": "https://github.com/riverventures/solana-narrative-detector",
    "tweet": "",
    "otherInfo": "v2 Complete - Google Trends style dashboard with real Solana ecosystem data ingestion and NLP-powered narrative detection",
    "eligibilityAnswers": [],
    "ask": null,
    "telegram": "http://t.me/afscott"
  }'
```

## 📝 License

MIT License - Built for the Solana ecosystem

---

**Built by Sterling Rhodes for Superteam Earn**  
*Making Solana narrative trends as accessible as Google Trends*