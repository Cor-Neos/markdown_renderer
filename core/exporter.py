"""
Export functionality for converting markdown to various formats
"""
from pathlib import Path
from typing import Optional
from datetime import datetime
import config

# Try to import weasyprint, but make it optional
try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False

class Exporter:
    """Handle exporting markdown to various formats"""
    
    def __init__(self, markdown_processor):
        """
        Initialize exporter
        
        Args:
            markdown_processor: MarkdownProcessor instance for HTML conversion
        """
        self.markdown_processor = markdown_processor
    
    def export_html(self, markdown_content: str, output_path: str, 
                   theme_css: str = "", standalone: bool = True) -> tuple[bool, str]:
        """
        Export markdown to HTML file
        
        Args:
            markdown_content: Markdown text to export
            output_path: Path to save HTML file
            theme_css: CSS theme to apply
            standalone: Whether to create standalone HTML document
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Convert markdown to HTML
            if standalone:
                html_content = self.markdown_processor.convert(markdown_content, theme_css)
            else:
                # Just the HTML content without full document structure
                self.markdown_processor.md.reset()
                html_content = self.markdown_processor.md.convert(markdown_content)
            
            # Write to file
            output = Path(output_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True, ""
            
        except Exception as e:
            return False, f"Error exporting HTML: {str(e)}"
    
    def export_pdf(self, markdown_content: str, output_path: str, 
                   theme_css: str = "") -> tuple[bool, str]:
        """
        Export markdown to PDF file
        
        Args:
            markdown_content: Markdown text to export
            output_path: Path to save PDF file
            theme_css: CSS theme to apply
            
        Returns:
            Tuple of (success, error_message)
        """
        if not WEASYPRINT_AVAILABLE:
            return False, (
                "PDF export requires WeasyPrint and GTK libraries.\n\n"
                "On Windows, this requires additional system dependencies:\n"
                "1. Download GTK3 from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases\n"
                "2. Run the installer\n"
                "3. Restart the application\n\n"
                "Alternative: Export as HTML and use your browser to 'Print to PDF'"
            )
        
        try:
            # Convert markdown to HTML
            html_content = self.markdown_processor.convert(markdown_content, theme_css)
            
            # Enhance CSS for PDF
            pdf_css = self._get_pdf_css()
            html_with_pdf_css = html_content.replace('</style>', f'{pdf_css}</style>')
            
            # Create output directory if needed
            output = Path(output_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert HTML to PDF using weasyprint
            html_document = weasyprint.HTML(string=html_with_pdf_css)
            html_document.write_pdf(output)
            
            return True, ""
            
        except Exception as e:
            return False, f"Error exporting PDF: {str(e)}"
    
    def _get_pdf_css(self) -> str:
        """
        Get additional CSS for PDF export
        
        Returns:
            CSS string for PDF formatting
        """
        return """
        /* PDF-specific styles */
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            max-width: 100%;
        }
        
        /* Avoid page breaks inside elements */
        h1, h2, h3, h4, h5, h6 {
            page-break-after: avoid;
        }
        
        pre, blockquote, table {
            page-break-inside: avoid;
        }
        
        img {
            page-break-inside: avoid;
            max-width: 100%;
        }
        
        /* Print links */
        a[href]:after {
            content: " (" attr(href) ")";
            font-size: 0.8em;
            color: #666;
        }
        
        a[href^="#"]:after {
            content: "";
        }
        """
    
    def export_markdown_copy(self, markdown_content: str, output_path: str) -> tuple[bool, str]:
        """
        Export/copy markdown to another file
        
        Args:
            markdown_content: Markdown text to export
            output_path: Path to save markdown file
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            output = Path(output_path)
            output.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return True, ""
            
        except Exception as e:
            return False, f"Error exporting markdown: {str(e)}"
    
    def get_export_metadata(self, markdown_content: str) -> dict:
        """
        Get metadata about the export
        
        Args:
            markdown_content: Markdown content
            
        Returns:
            Dictionary with export metadata
        """
        stats = self.markdown_processor.get_statistics(markdown_content)
        return {
            'timestamp': datetime.now().isoformat(),
            'statistics': stats,
            'version': config.APP_VERSION,
        }
