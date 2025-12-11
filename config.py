"""
Configuration settings for Markdown Renderer
"""
import os
import sys
from pathlib import Path

# Application Info
APP_NAME = "MDRender"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# Directories - handle both development and PyInstaller frozen app
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = Path(sys._MEIPASS)
else:
    # Running as script
    BASE_DIR = Path(__file__).parent

RESOURCES_DIR = BASE_DIR / "resources"
THEMES_DIR = RESOURCES_DIR / "themes"
TEMPLATES_DIR = RESOURCES_DIR / "templates"
CONFIG_DIR = Path.home() / ".mdrender"

# Ensure config directory exists
CONFIG_DIR.mkdir(exist_ok=True)

# Configuration Files
SETTINGS_FILE = CONFIG_DIR / "settings.yaml"
RECENT_FILES_FILE = CONFIG_DIR / "recent_files.txt"

# Editor Settings
DEFAULT_FONT_FAMILY = "Consolas" if os.name == "nt" else "Monaco"
# Emoji fallback fonts for Windows
EMOJI_FALLBACK_FONTS = ["Segoe UI Emoji", "Segoe UI Symbol", "Apple Color Emoji"]
DEFAULT_FONT_SIZE = 11
DEFAULT_TAB_SIZE = 4
AUTO_SAVE_INTERVAL = 60  # seconds
MAX_RECENT_FILES = 10

# Preview Settings
DEFAULT_THEME = "github"
SYNC_SCROLL_ENABLED = True
DEFAULT_ZOOM = 100

# Window Settings
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800
DEFAULT_SPLITTER_RATIO = 0.5  # 50-50 split

# Markdown Extensions
MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.toc',
    'markdown.extensions.tables',
    'markdown.extensions.fenced_code',
    'markdown.extensions.nl2br',
    'pymdownx.superfences',
    'pymdownx.highlight',
    'pymdownx.inlinehilite',
    'pymdownx.tasklist',
    'pymdownx.emoji',
    'pymdownx.magiclink',
    'pymdownx.mark',
    'pymdownx.tilde',
    'pymdownx.keys',
]

MARKDOWN_EXTENSION_CONFIGS = {
    'pymdownx.highlight': {
        'use_pygments': True,
        'linenums': True,
    },
    'pymdownx.superfences': {
        'custom_fences': [
            {
                'name': 'mermaid',
                'class': 'mermaid',
                'format': lambda src: f'<div class="mermaid">{src}</div>'
            }
        ]
    },
    'pymdownx.tasklist': {
        'custom_checkbox': True,
    },
    'pymdownx.emoji': {
        'emoji_index': lambda: None,
        'emoji_generator': lambda: None,
    },
    'markdown.extensions.codehilite': {
        'css_class': 'highlight',
        'linenums': False,
    },
    'markdown.extensions.toc': {
        'permalink': True,
    }
}

# Export Settings
EXPORT_DEFAULT_FORMAT = "html"
PDF_PAGE_SIZE = "A4"
PDF_MARGIN = "2cm"

# Keyboard Shortcuts (default)
SHORTCUTS = {
    'new_file': 'Ctrl+N',
    'open_file': 'Ctrl+O',
    'save_file': 'Ctrl+S',
    'save_as': 'Ctrl+Shift+S',
    'export_html': 'Ctrl+E',
    'export_pdf': 'Ctrl+Shift+E',
    'quit': 'Ctrl+Q',
    'bold': 'Ctrl+B',
    'italic': 'Ctrl+I',
    'code': 'Ctrl+K',
    'link': 'Ctrl+L',
    'heading_1': 'Ctrl+1',
    'heading_2': 'Ctrl+2',
    'heading_3': 'Ctrl+3',
    'find': 'Ctrl+F',
    'replace': 'Ctrl+H',
    'toggle_preview': 'Ctrl+P',
    'focus_mode': 'F11',
    'zoom_in': 'Ctrl++',
    'zoom_out': 'Ctrl+-',
    'zoom_reset': 'Ctrl+0',
}

# Theme Names
AVAILABLE_THEMES = [
    'github',
    'dark',
    'solarized-light',
    'solarized-dark',
]
