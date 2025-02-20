# 🛡️ Email Spam Guardian
    
A modern, AI-powered spam detection service that helps keep your inbox clean and secure!

![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=flat-square&logo=flask)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)

## ✨ Features

- 🤖 Machine Learning-based spam detection
- 📝 Text analysis support
- 📎 File upload capabilities (txt, doc, docx)
- 🎨 Beautiful responsive UI with dark mode
- 🔒 Built-in security features
- ⚡ Real-time analysis
- 📊 Confidence scoring

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/email-spam-guardian.git
cd email-spam-guardian
```

2. Build and run with Docker:
```bash
docker build -t spam-guardian .
docker run -p 8080:8080 spam-guardian
```

Or run locally:
```bash
pip install -r requirements.txt
python app.py
```

3. Visit `http://localhost:8080` in your browser

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Flask
- **ML Model**: Naive Bayes
- **Security**: Flask-Limiter, python-magic
- **Containerization**: Docker

## 🔒 Security Features

- Rate limiting
- File type validation
- Content sanitization
- Size restrictions
- CORS protection

## 📊 API Endpoints

- `GET /` - Web interface
- `POST /check_text` - Analyze text content
- `POST /check_file` - Analyze file content

## 🤝 Contributing

Feel free to open issues and submit pull requests!

## 📜 License

MIT License - feel free to use this project for learning and development!

## 👨‍💻 Author

Pratama Varian Andika Parulian  
Student ID: 2207421040  
Politeknik Negeri Jakarta

---
Made with ❤️ and lots of ☕