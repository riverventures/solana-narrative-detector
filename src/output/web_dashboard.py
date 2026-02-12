"""
Web Dashboard
Simple Flask-based dashboard to display narrative detection results
"""

from flask import Flask, render_template_string, jsonify
import json
import os
from pathlib import Path

class WebDashboard:
    def __init__(self, data_file: str = "data/narratives.json"):
        self.app = Flask(__name__)
        self.data_file = data_file
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def dashboard():
            return render_template_string(self._get_dashboard_html())
        
        @self.app.route('/api/data')
        def api_data():
            return jsonify(self._load_data())
        
        @self.app.route('/api/health')
        def health():
            return jsonify({"status": "healthy", "tool": "Solana Narrative Detector"})
    
    def _load_data(self):
        """Load narrative data from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"narratives": [], "metadata": {}, "summary": {}}
    
    def serve(self, host: str = '127.0.0.1', port: int = 8080, debug: bool = False):
        """Start the web server"""
        self.app.run(host=host, port=port, debug=debug)
    
    def _get_dashboard_html(self):
        """Return HTML template for dashboard"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solana Narrative Detector</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            color: #2d3748;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            color: #718096;
            font-size: 1.1rem;
        }
        
        .header .bounty-info {
            background: #9f7aea;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            margin-top: 15px;
            font-weight: 600;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-card .number {
            font-size: 2.5rem;
            font-weight: bold;
            color: #9f7aea;
            display: block;
        }
        
        .stat-card .label {
            color: #718096;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .narratives-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }
        
        .narrative-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .narrative-card:hover {
            transform: translateY(-5px);
        }
        
        .narrative-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        
        .narrative-rank {
            background: #9f7aea;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }
        
        .narrative-title {
            flex: 1;
            margin-left: 15px;
        }
        
        .narrative-title h3 {
            color: #2d3748;
            font-size: 1.3rem;
            margin-bottom: 5px;
        }
        
        .momentum-badge {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .momentum-accelerating {
            background: #48bb78;
            color: white;
        }
        
        .momentum-stable {
            background: #ed8936;
            color: white;
        }
        
        .momentum-declining {
            background: #f56565;
            color: white;
        }
        
        .momentum-emerging {
            background: #4299e1;
            color: white;
        }
        
        .confidence-bar {
            background: #e2e8f0;
            height: 8px;
            border-radius: 4px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #f56565, #ed8936, #48bb78);
            transition: width 0.5s ease;
        }
        
        .ideas-list {
            margin-top: 20px;
        }
        
        .ideas-list h4 {
            color: #2d3748;
            margin-bottom: 10px;
            font-size: 1rem;
        }
        
        .ideas-list ul {
            list-style: none;
        }
        
        .ideas-list li {
            background: #f7fafc;
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 8px;
            border-left: 3px solid #9f7aea;
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            color: white;
            font-size: 1.2rem;
        }
        
        .error {
            background: #fed7d7;
            color: #9b2c2c;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .refresh-btn {
            background: #9f7aea;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s ease;
            margin-top: 20px;
        }
        
        .refresh-btn:hover {
            background: #805ad5;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .narratives-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Solana Narrative Detector</h1>
            <p class="subtitle">Real-time detection of emerging narratives in the Solana ecosystem</p>
            <div class="bounty-info">
                🏆 Superteam Earn Bounty - $3,500 Prize Pool
            </div>
        </div>
        
        <div id="loading" class="loading">
            Loading narrative data...
        </div>
        
        <div id="error" class="error" style="display: none;"></div>
        
        <div id="dashboard" style="display: none;">
            <div class="summary-grid">
                <div class="stat-card">
                    <span id="total-narratives" class="number">0</span>
                    <span class="label">Narratives Detected</span>
                </div>
                <div class="stat-card">
                    <span id="avg-confidence" class="number">0%</span>
                    <span class="label">Average Confidence</span>
                </div>
                <div class="stat-card">
                    <span id="signal-sources" class="number">0</span>
                    <span class="label">Signal Sources</span>
                </div>
                <div class="stat-card">
                    <span id="top-momentum" class="number">0</span>
                    <span class="label">Highest Momentum</span>
                </div>
            </div>
            
            <button class="refresh-btn" onclick="loadData()">🔄 Refresh Data</button>
            
            <div id="narratives-container" class="narratives-grid">
                <!-- Narratives will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        async function loadData() {
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const dashboard = document.getElementById('dashboard');
            
            loading.style.display = 'block';
            error.style.display = 'none';
            dashboard.style.display = 'none';
            
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                
                if (data.narratives && data.narratives.length > 0) {
                    renderDashboard(data);
                    dashboard.style.display = 'block';
                } else {
                    showError('No narrative data available. Run the detector first!');
                }
                
                loading.style.display = 'none';
            } catch (err) {
                console.error('Error loading data:', err);
                showError('Failed to load data. Is the detector running?');
                loading.style.display = 'none';
            }
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
        
        function renderDashboard(data) {
            // Update summary stats
            document.getElementById('total-narratives').textContent = data.narratives.length;
            document.getElementById('avg-confidence').textContent = 
                Math.round((data.summary.average_confidence || 0) * 100) + '%';
            document.getElementById('signal-sources').textContent = 
                data.summary.signal_sources ? data.summary.signal_sources.length : 0;
            document.getElementById('top-momentum').textContent = 
                data.summary.top_trend ? data.summary.top_trend.momentum_score.toFixed(2) : '0';
            
            // Render narratives
            const container = document.getElementById('narratives-container');
            container.innerHTML = '';
            
            data.narratives.forEach(narrative => {
                const card = createNarrativeCard(narrative);
                container.appendChild(card);
            });
        }
        
        function createNarrativeCard(narrative) {
            const card = document.createElement('div');
            card.className = 'narrative-card';
            
            const momentumClass = `momentum-${narrative.momentum.trend}`;
            const confidencePercent = Math.round(narrative.confidence * 100);
            
            card.innerHTML = `
                <div class="narrative-header">
                    <div class="narrative-rank">${narrative.rank}</div>
                    <div class="narrative-title">
                        <h3>${narrative.name}</h3>
                        <span class="momentum-badge ${momentumClass}">
                            ${narrative.momentum.trend}
                        </span>
                    </div>
                </div>
                
                <p style="color: #718096; margin-bottom: 15px;">
                    ${narrative.description}
                </p>
                
                <div style="margin-bottom: 15px;">
                    <strong>Confidence: ${confidencePercent}%</strong>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong>Momentum Score:</strong> ${narrative.momentum.score}
                    <br>
                    <small style="color: #718096;">${narrative.momentum.explanation}</small>
                </div>
                
                <div class="ideas-list">
                    <h4>💡 Product Ideas</h4>
                    <ul>
                        ${narrative.product_ideas.map(idea => `<li>${idea}</li>`).join('')}
                    </ul>
                </div>
                
                <div style="margin-top: 15px; font-size: 0.9rem; color: #718096;">
                    <strong>Signals:</strong> ${narrative.signals.count} from ${narrative.signals.sources.join(', ')}
                </div>
            `;
            
            return card;
        }
        
        // Load data on page load
        document.addEventListener('DOMContentLoaded', loadData);
    </script>
</body>
</html>
        '''
    
    def generate_static_html(self, output_file: str = "web/index.html"):
        """Generate a static HTML file with embedded data"""
        data = self._load_data()
        
        # Create web directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Embed data in HTML
        html = self._get_dashboard_html()
        
        # Replace the fetch call with embedded data
        embedded_data = f"const embeddedData = {json.dumps(data, indent=2)};"
        
        # Modify the loadData function to use embedded data
        static_js = '''
        async function loadData() {
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const dashboard = document.getElementById('dashboard');
            
            loading.style.display = 'block';
            error.style.display = 'none';
            dashboard.style.display = 'none';
            
            try {
                const data = embeddedData;
                
                if (data.narratives && data.narratives.length > 0) {
                    renderDashboard(data);
                    dashboard.style.display = 'block';
                } else {
                    showError('No narrative data available. Run the detector first!');
                }
                
                loading.style.display = 'none';
            } catch (err) {
                console.error('Error loading data:', err);
                showError('Failed to load embedded data.');
                loading.style.display = 'none';
            }
        }
        '''
        
        # Insert embedded data and modified JS
        html = html.replace('<script>', f'<script>\n{embedded_data}\n{static_js}')
        html = html.replace('async function loadData() {', '// Original loadData replaced\n/*')
        html = html.replace('// Load data on page load', '*/')
        
        with open(output_file, 'w') as f:
            f.write(html)
        
        return output_file