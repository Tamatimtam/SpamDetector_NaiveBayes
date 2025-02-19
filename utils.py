import magic
import os
import re
from werkzeug.utils import secure_filename

def is_safe_file(file_stream):
    """Check if file content appears to be safe"""
    # Get MIME type of file
    mime = magic.from_buffer(file_stream.read(2048), mime=True)
    file_stream.seek(0)  # Reset file pointer
    
    # Only allow text-based files
    allowed_mimes = {'text/plain', 'application/msword', 
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
    return mime in allowed_mimes

def sanitize_content(content):
    """Remove potentially dangerous content"""
    # Remove control characters except newlines and tabs
    content = ''.join(char for char in content if char == '\n' or char == '\t' or char.isprintable())
    
    # Remove any script tags
    content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.DOTALL)
    
    # Remove any HTML tags
    content = re.sub(r'<[^>]*>', '', content)
    
    return content.strip()

def get_safe_filename(filename):
    """Get sanitized filename"""
    return secure_filename(filename)
