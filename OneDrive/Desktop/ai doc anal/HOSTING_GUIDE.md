# 🚀 Hosting Guide - Contract Risk Analyzer

Complete guide to deploy your Contract Risk Analyzer application on various platforms.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Deployment Options](#deployment-options)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Database Setup](#database-setup)
6. [Environment Variables](#environment-variables)
7. [Production Checklist](#production-checklist)

---

## Prerequisites

### Required Software
- Python 3.9+ (for backend)
- Node.js 18+ and npm/yarn (for frontend)
- PostgreSQL or SQLite (database)
- Git

### Required Accounts
- GitHub/GitLab (for code repository)
- Cloud provider account (AWS, GCP, Azure, Railway, Render, etc.)

---

## Deployment Options

### Option 1: Railway (Recommended for Quick Start) ⭐
**Best for:** Quick deployment, automatic HTTPS, easy database setup

**Steps:**
1. **Sign up at [Railway.app](https://railway.app)**
2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Backend Setup:**
   - Add new service → "Empty Service"
   - Set root directory: `backend`
   - Add environment variables (see [Environment Variables](#environment-variables))
   - Add PostgreSQL database service
   - Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Frontend Setup:**
   - Add new service → "Empty Service"
   - Set root directory: `frontend`
   - Add environment variables:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
     ```
   - Set start command: `npm run build && npm start`

5. **Configure Domains:**
   - Railway automatically provides HTTPS URLs
   - You can add custom domains in project settings

**Cost:** Free tier available, then pay-as-you-go

---

### Option 2: Render
**Best for:** Free tier with automatic deployments

**Backend:**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** contract-analyzer-backend
   - **Root Directory:** `backend`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:** (see below)

**Frontend:**
1. Click "New" → "Static Site"
2. Connect repository
3. Configure:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `.next`
   - **Environment Variables:**
     ```
     NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
     ```

**Database:**
1. Click "New" → "PostgreSQL"
2. Copy connection string to backend environment variables

**Cost:** Free tier available (with limitations)

---

### Option 3: AWS (EC2 + S3 + RDS)
**Best for:** Production, scalability, full control

**Steps:**

1. **Launch EC2 Instance:**
   ```bash
   # Ubuntu 22.04 LTS
   # Instance type: t3.medium or larger (for ML model)
   # Security Group: Allow HTTP (80), HTTPS (443), SSH (22)
   ```

2. **Connect and Setup:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python, Node.js, Nginx
   sudo apt install python3.9 python3-pip nodejs npm nginx postgresql -y
   
   # Install PM2 for process management
   sudo npm install -g pm2
   ```

3. **Clone and Setup Backend:**
   ```bash
   git clone your-repo-url
   cd ai-doc-anal/backend
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Setup environment variables
   nano .env
   # (Add all environment variables)
   
   # Run database migrations
   alembic upgrade head
   
   # Start with PM2
   pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name backend
   pm2 save
   pm2 startup
   ```

4. **Setup Frontend:**
   ```bash
   cd ../frontend
   npm install
   npm run build
   
   # Start with PM2
   pm2 start "npm start" --name frontend
   pm2 save
   ```

5. **Configure Nginx:**
   ```bash
   sudo nano /etc/nginx/sites-available/contract-analyzer
   ```
   
   Add configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       # Frontend
       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
       
       # Backend API
       location /api {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   
   ```bash
   sudo ln -s /etc/nginx/sites-available/contract-analyzer /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

6. **Setup SSL with Let's Encrypt:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

7. **Setup RDS PostgreSQL:**
   - Create RDS instance in AWS Console
   - Use connection string in backend `.env`

**Cost:** ~$50-100/month (depending on instance size)

---

### Option 4: Docker + Docker Compose (Any VPS)
**Best for:** Easy deployment, consistent environment

1. **Create `docker-compose.yml` in project root:**
   ```yaml
   version: '3.8'
   
   services:
     db:
       image: postgres:15
       environment:
         POSTGRES_DB: contract_analyzer
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: your_password
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"
   
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       environment:
         DATABASE_URL: postgresql://postgres:your_password@db:5432/contract_analyzer
         ML_MODE: ml
       depends_on:
         - db
       volumes:
         - ./backend:/app
         - ./backend/models:/app/models
   
     frontend:
       build: ./frontend
       ports:
         - "3000:3000"
       environment:
         NEXT_PUBLIC_API_URL: http://localhost:8000
       depends_on:
         - backend
   
   volumes:
     postgres_data:
   ```

2. **Create `backend/Dockerfile`:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **Create `frontend/Dockerfile`:**
   ```dockerfile
   FROM node:18-alpine AS builder
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build
   
   FROM node:18-alpine
   WORKDIR /app
   COPY --from=builder /app/.next ./.next
   COPY --from=builder /app/public ./public
   COPY --from=builder /app/package*.json ./
   RUN npm install --production
   CMD ["npm", "start"]
   ```

4. **Deploy:**
   ```bash
   docker-compose up -d
   ```

---

## Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname
# OR for SQLite: sqlite:///./contract_analyzer.db

# App Settings
ML_MODE=ml  # or "rules" for rule-based only
MODEL_PATH=./models/risk_classifier
USE_GPU=false  # Set to true if GPU available

# Security
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com

# File Upload
UPLOADS_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB in bytes

# Logging
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
# For production: https://your-backend-url.com
```

---

## Database Setup

### PostgreSQL (Production)
```bash
# Create database
createdb contract_analyzer

# Run migrations
cd backend
alembic upgrade head
```

### SQLite (Development)
```bash
# Database file will be created automatically
# Run migrations
cd backend
alembic upgrade head
```

---

## Production Checklist

### Security
- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Set up CORS properly (ALLOWED_ORIGINS)
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Set up backup strategy

### Performance
- [ ] Enable gzip compression
- [ ] Configure CDN for static assets (optional)
- [ ] Set up caching (Redis recommended)
- [ ] Optimize database queries
- [ ] Enable database connection pooling

### Monitoring
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Monitor resource usage (CPU, RAM, disk)

### ML Model
- [ ] Ensure model files are included in deployment
- [ ] Test model loading on production server
- [ ] Consider GPU instance if using ML mode

### Testing
- [ ] Test file upload
- [ ] Test document analysis
- [ ] Test all API endpoints
- [ ] Test frontend-backend communication
- [ ] Test error handling

---

## Quick Start Commands

### Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Production Build
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run build
npm start
```

---

## Troubleshooting

### Backend won't start
- Check database connection
- Verify environment variables
- Check port availability
- Review logs: `pm2 logs backend` or check application logs

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in backend
- Verify backend is running and accessible

### ML Model not loading
- Check `MODEL_PATH` is correct
- Ensure model files exist in deployment
- Check file permissions
- Review model loading logs

### Database connection errors
- Verify DATABASE_URL format
- Check database is running
- Verify credentials
- Check network/firewall rules

---

## Support

For issues or questions:
1. Check application logs
2. Review error messages
3. Verify environment variables
4. Test locally first
5. Check deployment platform documentation

---

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2)
- [Docker Documentation](https://docs.docker.com)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment)

---

**Happy Deploying! 🚀**
