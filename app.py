from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
import io
import os
from werkzeug.utils import secure_filename
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__, static_folder='.', static_url_path='/')
CORS(app)

# Configuration
UPLOAD_FOLDER = '/tmp/image_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_image(file_path):
    """Load image and convert to BGR"""
    img = cv2.imread(file_path)
    if img is None:
        raise ValueError("Failed to load image")
    return img


def resize_images(img1, img2, max_size=512):
    """Resize images to reasonable size for processing"""
    scale1 = max_size / max(img1.shape[:2])
    scale2 = max_size / max(img2.shape[:2])
    
    img1 = cv2.resize(img1, None, fx=min(scale1, 1), fy=min(scale1, 1))
    img2 = cv2.resize(img2, None, fx=min(scale2, 1), fy=min(scale2, 1))
    
    return img1, img2


def histogram_comparison(img1, img2):
    """
    Algorithm 1: Histogram Matching
    Quick color distribution comparison
    Returns: 0-1 similarity score
    """
    try:
        # Convert to HSV for better color comparison
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        
        # Calculate histograms
        hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 50], [0, 180, 0, 256])
        hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 50], [0, 180, 0, 256])
        
        # Normalize
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()
        
        # Compare using Bhattacharyya distance
        distance = cv2.compareHist(hist1.reshape(-1, 1), hist2.reshape(-1, 1), cv2.HISTCMP_BHATTACHARYYA)
        
        # Convert distance to similarity (0-1)
        similarity = np.exp(-distance)
        return float(np.clip(similarity, 0, 1))
    except Exception as e:
        print(f"Histogram comparison error: {e}")
        return 0.0


def ssim_comparison(img1, img2):
    """
    Algorithm 2: Structural Similarity (SSIM)
    Pixel-level structural matching
    Returns: 0-1 similarity score
    """
    try:
        from skimage.metrics import structural_similarity as ssim
        
        # Resize to same dimensions
        h = min(img1.shape[0], img2.shape[0])
        w = min(img1.shape[1], img2.shape[1])
        img1_resized = img1[:h, :w]
        img2_resized = img2[:h, :w]
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1_resized, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)
        
        # Calculate SSIM
        score, _ = ssim(gray1, gray2, full=True)
        return float(np.clip((score + 1) / 2, 0, 1))
    except Exception as e:
        print(f"SSIM comparison error: {e}")
        return 0.0


def sift_comparison(img1, img2):
    """
    Algorithm 3: SIFT Keypoint Matching
    Handles rotations, scaling, and viewpoint changes
    Returns: 0-1 similarity score
    """
    try:
        # Use SIFT detector
        sift = cv2.SIFT_create()
        
        # Find keypoints and descriptors
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        
        if des1 is None or des2 is None or len(kp1) == 0 or len(kp2) == 0:
            return 0.0
        
        # Match descriptors using FLANN
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        
        matches = flann.knnMatch(des1, des2, k=2)
        
        if not matches:
            return 0.0
        
        # Apply Lowe's ratio test
        good_matches = []
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)
        
        # Calculate similarity based on match ratio
        max_matches = max(len(kp1), len(kp2))
        if max_matches == 0:
            return 0.0
        
        similarity = len(good_matches) / max_matches
        return float(np.clip(similarity, 0, 1))
    except Exception as e:
        print(f"SIFT comparison error: {e}")
        return 0.0


def compare_images(img1_path, img2_path):
    """
    Main comparison function combining all three algorithms
    Weighted average: 40% histogram, 30% SSIM, 30% SIFT
    Returns: 0-1 similarity score
    """
    try:
        # Load images
        img1 = load_image(img1_path)
        img2 = load_image(img2_path)
        
        if img1 is None or img2 is None:
            raise ValueError("Failed to load images")
        
        # Resize for processing efficiency
        img1, img2 = resize_images(img1, img2, max_size=512)
        
        # Run all three algorithms
        histogram_score = histogram_comparison(img1, img2)
        ssim_score = ssim_comparison(img1, img2)
        sift_score = sift_comparison(img1, img2)
        
        # Weighted average (40% histogram, 30% SSIM, 30% SIFT)
        final_score = (
            0.40 * histogram_score +
            0.30 * ssim_score +
            0.30 * sift_score
        )
        
        return {
            'similarity': float(np.clip(final_score, 0, 1)),
            'histogram': float(np.clip(histogram_score, 0, 1)),
            'ssim': float(np.clip(ssim_score, 0, 1)),
            'sift': float(np.clip(sift_score, 0, 1))
        }
    except Exception as e:
        print(f"Comparison error: {e}")
        raise


@app.route('/', methods=['GET'])
def index():
    """Serve main page"""
    return send_from_directory('.', 'index.html')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/compare', methods=['POST'])
def compare():
    """
    Main comparison endpoint
    Expects: multipart/form-data with 'image1' and 'image2' files
    Returns: JSON with similarity score and component scores
    """
    try:
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({'error': 'Both image1 and image2 are required'}), 400
        
        file1 = request.files['image1']
        file2 = request.files['image2']
        
        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'Both files must have names'}), 400
        
        if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
            return jsonify({'error': 'Only image files (png, jpg, jpeg, gif, bmp, webp) are allowed'}), 400
        
        # Save files temporarily
        filename1 = secure_filename('temp1_' + file1.filename)
        filename2 = secure_filename('temp2_' + file2.filename)
        path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        path2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        
        file1.save(path1)
        file2.save(path2)
        
        # Compare images
        result = compare_images(path1, path2)
        
        # Cleanup
        try:
            os.remove(path1)
            os.remove(path2)
        except:
            pass
        
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large. Maximum size: 10MB'}), 413


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
