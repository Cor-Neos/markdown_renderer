"""
Theme management for preview pane styling
"""
from pathlib import Path
from typing import Dict, Optional
import config

class ThemeManager:
    """Manage CSS themes for markdown preview"""
    
    def __init__(self):
        """Initialize theme manager"""
        self.current_theme = config.DEFAULT_THEME
        self.themes: Dict[str, str] = {}
        self._load_builtin_themes()
    
    def _load_builtin_themes(self):
        """Load built-in CSS themes"""
        
        # GitHub Theme (light)
        self.themes['github'] = """
        body {
            background-color: #ffffff;
            color: #24292e;
        }
        a { color: #0366d6; }
        code {
            background-color: rgba(27, 31, 35, 0.05);
            color: #24292e;
        }
        .codehilite, .highlight {
            background-color: #f6f8fa;
        }
        blockquote {
            color: #6a737d;
            border-left-color: #dfe2e5;
        }
        table th, table td {
            border-color: #dfe2e5;
        }
        table tr:nth-child(2n) {
            background-color: #f6f8fa;
        }
        h1, h2 {
            border-bottom-color: #eaecef;
        }
        """
        
        # Dark Theme
        self.themes['dark'] = """
        body {
            background-color: #0d1117;
            color: #c9d1d9;
        }
        a { color: #58a6ff; }
        code {
            background-color: rgba(110, 118, 129, 0.4);
            color: #c9d1d9;
        }
        .codehilite, .highlight {
            background-color: #161b22;
        }
        blockquote {
            color: #8b949e;
            border-left-color: #30363d;
        }
        table th, table td {
            border-color: #30363d;
        }
        table tr:nth-child(2n) {
            background-color: #161b22;
        }
        h1, h2 {
            border-bottom-color: #21262d;
        }
        hr {
            border-top-color: #30363d;
        }
        .toc {
            background-color: #161b22;
            border-color: #30363d;
        }
        """
        
        # Solarized Light
        self.themes['solarized-light'] = """
        body {
            background-color: #fdf6e3;
            color: #657b83;
        }
        a { color: #268bd2; }
        code {
            background-color: #eee8d5;
            color: #657b83;
        }
        .codehilite, .highlight {
            background-color: #eee8d5;
        }
        blockquote {
            color: #93a1a1;
            border-left-color: #eee8d5;
        }
        table th, table td {
            border-color: #eee8d5;
        }
        table tr:nth-child(2n) {
            background-color: #eee8d5;
        }
        h1, h2 {
            color: #586e75;
            border-bottom-color: #eee8d5;
        }
        hr {
            border-top-color: #eee8d5;
        }
        .toc {
            background-color: #eee8d5;
            border-color: #93a1a1;
        }
        """
        
        # Solarized Dark
        self.themes['solarized-dark'] = """
        body {
            background-color: #002b36;
            color: #839496;
        }
        a { color: #268bd2; }
        code {
            background-color: #073642;
            color: #839496;
        }
        .codehilite, .highlight {
            background-color: #073642;
        }
        blockquote {
            color: #586e75;
            border-left-color: #073642;
        }
        table th, table td {
            border-color: #073642;
        }
        table tr:nth-child(2n) {
            background-color: #073642;
        }
        h1, h2 {
            color: #93a1a1;
            border-bottom-color: #073642;
        }
        hr {
            border-top-color: #073642;
        }
        .toc {
            background-color: #073642;
            border-color: #586e75;
        }
        """
    
    def get_theme_css(self, theme_name: Optional[str] = None) -> str:
        """
        Get CSS for a specific theme
        
        Args:
            theme_name: Name of theme (uses current if None)
            
        Returns:
            CSS string for the theme
        """
        if theme_name is None:
            theme_name = self.current_theme
        
        return self.themes.get(theme_name, self.themes['github'])
    
    def set_theme(self, theme_name: str):
        """
        Set the current theme
        
        Args:
            theme_name: Name of theme to set
        """
        if theme_name in self.themes:
            self.current_theme = theme_name
    
    def get_available_themes(self) -> list:
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def load_custom_theme(self, name: str, css_content: str):
        """
        Load a custom theme from CSS content
        
        Args:
            name: Name for the custom theme
            css_content: CSS content
        """
        self.themes[name] = css_content
