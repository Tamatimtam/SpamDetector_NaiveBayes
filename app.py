from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from utils import is_safe_file, sanitize_content, get_safe_filename
import pickle
import os

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5000", "https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Configure maximum request size (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Load model and vectorizer
with open('spam_model.pkl', 'rb') as f:
    model = pickle.load(f)
    
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

def predict_spam(text):
    # Transform text using vectorizer
    text_count = vectorizer.transform([text])
    # Make prediction
    prediction = model.predict(text_count)
    # Get probability scores
    proba = model.predict_proba(text_count)
    return prediction[0], proba[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_text', methods=['POST'])
@limiter.limit("10 per minute")
def check_text():
    if not request.form.get('text'):
        return jsonify({'error': 'No text provided'}), 400
    
    text = request.form['text']
    if len(text) > 100000:  # Limit text length
        return jsonify({'error': 'Text too long'}), 400

    prediction, proba = predict_spam(text)
    is_spam = bool(prediction)
    confidence = proba[1] if is_spam else proba[0]
    return jsonify({
        'is_spam': is_spam,
        'confidence': float(confidence),
        'message': 'Spam' if is_spam else 'Not Spam'
    })

@app.route('/check_file', methods=['POST'])
@limiter.limit("5 per minute")
def check_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Sanitize filename
    filename = get_safe_filename(file.filename)
    
    # Check file extension
    allowed_extensions = {'txt', 'doc', 'docx'}
    if not '.' in filename or \
       filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        # Validate file content type
        if not is_safe_file(file):
            return jsonify({'error': 'Invalid file content'}), 400
            
        # Read and sanitize content
        text = file.read().decode('utf-8')
        text = sanitize_content(text)
        
        if len(text) > 100000:  # Limit file content length
            return jsonify({'error': 'File content too long'}), 400
        
        if not text.strip():  # Check if content is empty after sanitization
            return jsonify({'error': 'File contains no valid content'}), 400
            
        prediction, proba = predict_spam(text)
        is_spam = bool(prediction)
        confidence = proba[1] if is_spam else proba[0]
        return jsonify({
            'is_spam': is_spam,
            'confidence': float(confidence),
            'message': 'Spam' if is_spam else 'Not Spam'
        })
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 400

# Error handlers
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large'}), 413

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded'}), 429

if __name__ == '__main__':
    app.run(debug=True)
