# ⚡ Quick Reference Card

## 🚀 5-Minute Quick Start

### Windows
```cmd
start.bat
```

### Linux/Mac
```bash
./start.sh
```

### Manual
```bash
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
pip install -r requirements.txt
python app.py
```

**Then open:** `http://localhost:5000`

---

## 📱 Browser Usage

1. **Upload Image 1** → Drag & drop or click
2. **Upload Image 2** → Same process
3. **Compare** → Click button
4. **View Result** → Score + breakdown
5. **Reset** → Clear & start over

---

## 🌍 Deploy to Cloud

### Railway (⭐ Fastest - 1 min)
```bash
git add .
git commit -m "Initial"
git push
# Then: railway up
```

### Render (2-3 min)
- Go to render.com
- New Web Service
- Select repo
- Deploy

### Docker
```bash
docker build -t image-similarity .
docker run -p 5000:5000 image-similarity
```

---

## 📊 Score Meanings

| Score | Meaning |
|-------|---------|
| 90-100% | Nearly identical |
| 70-90% | Very similar |
| 50-70% | Moderately similar |
| 30-50% | Some similarity |
| 0-30% | Completely different |

---

## 🔧 Common Commands

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py

# Run tests
python test.py

# Test API
curl -X POST \
  -F "image1=@img1.jpg" \
  -F "image2=@img2.jpg" \
  http://localhost:5000/compare
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Backend server & algorithms |
| `index.html` | Frontend UI |
| `requirements.txt` | Python packages |
| `Dockerfile` | Container config |
| `Procfile` | Deployment config |
| `test.py` | Testing suite |

---

## 🆘 Troubleshooting

### "Port 5000 in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Comparison too slow"
- Use smaller images (<1MB)
- Disable SIFT in app.py
- Reduce max_size from 512 to 256

---

## 🎨 Customize

### Change Colors (index.html)
Find:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```
Replace hex codes with your colors

### Change Weights (app.py)
```python
final_score = (
    0.40 * histogram_score +   # Change this
    0.30 * ssim_score +        # Or this
    0.30 * sift_score          # Or this
)
```

### Change Max File Size (app.py)
```python
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB instead of 10MB
```

---

## 📊 Algorithms

| Algorithm | Speed | Use Case |
|-----------|-------|----------|
| Histogram | ⚡ 5ms | Color matching |
| SSIM | ⚡⚡ 20ms | Structure matching |
| SIFT | ⚡⚡⚡ 300ms | Feature matching |

---

## 💻 Requirements

- Python 3.9+ (recommended 3.11)
- 512MB RAM (free tier)
- 500MB disk space
- Modern browser

---

## 📚 Documentation

| File | Content |
|------|---------|
| `README.md` | Features & overview |
| `SETUP.md` | Installation guide |
| `DEPLOYMENT.md` | Cloud deployment |
| `OPTIMIZATION.md` | Performance tuning |
| `PROJECT_SUMMARY.md` | Complete overview |

---

## 🚀 Deployment Checklist

- [ ] Run locally: `python app.py`
- [ ] Test functionality: `python test.py`
- [ ] Push to GitHub: `git push`
- [ ] Deploy: Railway/Render/Docker
- [ ] Test cloud version
- [ ] Share URL with others

---

## 💰 Costs

| Platform | Free | Paid |
|----------|------|------|
| Railway | 500 hrs/mo | $5+/mo |
| Render | Limited | $7+/mo |
| VPS | ❌ | $5+/mo |
| Docker Hub | ✅ | $5+/mo |

---

## 🆔 API Endpoints

```
POST /compare
  Input: image1, image2 (multipart/form-data)
  Output: JSON with similarity scores

GET /health
  Output: {"status": "healthy"}
```

---

## ⚙️ Environment Variables

```bash
PORT=5000           # Server port
FLASK_ENV=prod      # Production mode
DEBUG=0             # No debug mode
```

---

## 🎯 Use Cases

- Quality control
- Duplicate detection
- Image search
- Content moderation
- Fashion e-commerce
- Medical imaging
- Art authentication

---

## 📈 Performance

- **Deploy Time**: <2 minutes
- **Response Time**: 300-400ms
- **Image Size**: ~95MB
- **Memory**: 100-200MB per request
- **Cold Start**: <2 seconds

---

## ✅ Status

```
Build:     ✅ Complete
Frontend:  ✅ Production-ready
Backend:   ✅ 3 algorithms
Docs:      ✅ Comprehensive
Deploy:    ✅ Ready
```

---

## 🎓 Learn

This project teaches:
- Flask web development
- Computer vision (OpenCV)
- Image processing algorithms
- REST API design
- Docker containerization
- Cloud deployment
- Modern web UI

---

**Start now: `start.bat` or `./start.sh`**

**Deploy now: Railway.app or Render.com**

**Questions? See README.md or SETUP.md**
