from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

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
def check_text():
    text = request.form['text']
    prediction, proba = predict_spam(text)
    is_spam = bool(prediction)
    confidence = proba[1] if is_spam else proba[0]
    return jsonify({
        'is_spam': is_spam,
        'confidence': float(confidence),
        'message': 'Spam' if is_spam else 'Not Spam'
    })

@app.route('/check_file', methods=['POST'])
def check_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    try:
        text = file.read().decode('utf-8')
        prediction, proba = predict_spam(text)
        is_spam = bool(prediction)
        confidence = proba[1] if is_spam else proba[0]
        return jsonify({
            'is_spam': is_spam,
            'confidence': float(confidence),
            'message': 'Spam' if is_spam else 'Not Spam'
        })
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
