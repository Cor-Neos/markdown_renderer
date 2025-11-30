"""
Markdown to HTML processor with extensions support
"""
import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re
from typing import Optional
import config

class MarkdownProcessor:
    """Process Markdown text and convert to HTML"""
    
    def __init__(self):
        """Initialize the Markdown processor with extensions"""
        self.md = markdown.Markdown(
            extensions=config.MARKDOWN_EXTENSIONS,
            extension_configs=config.MARKDOWN_EXTENSION_CONFIGS,
            output_format='html5'
        )
    
    def convert(self, markdown_text: str, theme_css: str = "") -> str:
        """
        Convert Markdown text to HTML with theme styling
        
        Args:
            markdown_text: The Markdown content to convert
            theme_css: CSS styling to apply to the HTML
            
        Returns:
            Complete HTML document with styling
        """
        # Reset the parser to clear previous state
        self.md.reset()
        
        # Convert markdown to HTML
        html_content = self.md.convert(markdown_text)
        
        # Get table of contents if generated
        toc = ""
        if hasattr(self.md, 'toc'):
            toc = f'<div class="toc">{self.md.toc}</div>'
        
        # Build complete HTML document
        full_html = self._build_html_document(html_content, toc, theme_css)
        
        return full_html
    
    def _build_html_document(self, content: str, toc: str, theme_css: str) -> str:
        """
        Build a complete HTML document with CSS and content
        
        Args:
            content: The HTML content
            toc: Table of contents HTML
            theme_css: CSS styling
            
        Returns:
            Complete HTML document as string
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Preview</title>
    <style>
        {theme_css}
        
        /* Base styles */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
        }}
        
        /* Code block styling */
        .codehilite, .highlight {{
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            margin: 1em 0;
        }}
        
        code {{
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        /* Inline code */
        p code, li code {{
            background-color: rgba(175, 184, 193, 0.2);
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }}
        
        /* Table styling */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        
        table th, table td {{
            border: 1px solid #dfe2e5;
            padding: 6px 13px;
        }}
        
        table tr:nth-child(2n) {{
            background-color: #f6f8fa;
        }}
        
        /* Task list styling */
        .task-list-item {{
            list-style-type: none;
        }}
        
        .task-list-item input[type="checkbox"] {{
            margin-right: 0.5em;
        }}
        
        /* Blockquote styling */
        blockquote {{
            border-left: 4px solid #dfe2e5;
            color: #6a737d;
            padding-left: 1em;
            margin-left: 0;
        }}
        
        /* Link styling */
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        /* Heading anchors */
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        
        h1 {{
            font-size: 2em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        
        h2 {{
            font-size: 1.5em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        
        /* TOC styling */
        .toc {{
            background-color: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 16px;
        }}
        
        .toc ul {{
            list-style-type: none;
            padding-left: 1em;
        }}
        
        /* Image styling */
        img {{
            max-width: 100%;
            height: auto;
        }}
        
        /* Horizontal rule */
        hr {{
            border: 0;
            border-top: 1px solid #e1e4e8;
            margin: 24px 0;
        }}
        
        /* Mark/highlight */
        mark {{
            background-color: #fff3cd;
            padding: 0.1em 0.2em;
        }}
        
        /* Keyboard keys */
        kbd {{
            display: inline-block;
            padding: 3px 5px;
            font-size: 0.85em;
            line-height: 1;
            color: #444d56;
            vertical-align: middle;
            background-color: #fafbfc;
            border: 1px solid #d1d5da;
            border-radius: 3px;
            box-shadow: inset 0 -1px 0 #d1d5da;
        }}
    </style>
    
    <!-- Mermaid for diagrams -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
</head>
<body>
    {toc}
    {content}
</body>
</html>"""
        return html
    
    def get_statistics(self, markdown_text: str) -> dict:
        """
        Calculate statistics about the markdown content
        
        Args:
            markdown_text: The markdown content to analyze
            
        Returns:
            Dictionary with statistics (words, characters, lines, etc.)
        """
        lines = markdown_text.split('\n')
        words = len(re.findall(r'\b\w+\b', markdown_text))
        characters = len(markdown_text)
        characters_no_spaces = len(markdown_text.replace(' ', '').replace('\n', ''))
        
        # Count headings
        headings = len(re.findall(r'^#{1,6}\s+.+$', markdown_text, re.MULTILINE))
        
        # Count code blocks
        code_blocks = len(re.findall(r'```[\s\S]*?```', markdown_text))
        
        # Count links
        links = len(re.findall(r'\[.*?\]\(.*?\)', markdown_text))
        
        # Count images
        images = len(re.findall(r'!\[.*?\]\(.*?\)', markdown_text))
        
        return {
            'lines': len(lines),
            'words': words,
            'characters': characters,
            'characters_no_spaces': characters_no_spaces,
            'headings': headings,
            'code_blocks': code_blocks,
            'links': links,
            'images': images,
        }
    
    def extract_toc(self, markdown_text: str) -> list:
        """
        Extract table of contents from markdown text
        
        Args:
            markdown_text: The markdown content
            
        Returns:
            List of tuples (level, title, anchor)
        """
        toc = []
        for match in re.finditer(r'^(#{1,6})\s+(.+)$', markdown_text, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2).strip()
            # Create anchor from title
            anchor = re.sub(r'[^\w\s-]', '', title.lower())
            anchor = re.sub(r'[-\s]+', '-', anchor)
            toc.append((level, title, anchor))
        
        return toc
