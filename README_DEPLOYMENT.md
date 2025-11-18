# 🚀 Quick Deployment Guide

## One-Command Deployment

### Windows:
```powershell
.\deploy.ps1
```

### Linux/Mac:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## What Gets Deployed

✅ **Backend API** (FastAPI) - Port 8000
✅ **Frontend** (Next.js) - Port 3000  
✅ **PostgreSQL Database** - Port 5432
✅ **Nginx Reverse Proxy** (Optional) - Port 80/443

---

## Access After Deployment

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## Production Deployment

See `PRODUCTION_DEPLOYMENT.md` for:
- Railway deployment
- Render deployment
- AWS EC2 deployment
- DigitalOcean deployment
- SSL/HTTPS setup
- Security configuration

---

## Environment Variables

Copy `.env.example` to `.env` and update:
- `DATABASE_URL` - PostgreSQL connection
- `SECRET_KEY` - Random secret key
- `ALLOWED_ORIGINS` - Your domain(s)
- `NEXT_PUBLIC_API_URL` - Backend URL

---

## Troubleshooting

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop all
docker-compose down

# Rebuild
docker-compose up -d --build
```

---

**That's it! Your app is now hosted! 🎉**

