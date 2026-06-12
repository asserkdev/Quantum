"""
Quantum Utils - Helper functions
"""

import os
import re
import hashlib
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from urllib.parse import urlparse

def sanitize_text(text: str) -> str:
    """Sanitize text input"""
    if not text:
        return ""
    # Remove potentially harmful characters
    text = re.sub(r'[<>"\';]', '', text)
    return text.strip()

def validate_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return ""

def generate_id(prefix: str = "") -> str:
    """Generate unique ID"""
    timestamp = datetime.now().timestamp()
    hash_input = f"{timestamp}_{os.urandom(8).hex()}"
    hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:12]
    return f"{prefix}_{hash_value}" if prefix else hash_value

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)].strip() + suffix

def format_timestamp(timestamp: str = None, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format timestamp"""
    if not timestamp:
        timestamp = datetime.now()
    elif isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return timestamp.strftime(format_str)

def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """Extract keywords from text"""
    # Simple keyword extraction
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter short words and common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    keywords = [w for w in words if len(w) >= min_length and w not in stop_words]
    return list(set(keywords))

def parse_markdown(text: str) -> str:
    """Parse basic markdown to HTML"""
    if not text:
        return ""
    
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    # Line breaks
    text = text.replace('\n', '<br>')
    
    return text

def calculate_read_time(text: str, words_per_minute: int = 200) -> int:
    """Calculate estimated read time in minutes"""
    words = len(text.split())
    minutes = max(1, round(words / words_per_minute))
    return minutes

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks

def merge_dicts(*dicts: Dict) -> Dict:
    """Merge multiple dictionaries"""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result

def safe_get(dictionary: Dict, *keys, default: Any = None) -> Any:
    """Safely get nested dictionary value"""
    result = dictionary
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
        else:
            return default
        if result is None:
            return default
    return result

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def is_valid_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_valid_password(password: str) -> bool:
    """Check password strength"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

def get_file_extension(filename: str) -> str:
    """Get file extension"""
    return os.path.splitext(filename)[1].lower()

def is_image_file(filename: str) -> bool:
    """Check if file is an image"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
    return get_file_extension(filename) in image_extensions

def is_document_file(filename: str) -> bool:
    """Check if file is a document"""
    doc_extensions = {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'}
    return get_file_extension(filename) in doc_extensions

def rate_limit_key(identifier: str, action: str) -> str:
    """Generate rate limit key"""
    return f"rate_limit:{identifier}:{action}"

def cache_key(*args) -> str:
    """Generate cache key from arguments"""
    key_string = ":".join(str(arg) for arg in args)
    return hashlib.md5(key_string.encode()).hexdigest()

class Timer:
    """Simple timer context manager"""
    def __init__(self):
        self.start = None
        self.end = None
        self.elapsed = None
    
    def __enter__(self):
        self.start = datetime.now()
        return self
    
    def __exit__(self, *args):
        self.end = datetime.now()
        self.elapsed = (self.end - self.start).total_seconds()
    
    def __str__(self):
        if self.elapsed:
            return f"{self.elapsed:.3f}s"
        return "Not finished"

def log_interaction(user_id: str, action: str, details: Dict = None):
    """Log user interaction"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "action": action,
        "details": details or {}
    }
    # In production, this would write to a log file or database
    print(f"[LOG] {json.dumps(log_entry)}")