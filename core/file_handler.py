"""
File operations handler for opening, saving, and managing files
"""
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import config

class FileHandler:
    """Handle file I/O operations and recent files management"""
    
    def __init__(self):
        """Initialize the file handler"""
        self.current_file: Optional[Path] = None
        self.current_content: str = ""
        self.is_modified: bool = False
        self.last_saved: Optional[datetime] = None
    
    def open_file(self, file_path: str) -> tuple[bool, str, str]:
        """
        Open and read a file
        
        Args:
            file_path: Path to the file to open
            
        Returns:
            Tuple of (success, content, error_message)
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return False, "", f"File not found: {file_path}"
            
            if not path.is_file():
                return False, "", f"Not a file: {file_path}"
            
            # Read file content
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.current_file = path
            self.current_content = content
            self.is_modified = False
            self.last_saved = datetime.now()
            
            # Add to recent files
            self._add_to_recent_files(str(path))
            
            return True, content, ""
            
        except UnicodeDecodeError:
            return False, "", "Unable to decode file. File may not be a text file."
        except PermissionError:
            return False, "", f"Permission denied: {file_path}"
        except Exception as e:
            return False, "", f"Error opening file: {str(e)}"
    
    def save_file(self, content: str, file_path: Optional[str] = None) -> tuple[bool, str]:
        """
        Save content to file
        
        Args:
            content: Content to save
            file_path: Path to save to (uses current_file if None)
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Determine save path
            if file_path:
                path = Path(file_path)
            elif self.current_file:
                path = self.current_file
            else:
                return False, "No file path specified"
            
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.current_file = path
            self.current_content = content
            self.is_modified = False
            self.last_saved = datetime.now()
            
            # Add to recent files
            self._add_to_recent_files(str(path))
            
            return True, ""
            
        except PermissionError:
            return False, f"Permission denied: {path}"
        except Exception as e:
            return False, f"Error saving file: {str(e)}"
    
    def new_file(self):
        """Create a new file (clear current file state)"""
        self.current_file = None
        self.current_content = ""
        self.is_modified = False
        self.last_saved = None
    
    def set_modified(self, modified: bool = True):
        """Mark the current file as modified"""
        self.is_modified = modified
    
    def get_current_file_name(self) -> str:
        """Get the name of the current file"""
        if self.current_file:
            return self.current_file.name
        return "Untitled"
    
    def get_current_file_path(self) -> Optional[str]:
        """Get the full path of the current file"""
        if self.current_file:
            return str(self.current_file)
        return None
    
    def _add_to_recent_files(self, file_path: str):
        """
        Add a file to the recent files list
        
        Args:
            file_path: Path of the file to add
        """
        try:
            # Read existing recent files
            recent_files = self.get_recent_files()
            
            # Remove if already exists
            if file_path in recent_files:
                recent_files.remove(file_path)
            
            # Add to beginning
            recent_files.insert(0, file_path)
            
            # Limit to max recent files
            recent_files = recent_files[:config.MAX_RECENT_FILES]
            
            # Write back
            with open(config.RECENT_FILES_FILE, 'w', encoding='utf-8') as f:
                f.write('\n'.join(recent_files))
                
        except Exception as e:
            # Silently fail for recent files
            print(f"Warning: Could not update recent files: {e}")
    
    def get_recent_files(self) -> List[str]:
        """
        Get list of recent files
        
        Returns:
            List of file paths
        """
        try:
            if not config.RECENT_FILES_FILE.exists():
                return []
            
            with open(config.RECENT_FILES_FILE, 'r', encoding='utf-8') as f:
                files = [line.strip() for line in f.readlines() if line.strip()]
            
            # Filter out non-existent files
            existing_files = [f for f in files if Path(f).exists()]
            
            # Update the file if we removed any
            if len(existing_files) != len(files):
                with open(config.RECENT_FILES_FILE, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(existing_files))
            
            return existing_files
            
        except Exception:
            return []
    
    def clear_recent_files(self):
        """Clear the recent files list"""
        try:
            config.RECENT_FILES_FILE.unlink(missing_ok=True)
        except Exception:
            pass
    
    @staticmethod
    def is_markdown_file(file_path: str) -> bool:
        """
        Check if a file is a markdown file based on extension
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file has markdown extension
        """
        markdown_extensions = {'.md', '.markdown', '.mdown', '.mkd', '.mkdn', '.mdwn', '.mdtxt', '.mdtext'}
        return Path(file_path).suffix.lower() in markdown_extensions
