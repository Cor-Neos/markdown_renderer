"""
Unit tests for FileHandler
"""
import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    """Test cases for FileHandler"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.handler = FileHandler()
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.md")
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    def test_new_file(self):
        """Test creating a new file"""
        self.handler.new_file()
        
        self.assertIsNone(self.handler.current_file)
        self.assertEqual(self.handler.current_content, "")
        self.assertFalse(self.handler.is_modified)
    
    def test_save_new_file(self):
        """Test saving a new file"""
        content = "# Test\n\nThis is test content."
        success, error = self.handler.save_file(content, self.test_file)
        
        self.assertTrue(success)
        self.assertEqual(error, "")
        self.assertTrue(os.path.exists(self.test_file))
        
        # Read back and verify
        with open(self.test_file, 'r') as f:
            saved_content = f.read()
        self.assertEqual(saved_content, content)
    
    def test_open_file(self):
        """Test opening an existing file"""
        # Create a test file
        content = "# Test Content\n\nSome text here."
        with open(self.test_file, 'w') as f:
            f.write(content)
        
        # Open the file
        success, read_content, error = self.handler.open_file(self.test_file)
        
        self.assertTrue(success)
        self.assertEqual(read_content, content)
        self.assertEqual(error, "")
        self.assertFalse(self.handler.is_modified)
    
    def test_open_nonexistent_file(self):
        """Test opening a file that doesn't exist"""
        success, content, error = self.handler.open_file("/nonexistent/file.md")
        
        self.assertFalse(success)
        self.assertEqual(content, "")
        self.assertIn("not found", error.lower())
    
    def test_set_modified(self):
        """Test setting modified flag"""
        self.handler.set_modified(True)
        self.assertTrue(self.handler.is_modified)
        
        self.handler.set_modified(False)
        self.assertFalse(self.handler.is_modified)
    
    def test_get_current_file_name(self):
        """Test getting current file name"""
        # No file opened
        self.assertEqual(self.handler.get_current_file_name(), "Untitled")
        
        # After saving
        self.handler.save_file("test", self.test_file)
        self.assertEqual(self.handler.get_current_file_name(), "test.md")
    
    def test_is_markdown_file(self):
        """Test markdown file detection"""
        self.assertTrue(FileHandler.is_markdown_file("test.md"))
        self.assertTrue(FileHandler.is_markdown_file("test.markdown"))
        self.assertTrue(FileHandler.is_markdown_file("test.mdown"))
        self.assertFalse(FileHandler.is_markdown_file("test.txt"))
        self.assertFalse(FileHandler.is_markdown_file("test.html"))

if __name__ == '__main__':
    unittest.main()
