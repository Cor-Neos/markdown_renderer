"""
Preview pane component for rendering HTML
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl, pyqtSignal

class MarkdownPreview(QWidget):
    """Preview pane for rendering markdown as HTML"""
    
    linkClicked = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # Configure web view settings
        self._setup_web_view()
        
        # Initial content
        self.set_html("")
    
    def _setup_web_view(self):
        """Configure web view settings"""
        settings = self.web_view.settings()
        
        # Enable useful features
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
        
        # Set default font
        settings.setFontFamily(QWebEngineSettings.FontFamily.StandardFont, "Arial")
        settings.setFontSize(QWebEngineSettings.FontSize.DefaultFontSize, 16)
    
    def set_html(self, html_content: str, base_url: str = ""):
        """
        Set HTML content to display
        
        Args:
            html_content: HTML content to render
            base_url: Base URL for resolving relative links
        """
        if not html_content:
            # Show empty state
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                        color: #6a737d;
                        background-color: #ffffff;
                    }
                    .empty-state {
                        text-align: center;
                    }
                    .empty-state h2 {
                        font-size: 24px;
                        margin-bottom: 8px;
                        color: #24292e;
                    }
                    .empty-state p {
                        font-size: 14px;
                    }
                </style>
            </head>
            <body>
                <div class="empty-state">
                    <h2>👋 Welcome to Markdown Renderer</h2>
                    <p>Start typing in the editor to see a live preview</p>
                </div>
            </body>
            </html>
            """
        
        if base_url:
            self.web_view.setHtml(html_content, QUrl.fromLocalFile(base_url))
        else:
            self.web_view.setHtml(html_content)
    
    def zoom_in(self):
        """Increase zoom level"""
        current_zoom = self.web_view.zoomFactor()
        self.web_view.setZoomFactor(min(current_zoom + 0.1, 3.0))
    
    def zoom_out(self):
        """Decrease zoom level"""
        current_zoom = self.web_view.zoomFactor()
        self.web_view.setZoomFactor(max(current_zoom - 0.1, 0.3))
    
    def zoom_reset(self):
        """Reset zoom to 100%"""
        self.web_view.setZoomFactor(1.0)
    
    def get_zoom_factor(self) -> float:
        """Get current zoom factor"""
        return self.web_view.zoomFactor()
    
    def reload(self):
        """Reload the preview"""
        self.web_view.reload()
