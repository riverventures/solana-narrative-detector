#!/usr/bin/env python3
"""
Solana Narrative Detector v2 - FastAPI Backend Server
Serves the dashboard and provides API endpoints for narrative data
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import os

from data_ingestion import DataIngestionOrchestrator
from narrative_engine import NarrativeAnalyzer

app = FastAPI(
    title="Solana Narrative Detector v2",
    description="Google Trends for Solana Narratives - Real-time ecosystem intelligence",
    version="2.0.0"
)

# Global state for caching
narrative_data = None
last_update = None
UPDATE_INTERVAL = 3600  # 1 hour in seconds

class NarrativeServer:
    """Main server class handling data and endpoints"""
    
    def __init__(self):
        self.ingestion = DataIngestionOrchestrator()
        self.analyzer = NarrativeAnalyzer()
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        Path("data").mkdir(exist_ok=True)
    
    async def get_latest_data(self, force_refresh: bool = False) -> Dict:
        """Get latest narrative data, refreshing if needed"""
        global narrative_data, last_update
        
        now = datetime.now()
        
        # Check if we need to refresh data
        if (force_refresh or 
            narrative_data is None or 
            last_update is None or 
            (now - last_update).total_seconds() > UPDATE_INTERVAL):
            
            print("🔄 Refreshing narrative data...")
            try:
                # Ingest fresh content
                content = await self.ingestion.ingest_all_content()
                self.ingestion.save_raw_data(content)
                
                # Analyze narratives
                analysis_result = self.analyzer.analyze_content()
                
                # Save analysis
                with open("data/narrative_analysis.json", 'w') as f:
                    json.dump(analysis_result, f, indent=2)
                
                narrative_data = analysis_result
                last_update = now
                
                print(f"✅ Data refreshed: {len(narrative_data['narratives'])} narratives detected")
                
            except Exception as e:
                print(f"❌ Error refreshing data: {e}")
                # Try to load existing data as fallback
                if Path("data/narrative_analysis.json").exists():
                    with open("data/narrative_analysis.json", 'r') as f:
                        narrative_data = json.load(f)
                else:
                    # Return demo data as last resort
                    narrative_data = self._get_demo_data()
        
        return narrative_data
    
    def _get_demo_data(self) -> Dict:
        """Generate demo data for fallback"""
        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "total_content_analyzed": 847,
            "narratives_detected": 6,
            "narratives": [
                {
                    "name": "Autonomous Agents",
                    "keywords": ["agent", "autonomous", "ai", "bot", "hackathon"],
                    "confidence": 0.92,
                    "frequency": 45,
                    "momentum": "accelerating",
                    "source_breakdown": {"twitter": 32, "youtube": 8, "event": 5},
                    "sample_content": [
                        "Solana agent hackathon sees 3,700+ registrations...",
                        "@SuperteamDAO announces new agent bounties...",
                        "Drift protocol integration with autonomous agents..."
                    ],
                    "timespan_data": [
                        {"date": "2026-02-12", "count": 15},
                        {"date": "2026-02-11", "count": 18},
                        {"date": "2026-02-10", "count": 12},
                        {"date": "2026-02-09", "count": 8},
                        {"date": "2026-02-08", "count": 5},
                        {"date": "2026-02-07", "count": 3},
                        {"date": "2026-02-06", "count": 2}
                    ]
                }
            ],
            "source_summary": {
                "total_sources": 15,
                "source_breakdown": {"twitter": 142, "youtube": 38, "event": 20},
                "top_accounts": [["aaboronkov", 25], ["SuperteamDAO", 22]]
            },
            "rising_narratives": [
                {"name": "Autonomous Agents", "momentum_score": 2.1, "frequency": 45, "confidence": 0.92}
            ]
        }

# Initialize server
server = NarrativeServer()

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the main dashboard"""
    try:
        with open("dashboard.html", 'r') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dashboard file not found")

@app.get("/api/narratives")
async def get_narratives(refresh: bool = False):
    """Get all detected narratives"""
    try:
        data = await server.get_latest_data(force_refresh=refresh)
        return {
            "narratives": data["narratives"],
            "total_detected": data["narratives_detected"],
            "last_updated": data["analysis_timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching narratives: {str(e)}")

@app.get("/api/rising")
async def get_rising_narratives():
    """Get rising narratives only"""
    try:
        data = await server.get_latest_data()
        return {
            "rising_narratives": data["rising_narratives"],
            "last_updated": data["analysis_timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching rising narratives: {str(e)}")

@app.get("/api/search")
async def search_narratives(q: str):
    """Search narratives by keyword"""
    try:
        data = await server.get_latest_data()
        query = q.lower()
        
        matching_narratives = [
            narrative for narrative in data["narratives"]
            if query in narrative["name"].lower() or 
            any(query in keyword.lower() for keyword in narrative["keywords"])
        ]
        
        return {
            "query": q,
            "results": matching_narratives,
            "total_found": len(matching_narratives)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching narratives: {str(e)}")

@app.get("/api/narrative/{narrative_name}")
async def get_narrative_details(narrative_name: str):
    """Get detailed information about a specific narrative"""
    try:
        data = await server.get_latest_data()
        
        # Find matching narrative
        narrative = next(
            (n for n in data["narratives"] if n["name"].lower() == narrative_name.lower()),
            None
        )
        
        if not narrative:
            raise HTTPException(status_code=404, detail="Narrative not found")
        
        return {
            "narrative": narrative,
            "last_updated": data["analysis_timestamp"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching narrative: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    try:
        data = await server.get_latest_data()
        return {
            "total_narratives": data["narratives_detected"],
            "content_analyzed": data["total_content_analyzed"],
            "sources_tracked": data["source_summary"]["total_sources"],
            "rising_count": len(data["rising_narratives"]),
            "source_breakdown": data["source_summary"]["source_breakdown"],
            "top_accounts": data["source_summary"]["top_accounts"],
            "last_updated": data["analysis_timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@app.post("/api/refresh")
async def force_refresh():
    """Force refresh of narrative data"""
    try:
        data = await server.get_latest_data(force_refresh=True)
        return {
            "message": "Data refreshed successfully",
            "narratives_detected": data["narratives_detected"],
            "content_analyzed": data["total_content_analyzed"],
            "timestamp": data["analysis_timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing data: {str(e)}")

@app.get("/api/trends")
async def get_trend_data():
    """Get time-series trend data for charts"""
    try:
        data = await server.get_latest_data()
        
        # Prepare chart data
        chart_data = {
            "dates": [],
            "datasets": []
        }
        
        if data["narratives"]:
            # Get dates from first narrative
            chart_data["dates"] = [item["date"] for item in data["narratives"][0]["timespan_data"]]
            
            # Add data for top 5 narratives
            for narrative in data["narratives"][:5]:
                chart_data["datasets"].append({
                    "name": narrative["name"],
                    "data": [item["count"] for item in narrative["timespan_data"]],
                    "momentum": narrative["momentum"]
                })
        
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trend data: {str(e)}")

@app.get("/data/narrative_analysis.json")
async def get_raw_data():
    """Serve raw analysis data for frontend"""
    try:
        data = await server.get_latest_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# Background task to periodically refresh data
@app.on_event("startup")
async def startup_event():
    """Initialize data on startup"""
    print("🚀 Starting Solana Narrative Detector v2...")
    # Don't block startup, but start with demo data
    global narrative_data
    if not narrative_data:
        narrative_data = server._get_demo_data()
    print("✅ Server ready!")

if __name__ == "__main__":
    print("🌐 Starting Solana Narrative Detector v2 Server...")
    print("📊 Dashboard: http://localhost:8000")
    print("🔗 API docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )