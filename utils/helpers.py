"""
Helper utility functions
"""
from pathlib import Path
from typing import Optional
import re

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    return filename

def get_file_size_str(size_bytes: int) -> str:
    """
    Convert bytes to human-readable string
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def extract_title_from_markdown(markdown_text: str) -> Optional[str]:
    """
    Extract title from markdown (first H1 heading)
    
    Args:
        markdown_text: Markdown content
        
    Returns:
        Title text or None
    """
    # Look for first H1 heading
    match = re.search(r'^#\s+(.+)$', markdown_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None

def count_reading_time(markdown_text: str, words_per_minute: int = 200) -> int:
    """
    Calculate estimated reading time in minutes
    
    Args:
        markdown_text: Markdown content
        words_per_minute: Average reading speed
        
    Returns:
        Estimated reading time in minutes
    """
    # Count words
    words = len(re.findall(r'\b\w+\b', markdown_text))
    
    # Calculate time
    minutes = max(1, round(words / words_per_minute))
    
    return minutes

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def ensure_file_extension(filename: str, extension: str) -> str:
    """
    Ensure filename has the correct extension
    
    Args:
        filename: Original filename
        extension: Required extension (with or without dot)
        
    Returns:
        Filename with correct extension
    """
    if not extension.startswith('.'):
        extension = '.' + extension
    
    path = Path(filename)
    if path.suffix.lower() != extension.lower():
        return str(path.with_suffix(extension))
    
    return filename

def is_valid_url(url: str) -> bool:
    """
    Check if a string is a valid URL
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid URL
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

def format_timestamp(timestamp: float) -> str:
    """
    Format Unix timestamp to readable string
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Formatted date/time string
    """
    from datetime import datetime
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def create_backup_filename(original_path: str) -> str:
    """
    Create a backup filename
    
    Args:
        original_path: Original file path
        
    Returns:
        Backup file path
    """
    from datetime import datetime
    
    path = Path(original_path)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{path.stem}_backup_{timestamp}{path.suffix}"
    
    return str(path.parent / backup_name)
