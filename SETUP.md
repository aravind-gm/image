# 📋 Setup & Usage Guide

## Prerequisites

- Python 3.9+ (recommended: 3.11)
- pip (comes with Python)
- 500MB free disk space
- Modern web browser

## Quick Setup (Choose One)

### ⚡ Fastest: Using Provided Scripts

**Windows**:
```bash
start.bat
```

**Linux/Mac**:
```bash
chmod +x start.sh
./start.sh
```

Then open `http://localhost:5000` in your browser.

---

### 📖 Manual Setup

#### 1. Clone/Download Project
```bash
git clone <your-repo-url>
cd image-similarity
```

Or download ZIP and extract.

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected output**:
```
Successfully installed Flask-2.3.3 flask-cors-4.0.0 opencv-python-4.8.1.78 ...
```

**Time**: 3-5 minutes on first install

#### 4. Run Application
```bash
python app.py
```

**Expected output**:
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://0.0.0.0:5000
```

#### 5. Open Browser
Navigate to: `http://localhost:5000`

---

## Usage

### Basic Workflow

1. **Upload Image 1**
   - Drag & drop or click "Image 1" box
   - Supported: PNG, JPG, JPEG, GIF, BMP, WebP
   - Max size: 10MB
   - See preview immediately

2. **Upload Image 2**
   - Same process as Image 1
   - "Compare Images" button enables when both loaded

3. **Compare**
   - Click "Compare Images" button
   - Wait for analysis (typically 1-3 seconds)
   - View similarity score and algorithm breakdown

4. **Interpret Results**
   - **Similarity Score**: 0-100% overall match
   - **Color Histogram**: Color distribution similarity
   - **Structural (SSIM)**: Pixel-level structure match
   - **Feature Match (SIFT)**: Keypoint correspondence

5. **Reset**
   - Click "Reset" to clear and start over
   - Or individually clear using "Clear" buttons

### Score Interpretation

| Score | Meaning |
|-------|---------|
| 90-100% | Nearly identical images |
| 70-90% | Very similar (minor differences) |
| 50-70% | Moderately similar |
| 30-50% | Some similarity |
| 0-30% | Completely different |

---

## Keyboard Shortcuts

- **Enter**: Compare (when both images loaded)
- **Escape**: Clear error messages
- **R**: Reset (not default, can be added to code)

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'cv2'"

**Solution**:
```bash
# Ensure virtual environment is activated, then:
pip install --upgrade opencv-python
```

### "Port 5000 already in use"

**Windows**:
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Linux/Mac**:
```bash
lsof -i :5000
kill -9 <PID>
```

Or use different port:
```bash
# Edit app.py, line ~167:
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
```

### Comparison takes >10 seconds

**Causes**:
1. Large images (>1000×1000)
2. Complex images with many features
3. Low system RAM

**Solutions**:
- Use smaller images
- Close other applications
- Reduce image resolution before upload
- Edit `app.py` max_size parameter:
  ```python
  def resize_images(img1, img2, max_size=256):  # Reduce from 512
  ```

### "Failed to load image"

**Causes**:
1. Corrupted file
2. Unsupported format
3. File permission issue

**Solutions**:
- Try different image
- Verify format is supported
- Re-download image if corrupted

### "File too large" Error

Max size: 10MB. Reduce image size:

**Using Python**:
```python
from PIL import Image
img = Image.open('large_image.jpg')
img.thumbnail((1024, 1024))
img.save('small_image.jpg')
```

---

## Performance Tips

### For Faster Comparisons

1. **Smaller Images**: 
   - Resize to <800×800 pixels
   - Typical processing: 150-300ms

2. **Disable SIFT** (if not needed):
   - Edit `app.py` line ~108
   - Set `sift_score = 0.0`
   - Process time: ~50-100ms

3. **Increase Workers** (production):
   - Edit `Procfile`:
     ```
     web: gunicorn --workers 4 --threads 2 app:app
     ```

### For Better Accuracy

1. **Use High-Quality Images**:
   - Avoid compressed JPGs
   - Use PNG when possible
   - Ensure good lighting

2. **Properly Aligned Images**:
   - Similar orientation
   - Similar scale
   - Similar perspective

3. **Consider Algorithm Weights**:
   - Edit weights in `app.py` `compare_images()`:
     ```python
     # Adjust percentages as needed
     final_score = (0.50 * histogram + 0.25 * ssim + 0.25 * sift)
     ```

---

## Testing

### Manual Testing

1. **Test with identical images**:
   - Upload same image twice
   - Score should be ~95-100%

2. **Test with different images**:
   - Upload unrelated images
   - Score should be 0-20%

3. **Test with similar images**:
   - Upload photos of same object
   - Score should be 60-80%

### Automated Testing

```bash
python test.py
```

**Output**:
```
🧪 Testing Image Similarity Analyzer

Test 1: Identical Images
  Similarity: 100.00%
  ✓ Should be ~100% (actual: 100.00%)
...
✅ All tests completed!
```

---

## API Testing

### Using curl (Command Line)

```bash
curl -X POST \
  -F "image1=@/path/to/image1.jpg" \
  -F "image2=@/path/to/image2.jpg" \
  http://localhost:5000/compare
```

### Using Python

```python
import requests

files = {
    'image1': open('image1.jpg', 'rb'),
    'image2': open('image2.jpg', 'rb')
}

response = requests.post('http://localhost:5000/compare', files=files)
print(response.json())

# Output:
# {
#   "similarity": 0.75,
#   "histogram": 0.82,
#   "ssim": 0.68,
#   "sift": 0.73
# }
```

### Using JavaScript

```javascript
const formData = new FormData();
formData.append('image1', imageFile1);
formData.append('image2', imageFile2);

fetch('/compare', {
    method: 'POST',
    body: formData
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## Customization

### Change UI Colors

Edit `index.html`, find CSS section:

```css
/* Change primary color from purple to blue */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* To */
background: linear-gradient(135deg, #0066FF 0%, #0033CC 100%);
```

### Change Algorithm Weights

Edit `app.py`, `compare_images()` function:

```python
# Default (40% histogram, 30% SSIM, 30% SIFT)
final_score = (0.40 * histogram_score + 0.30 * ssim_score + 0.30 * sift_score)

# Favor color: (50% histogram, 25% SSIM, 25% SIFT)
final_score = (0.50 * histogram_score + 0.25 * ssim_score + 0.25 * sift_score)

# Favor structure: (30% histogram, 40% SSIM, 30% SIFT)
final_score = (0.30 * histogram_score + 0.40 * ssim_score + 0.30 * sift_score)
```

### Change Max File Size

Edit `app.py`:

```python
# Change from 10MB to 20MB
MAX_FILE_SIZE = 20 * 1024 * 1024
```

### Change Server Port

Edit `app.py`:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Changed from 5000
    app.run(debug=False, host='0.0.0.0', port=port)
```

---

## Production Deployment

### Before Deploying

1. **Test locally**:
   ```bash
   python app.py
   ```

2. **Run test suite**:
   ```bash
   python test.py
   ```

3. **Check dependencies**:
   ```bash
   pip freeze > requirements.txt
   ```

### Deploy to Railway (Recommended)

See `DEPLOYMENT.md` for detailed instructions.

Quick deploy:
```bash
git add .
git commit -m "Initial commit"
git push origin main

# Then connect to Railway via dashboard
```

---

## Monitoring & Logs

### Local (Development)

Console output shows:
```
 * Running on http://0.0.0.0:5000
 * Restarting with reloader
DEBUG:werkzeug:127.0.0.1 - - [date] "POST /compare HTTP/1.1"
```

### Production (Railway/Render)

Check logs in dashboard:
```
railway logs
# or
render logs
```

---

## Regular Maintenance

### Weekly
- Monitor error logs
- Check disk usage

### Monthly
- Update dependencies:
  ```bash
  pip list --outdated
  pip install --upgrade package-name
  ```

### Quarterly
- Test all algorithms
- Review and update documentation
- Performance analysis

---

## Getting Help

### Common Issues

- **Check README.md**: Features and overview
- **Check DEPLOYMENT.md**: Deployment instructions
- **Check test.py**: Algorithm testing
- **GitHub Issues**: Report bugs

### Debug Mode

Enable detailed logging:

```python
# Edit app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

⚠️ **Warning**: Never use debug=True in production!

---

## Next Steps

1. ✅ Run locally: `start.bat` (Windows) or `./start.sh` (Linux/Mac)
2. ✅ Test functionality
3. ✅ Deploy to cloud (Railway/Render)
4. ✅ Share with others
5. ✅ Customize as needed

---

**Happy comparing! 🔍**
