"""
Unit tests for MarkdownProcessor
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.markdown_processor import MarkdownProcessor

class TestMarkdownProcessor(unittest.TestCase):
    """Test cases for MarkdownProcessor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = MarkdownProcessor()
    
    def test_basic_conversion(self):
        """Test basic markdown to HTML conversion"""
        markdown = "# Hello World\n\nThis is a test."
        html = self.processor.convert(markdown)
        
        self.assertIn('<h1', html)
        self.assertIn('Hello World', html)
        self.assertIn('<p>', html)
        self.assertIn('This is a test.', html)
    
    def test_bold_text(self):
        """Test bold text conversion"""
        markdown = "**bold text**"
        html = self.processor.convert(markdown)
        
        self.assertIn('<strong>', html)
        self.assertIn('bold text', html)
    
    def test_italic_text(self):
        """Test italic text conversion"""
        markdown = "*italic text*"
        html = self.processor.convert(markdown)
        
        self.assertIn('<em>', html)
        self.assertIn('italic text', html)
    
    def test_code_block(self):
        """Test code block conversion"""
        markdown = "```python\nprint('Hello')\n```"
        html = self.processor.convert(markdown)
        
        self.assertIn('<code>', html)
        self.assertIn('print', html)
    
    def test_inline_code(self):
        """Test inline code conversion"""
        markdown = "Use `inline code` here"
        html = self.processor.convert(markdown)
        
        self.assertIn('<code>', html)
        self.assertIn('inline code', html)
    
    def test_link(self):
        """Test link conversion"""
        markdown = "[GitHub](https://github.com)"
        html = self.processor.convert(markdown)
        
        self.assertIn('<a', html)
        self.assertIn('href="https://github.com"', html)
        self.assertIn('GitHub', html)
    
    def test_list(self):
        """Test unordered list conversion"""
        markdown = "- Item 1\n- Item 2\n- Item 3"
        html = self.processor.convert(markdown)
        
        self.assertIn('<ul>', html)
        self.assertIn('<li>', html)
        self.assertIn('Item 1', html)
    
    def test_ordered_list(self):
        """Test ordered list conversion"""
        markdown = "1. First\n2. Second\n3. Third"
        html = self.processor.convert(markdown)
        
        self.assertIn('<ol>', html)
        self.assertIn('<li>', html)
        self.assertIn('First', html)
    
    def test_blockquote(self):
        """Test blockquote conversion"""
        markdown = "> This is a quote"
        html = self.processor.convert(markdown)
        
        self.assertIn('<blockquote>', html)
        self.assertIn('This is a quote', html)
    
    def test_statistics(self):
        """Test statistics calculation"""
        markdown = "# Title\n\nThis is a test with 10 words in total here."
        stats = self.processor.get_statistics(markdown)
        
        self.assertEqual(stats['lines'], 3)
        self.assertGreater(stats['words'], 0)
        self.assertGreater(stats['characters'], 0)
        self.assertEqual(stats['headings'], 1)
    
    def test_toc_extraction(self):
        """Test table of contents extraction"""
        markdown = "# Title 1\n## Title 2\n### Title 3"
        toc = self.processor.extract_toc(markdown)
        
        self.assertEqual(len(toc), 3)
        self.assertEqual(toc[0][0], 1)  # Level 1
        self.assertEqual(toc[1][0], 2)  # Level 2
        self.assertEqual(toc[2][0], 3)  # Level 3

if __name__ == '__main__':
    unittest.main()
