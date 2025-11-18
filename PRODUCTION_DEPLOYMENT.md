# 🚀 Complete Production Deployment Guide

## 📋 Prerequisites

1. **Docker & Docker Compose** installed
2. **Domain name** (optional, for production)
3. **SSL certificates** (for HTTPS, optional)

---

## 🚀 Quick Deployment (Docker)

### Option 1: Automated Script (Recommended)

**Windows:**
```powershell
.\deploy.ps1
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Steps

```bash
# 1. Create .env file
cp .env.example .env
# Edit .env with your settings

# 2. Build and start
docker-compose up -d --build

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f
```

---

## 🌐 Deployment Options

### Option 1: Railway (Easiest) ⭐

1. **Sign up at [Railway.app](https://railway.app)**
2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Add PostgreSQL Database**
   - Click "New" → "Database" → "PostgreSQL"
   - Copy connection string

4. **Deploy Backend**
   - Click "New" → "GitHub Repo"
   - Select your repo
   - Root directory: `backend`
   - Add environment variables:
     ```
     DATABASE_URL=<postgres-connection-string>
     ML_MODE=ml
     SECRET_KEY=<generate-random-key>
     ALLOWED_ORIGINS=https://your-app.railway.app
     ```
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. **Deploy Frontend**
   - Click "New" → "GitHub Repo"
   - Root directory: `frontend`
   - Add environment variable:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.railway.app
     ```
   - Build command: `npm install && npm run build`
   - Start command: `npm start`

**Cost:** Free tier available, then pay-as-you-go

---

### Option 2: Render

1. **Backend:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect GitHub repo
   - Settings:
     - **Root Directory:** `backend`
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add PostgreSQL database
   - Add environment variables

2. **Frontend:**
   - Click "New" → "Static Site"
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `.next`
   - Environment: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

**Cost:** Free tier available

---

### Option 3: AWS EC2 (Full Control)

1. **Launch EC2 Instance:**
   - Ubuntu 22.04 LTS
   - Instance type: t3.medium or larger
   - Security Group: Allow HTTP (80), HTTPS (443), SSH (22)

2. **Connect and Setup:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. **Clone and Deploy:**
   ```bash
   git clone your-repo-url
   cd ai-doc-anal
   
   # Create .env file
   cp .env.example .env
   nano .env  # Edit with your settings
   
   # Deploy
   docker-compose up -d --build
   ```

4. **Setup SSL (Let's Encrypt):**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

**Cost:** ~$50-100/month

---

### Option 4: DigitalOcean App Platform

1. **Create App:**
   - Connect GitHub repo
   - Select "Docker" as source type

2. **Configure:**
   - Use `docker-compose.yml`
   - Add environment variables
   - Add PostgreSQL database

3. **Deploy:**
   - Click "Deploy"
   - App Platform handles the rest

**Cost:** ~$12-25/month

---

## 🔧 Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# App Settings
ML_MODE=ml
MODEL_PATH=./models/risk_classifier
USE_GPU=false

# Security
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# File Upload
UPLOADS_DIR=./uploads
MAX_FILE_SIZE=10485760

# Logging
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## 🔒 Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY (32+ characters)
- [ ] Enable HTTPS/SSL
- [ ] Set proper CORS (ALLOWED_ORIGINS)
- [ ] Configure firewall rules
- [ ] Enable rate limiting (Nginx)
- [ ] Set up backup strategy
- [ ] Enable database encryption
- [ ] Use environment variables (never commit secrets)
- [ ] Regular security updates

---

## 📊 Monitoring

### Health Checks
- Backend: `http://your-domain.com/health`
- Frontend: `http://your-domain.com`

### Logs
```bash
# Docker
docker-compose logs -f backend
docker-compose logs -f frontend

# Specific service
docker-compose logs -f backend --tail=100
```

### Performance
- Monitor CPU, RAM, disk usage
- Set up uptime monitoring (UptimeRobot, etc.)
- Monitor API response times
- Track error rates

---

## 🔄 Updates & Maintenance

### Update Application
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build

# Or restart specific service
docker-compose restart backend
```

### Backup Database
```bash
# Backup
docker-compose exec db pg_dump -U postgres contract_analyzer > backup.sql

# Restore
docker-compose exec -T db psql -U postgres contract_analyzer < backup.sql
```

### Update Model
```bash
# Train new model
cd backend
python -m app.ml.train --data ../ml_data/enhanced_legal_dataset.csv

# Restart backend
docker-compose restart backend
```

---

## 🐛 Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Check status
docker-compose ps

# Restart
docker-compose restart
```

### Database connection errors
- Check DATABASE_URL in .env
- Verify database is running: `docker-compose ps db`
- Check database logs: `docker-compose logs db`

### Frontend can't connect to backend
- Verify NEXT_PUBLIC_API_URL
- Check CORS settings in backend
- Check backend logs: `docker-compose logs backend`

### Model not loading
- Verify MODEL_PATH
- Check model files exist: `ls backend/models/`
- Check backend logs for errors

---

## 📈 Scaling

### Horizontal Scaling
- Use load balancer (Nginx, AWS ALB)
- Run multiple backend instances
- Use managed database (RDS, etc.)

### Vertical Scaling
- Increase EC2 instance size
- Add more RAM/CPU
- Use GPU instances for ML

---

## 💰 Cost Estimates

| Platform | Monthly Cost | Notes |
|----------|-------------|-------|
| Railway | $5-20 | Pay-as-you-go |
| Render | $7-25 | Free tier available |
| AWS EC2 | $50-100 | t3.medium instance |
| DigitalOcean | $12-25 | App Platform |
| VPS (Hetzner) | $5-15 | Budget option |

---

## 🎯 Quick Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart service
docker-compose restart backend

# Rebuild after code changes
docker-compose up -d --build

# Check status
docker-compose ps

# Access database
docker-compose exec db psql -U postgres contract_analyzer

# Backup database
docker-compose exec db pg_dump -U postgres contract_analyzer > backup.sql
```

---

## 📞 Support

For issues:
1. Check logs: `docker-compose logs`
2. Verify environment variables
3. Check service status: `docker-compose ps`
4. Review documentation

---

**Ready to deploy! Run `.\deploy.ps1` (Windows) or `./deploy.sh` (Linux/Mac)** 🚀

