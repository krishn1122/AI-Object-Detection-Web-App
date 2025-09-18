from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import requests
import os
import base64
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Configuration
BACKEND_URL = "http://localhost:8000"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# Create upload directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

@app.route('/')
def index():
    """Main page with upload form"""
    backend_status = check_backend_health()
    return render_template('index.html', backend_status=backend_status)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and object detection"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    confidence_threshold = float(request.form.get('confidence', 0.7))
    
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            # Check if backend is running
            if not check_backend_health():
                flash('Backend service is not available. Please start the FastAPI backend.')
                return redirect(url_for('index'))
            
            # Prepare file for API request
            files = {'file': (file.filename, file.stream, file.content_type)}
            data = {'confidence_threshold': confidence_threshold}
            
            # Send request to FastAPI backend
            response = requests.post(
                f"{BACKEND_URL}/detect",
                files=files,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return render_template('results.html', 
                                     result=result, 
                                     confidence_threshold=confidence_threshold)
            else:
                error_detail = response.json().get('detail', 'Unknown error')
                flash(f'Error processing image: {error_detail}')
                return redirect(url_for('index'))
                
        except requests.exceptions.Timeout:
            flash('Request timed out. The image might be too large or the backend is busy.')
            return redirect(url_for('index'))
        except requests.exceptions.ConnectionError:
            flash('Cannot connect to backend service. Please ensure FastAPI backend is running.')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload an image file.')
        return redirect(url_for('index'))

@app.route('/batch-upload', methods=['POST'])
def batch_upload():
    """Handle multiple file upload"""
    if 'files' not in request.files:
        flash('No files selected')
        return redirect(url_for('index'))
    
    files = request.files.getlist('files')
    confidence_threshold = float(request.form.get('confidence', 0.7))
    
    if not files or all(f.filename == '' for f in files):
        flash('No files selected')
        return redirect(url_for('index'))
    
    # Filter valid files
    valid_files = [f for f in files if f and allowed_file(f.filename)]
    
    if not valid_files:
        flash('No valid image files found')
        return redirect(url_for('index'))
    
    try:
        # Check if backend is running
        if not check_backend_health():
            flash('Backend service is not available. Please start the FastAPI backend.')
            return redirect(url_for('index'))
        
        # Prepare files for API request
        files_data = []
        for f in valid_files:
            files_data.append(('files', (f.filename, f.stream, f.content_type)))
        
        data = {'confidence_threshold': confidence_threshold}
        
        # Send batch request to FastAPI backend
        response = requests.post(
            f"{BACKEND_URL}/detect-batch",
            files=files_data,
            data=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return render_template('batch_results.html', 
                                 result=result, 
                                 confidence_threshold=confidence_threshold)
        else:
            error_detail = response.json().get('detail', 'Unknown error')
            flash(f'Error processing images: {error_detail}')
            return redirect(url_for('index'))
            
    except requests.exceptions.Timeout:
        flash('Request timed out. Try uploading fewer or smaller images.')
        return redirect(url_for('index'))
    except requests.exceptions.ConnectionError:
        flash('Cannot connect to backend service. Please ensure FastAPI backend is running.')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/api/status')
def api_status():
    """API endpoint to check backend status"""
    backend_status = check_backend_health()
    return jsonify({
        'backend_available': backend_status,
        'frontend_status': 'running'
    })

@app.errorhandler(413)
def too_large(e):
    flash("File is too large. Please upload a smaller image.")
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(e):
    flash("An internal error occurred. Please try again.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
