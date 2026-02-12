# Deployment Guide - Solana Narrative Detector v2

This guide covers deploying the Solana Narrative Detector v2 to various platforms.

## 🚀 Quick Deploy

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set up custom domain (optional)
vercel --prod
```

### Heroku
```bash
# Create Heroku app
heroku create solana-narrative-detector

# Add Python buildpack
heroku buildpacks:add heroku/python

# Deploy
git push heroku main
```

### Docker
```bash
# Build image
docker build -t solana-narrative-detector .

# Run locally
docker run -p 8000:8000 solana-narrative-detector

# Deploy to any container platform
```

## 🔧 Local Development

### Prerequisites
1. **Python 3.11+**
2. **bird CLI** for Twitter data
   ```bash
   # macOS
   brew install bird
   
   # Linux/Windows
   # Visit: https://github.com/travisbrown/bird
   ```

### Setup
```bash
# Clone repository
git clone https://github.com/riverventures/solana-narrative-detector
cd solana-narrative-detector

# Install dependencies
pip install -r requirements.txt

# Run detection pipeline
python main.py detect

# Start web server
python main.py server
```

### Environment Variables
```bash
# Optional: Set bird CLI path
export BIRD_PATH=/usr/local/bin/bird

# Optional: Set data refresh interval (seconds)
export REFRESH_INTERVAL=3600
```

## 📊 Monitoring and Scaling

### Health Checks
The application provides a health check endpoint:
```
GET /health
```

### Performance
- **Memory**: ~500MB baseline
- **CPU**: Low, spikes during analysis
- **Storage**: Minimal (< 100MB for data files)

### Scaling Considerations
1. **Rate Limiting**: bird CLI has Twitter API limits
2. **Data Size**: Grows linearly with content volume
3. **Analysis Time**: ~30-60 seconds for full pipeline

## 🔒 Security

### API Security
- No authentication required for read-only endpoints
- POST endpoints should be rate-limited in production
- Consider adding API keys for private deployments

### Data Privacy
- No personal data stored
- Only public social media content processed
- All data is aggregated and anonymized

## 📈 Production Configuration

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Cache static assets
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Systemd Service
```ini
[Unit]
Description=Solana Narrative Detector
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/app
Environment=PATH=/usr/local/bin
ExecStart=/usr/local/bin/python server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## 🔄 Continuous Deployment

### GitHub Actions
```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 🐛 Troubleshooting

### Common Issues

1. **bird CLI not found**
   ```bash
   # Check installation
   which bird
   bird --version
   ```

2. **Python dependencies conflict**
   ```bash
   # Use virtual environment
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **NLTK data missing**
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

4. **Port already in use**
   ```bash
   # Find and kill process
   lsof -i :8000
   kill -9 <PID>
   ```

### Log Analysis
```bash
# Check application logs
tail -f /var/log/solana-narrative-detector.log

# Check system resources
htop
df -h
```

## 📞 Support

For deployment issues:
1. Check the GitHub Issues page
2. Review error logs carefully
3. Ensure all prerequisites are installed
4. Contact: http://t.me/afscott

---

**Built by Sterling Rhodes for Superteam Earn**