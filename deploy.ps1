# PowerShell deployment script for Contract Risk Analyzer

Write-Host "🚀 Starting deployment..." -ForegroundColor Green
Write-Host ""

# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "   Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose is not installed. Please install Docker Compose first." -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating .env file from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Please update .env file with your configuration!" -ForegroundColor Yellow
    Write-Host ""
}

# Create necessary directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "backend\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\models" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "nginx\ssl" | Out-Null
New-Item -ItemType Directory -Force -Path "frontend\.next" | Out-Null

# Generate secret key if not set
$envContent = Get-Content ".env" -Raw -ErrorAction SilentlyContinue
if ($envContent -notmatch "SECRET_KEY=.*[a-zA-Z0-9]{32,}") {
    Write-Host "🔑 Generating secret key..." -ForegroundColor Yellow
    $secretKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
    if (Test-Path ".env") {
        $envContent = $envContent -replace "SECRET_KEY=.*", "SECRET_KEY=$secretKey"
        Set-Content -Path ".env" -Value $envContent
    }
}

# Build and start services
Write-Host ""
Write-Host "🔨 Building Docker images..." -ForegroundColor Green
docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting services..." -ForegroundColor Green
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start services!" -ForegroundColor Red
    exit 1
}

# Wait for services to be ready
Write-Host ""
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check if services are running
$services = docker-compose ps --services
$running = docker-compose ps --services --filter "status=running"

if ($running) {
    Write-Host ""
    Write-Host "✅ Services are running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Access the application:" -ForegroundColor Cyan
    Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
    Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 View logs:" -ForegroundColor Yellow
    Write-Host "   docker-compose logs -f" -ForegroundColor White
    Write-Host ""
    Write-Host "🛑 Stop services:" -ForegroundColor Yellow
    Write-Host "   docker-compose down" -ForegroundColor White
    Write-Host ""
    Write-Host "🔄 Restart services:" -ForegroundColor Yellow
    Write-Host "   docker-compose restart" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Some services failed to start. Check logs:" -ForegroundColor Red
    Write-Host "   docker-compose logs" -ForegroundColor Yellow
    exit 1
}

