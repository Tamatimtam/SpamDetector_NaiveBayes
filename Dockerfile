FROM python:3.9-slim

# Install system dependencies for python-magic
RUN apt-get update && apt-get install -y \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -r appuser

# Create and set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set proper permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080

# Expose portt
EXPOSE 8080

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
