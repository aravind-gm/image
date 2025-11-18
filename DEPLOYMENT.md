# 🚀 Deployment Guide

## Option 1: Railway.app (⭐ Recommended - Easiest)

**Time: ~1-2 minutes**

### Steps:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Create new project

2. **Deploy from GitHub**
   ```bash
   # In your repository
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

3. **Connect to Railway**
   - Click "Create Project" → "Deploy from GitHub"
   - Select your repository
   - Railway auto-detects Python and uses `Procfile`

4. **Set Environment Variables** (if needed)
   ```
   FLASK_ENV=production
   ```

5. **Deploy**
   - Click "Deploy Now"
   - Wait ~90 seconds
   - Get your URL from "Domains"

### Cost: **FREE** (limited to 500 hours/month)

---

## Option 2: Render.com

**Time: ~2-3 minutes**

### Steps:

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Service**
   - Dashboard → New → Web Service
   - Connect GitHub repository
   - Select branch (main)

3. **Configure**
   - **Environment**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt && pip install gunicorn`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 app:app`
   - **Plan**: Free

4. **Deploy**
   - Click "Create Web Service"
   - Wait for build (~2 minutes)
   - Get URL from dashboard

### Cost: **FREE** (with limitations)

---

## Option 3: Heroku Alternative (Render/Railway)

Since Heroku removed free tier, use Railway or Render instead.

---

## Option 4: Docker + Local VPS

**For DigitalOcean, Linode, AWS EC2, etc.**

### Build & Run:

```bash
# Build image
docker build -t image-similarity:latest .

# Run locally
docker run -p 5000:5000 image-similarity:latest

# Push to registry (e.g., Docker Hub)
docker tag image-similarity:latest yourusername/image-similarity:latest
docker push yourusername/image-similarity:latest
```

### On VPS:

```bash
# SSH into VPS
ssh user@your-vps-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Pull and run
docker pull yourusername/image-similarity:latest
docker run -d -p 80:5000 yourusername/image-similarity:latest
```

### Cost: **~$5-15/month** (DigitalOcean, Linode)

---

## Option 5: AWS Elastic Beanstalk

**Time: ~5 minutes**

### Steps:

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 image-similarity

# Create environment
eb create image-similarity-env

# Deploy
eb deploy

# Open in browser
eb open
```

### Cost: **FREE tier available** (~1GB memory), then ~$10-20/month

---

## Option 6: Vercel (Serverless)

⚠️ **Note**: Vercel is optimized for Node.js/Next.js
Python functions have limitations. Not recommended for this app.

---

## Post-Deployment Verification

After deployment, verify your app is working:

```bash
# Health check
curl https://your-deployed-app.com/health

# Expected response:
# {"status":"healthy"}
```

### Test Upload:

```bash
# Using curl (Windows: use PowerShell)
curl -X POST \
  -F "image1=@path/to/image1.jpg" \
  -F "image2=@path/to/image2.jpg" \
  https://your-deployed-app.com/compare
```

---

## Monitoring & Logs

### Railway
- Dashboard → Your Project → Deployments → Logs

### Render
- Dashboard → Your Service → Logs

### Docker VPS
```bash
docker logs container-id
docker logs -f container-id  # Follow logs
```

---

## Troubleshooting

### "Build Failed" Error

**Railway/Render**:
1. Check `requirements.txt` format
2. Verify Python version compatibility
3. Check build logs for detailed error

```bash
# Test locally first
pip install -r requirements.txt
python app.py
```

### "Out of Memory" Error

1. Reduce worker processes in Procfile:
   ```
   web: gunicorn --bind 0.0.0.0:$PORT --workers 1 app:app
   ```

2. Reduce max image size in `app.py`:
   ```python
   MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB instead of 10MB
   ```

### "Port Already in Use" (Local)

```bash
# Find and kill process
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :5000
kill -9 <PID>
```

### Slow Comparison (>10 seconds)

1. Check server resources
2. Reduce image processing size
3. Edit `app.py`:
   ```python
   def resize_images(img1, img2, max_size=256):  # Reduce from 512
   ```

---

## Performance Optimization

### Reduce Cold Start Time
- Pre-compile Python packages
- Use lightweight base image (already done)

### Reduce Memory Usage
```bash
# Remove unnecessary packages
pip uninstall -r unneeded.txt

# Use OpenCV headless
pip install opencv-python-headless
```

### Increase Concurrency
```
# Procfile
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --threads 2 app:app
```

---

## Cost Comparison

| Platform | Free Tier | Paid | Speed |
|----------|-----------|------|-------|
| Railway | 500 hrs/mo | $5+ | ⚡⚡ |
| Render | Limited | $7+ | ⚡ |
| Heroku | ❌ Removed | $50+ | ⚡⚡ |
| DigitalOcean | ❌ | $5+ | ⚡⚡⚡ |
| AWS | 1 year free | $10+ | ⚡⚡⚡ |

**Recommendation**: Start with **Railway** (free, reliable, fast)

---

## Custom Domain

### Railway
- Settings → Domains → Add Domain
- Configure DNS: Railway provides instructions

### Render
- Settings → Rewrites/Redirects → Add Custom Domain
- Configure DNS

### Steps:
1. Register domain (Namecheap, GoDaddy, etc.)
2. Point DNS to provider
3. Add to deployment platform

---

## SSL/HTTPS

All platforms provide **free SSL by default**. ✅

No additional configuration needed!

---

## Scaling Tips

If traffic increases:

1. **Horizontal**: More instances
   - Railway: Scale → Increase replicas
   - Render: Scale to 2+ instances

2. **Vertical**: Bigger instance
   - Railway: Change plan
   - Render: Use paid tier

3. **Caching**: Cache comparison results
   - Add Redis support
   - Cache identical uploads

4. **Optimization**: 
   - Reduce algorithm complexity
   - Use image compression
   - Implement rate limiting

---

## Maintenance

- Monitor error logs weekly
- Update dependencies monthly:
  ```bash
  pip list --outdated
  pip install --upgrade package-name
  ```
- Test locally before deploying:
  ```bash
  pip install -r requirements.txt
  python app.py
  ```

---

**Happy Deploying! 🚀**
