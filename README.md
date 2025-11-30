# Markdown Renderer

A modern, feature-rich Python desktop application for editing and rendering Markdown files with live preview, syntax highlighting, and export capabilities.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### Core Functionality
- **Dual-Pane Interface**: Side-by-side Markdown editor and live HTML preview
- **Syntax Highlighting**: Color-coded Markdown syntax in the editor
- **Live Preview**: Real-time rendering with 300ms debounce for smooth performance
- **Line Numbers**: Easy navigation with line number display

### Markdown Support
- **GitHub Flavored Markdown (GFM)**: Full support for tables, task lists, strikethrough
- **Code Blocks**: Syntax highlighting for code blocks using Pygments
- **Tables**: Beautiful table rendering
- **Task Lists**: Interactive checkboxes
- **Emoji Support**: Use emoji in your markdown
- **Math Equations**: LaTeX/KaTeX support for mathematical expressions
- **Mermaid Diagrams**: Create flowcharts and diagrams

### Editor Features
- **Smart Formatting**: Keyboard shortcuts for bold, italic, code, links, headings
- **Undo/Redo**: Full history tracking
- **Find & Replace**: Quick text search
- **Auto-Save**: Configurable auto-save with 60-second default interval
- **Word/Character Count**: Real-time statistics in status bar

### Themes
- **GitHub Theme**: Clean light theme (default)
- **Dark Theme**: Easy on the eyes for night coding
- **Solarized Light**: Professional light theme
- **Solarized Dark**: Elegant dark theme
- **Custom Themes**: Load your own CSS themes

### Export Options
- **HTML Export**: Standalone HTML with embedded CSS ✅
- **PDF Export**: Professional PDF documents (requires additional setup on Windows)*

*Note: PDF export requires GTK libraries on Windows. If you don't need PDF export, the application works perfectly without it. You can always export as HTML and use your browser's "Print to PDF" feature as an alternative.

### File Management
- **Recent Files**: Quick access to recently opened files
- **Auto-Save**: Never lose your work
- **Drag & Drop**: Open files by dragging into the window (planned)

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

1. Clone or download this repository

2. Navigate to the project directory:
```powershell
cd markdown_renderer
```

3. Install required packages:
```powershell
pip install -r requirements.txt
```

### Dependencies

The application requires the following packages:

- **PyQt6**: Modern GUI framework ✅
- **PyQt6-WebEngine**: HTML rendering engine ✅
- **markdown**: Core markdown to HTML conversion ✅
- **pymdown-extensions**: GitHub Flavored Markdown extensions ✅
- **Pygments**: Syntax highlighting for code blocks ✅
- **pyyaml**: Configuration management ✅
- **weasyprint**: PDF export (optional - requires GTK on Windows) ⚠️

**Note on PDF Export:** WeasyPrint requires GTK libraries which are complex to install on Windows. The application works fully without it - you can export as HTML and use your browser to "Print to PDF" as a workaround. If you want PDF export, see the troubleshooting section.

## 🚀 Usage

### Starting the Application

Run the application with:

```powershell
python main.py
```

### Basic Operations

#### Creating a New File
- **Menu**: File → New
- **Shortcut**: `Ctrl+N`
- **Toolbar**: Click the "New" button

#### Opening a File
- **Menu**: File → Open
- **Shortcut**: `Ctrl+O`
- **Toolbar**: Click the "Open" button
- **Recent Files**: File → Open Recent

#### Saving Files
- **Save**: `Ctrl+S` or File → Save
- **Save As**: `Ctrl+Shift+S` or File → Save As
- **Auto-Save**: Enabled by default (60 seconds)

### Formatting

#### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Bold | `Ctrl+B` |
| Italic | `Ctrl+I` |
| Inline Code | `Ctrl+K` |
| Link | `Ctrl+L` |
| Heading 1 | `Ctrl+1` |
| Heading 2 | `Ctrl+2` |
| Heading 3 | `Ctrl+3` |
| Find | `Ctrl+F` |
| Save | `Ctrl+S` |
| Open | `Ctrl+O` |
| New | `Ctrl+N` |

#### Using the Toolbar

Click the formatting buttons in the toolbar to:
- Make text **bold** or *italic*
- Insert `inline code`
- Create links
- Add headings (H1, H2, H3)

### Exporting

#### Export as HTML
- **Menu**: File → Export → Export as HTML
- **Shortcut**: `Ctrl+E`
- Creates a standalone HTML file with embedded CSS

#### Export as PDF
- **Menu**: File → Export → Export as PDF
- **Shortcut**: `Ctrl+Shift+E`
- Generates a professional PDF document

**Note:** PDF export requires GTK libraries on Windows. If unavailable, the application will offer to export as HTML instead, which you can then convert to PDF using your browser's "Print to PDF" feature.

### Changing Themes

1. Go to **View → Theme**
2. Select from available themes:
   - GitHub (default)
   - Dark
   - Solarized Light
   - Solarized Dark

### Preview Controls

- **Toggle Preview**: `Ctrl+P` to show/hide preview pane
- **Zoom In**: `Ctrl++`
- **Zoom Out**: `Ctrl+-`
- **Reset Zoom**: `Ctrl+0`

## 📁 Project Structure

```
markdown_renderer/
├── main.py                    # Application entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── core/                      # Core functionality
│   ├── markdown_processor.py # Markdown to HTML conversion
│   ├── file_handler.py        # File I/O operations
│   ├── themes.py              # Theme management
│   └── exporter.py            # Export functionality
│
├── gui/                       # GUI components
│   ├── main_window.py         # Main application window
│   ├── editor.py              # Text editor with syntax highlighting
│   ├── preview.py             # HTML preview pane
│   └── toolbar.py             # Toolbar with actions
│
├── utils/                     # Utility modules
│   ├── config_manager.py      # Settings persistence
│   ├── shortcuts.py           # Keyboard shortcut manager
│   └── helpers.py             # Helper functions
│
└── resources/                 # Resources
    ├── themes/                # Custom CSS themes
    └── templates/             # Markdown templates
        ├── readme_template.md
        ├── documentation_template.md
        └── blog_post_template.md
```

## ⚙️ Configuration

Settings are stored in `~/.markdown_renderer/settings.yaml`

### Default Configuration

```yaml
editor:
  font_family: Consolas  # or Monaco on macOS
  font_size: 11
  tab_size: 4
  line_wrap: true

preview:
  theme: github
  sync_scroll: true
  zoom: 100

general:
  auto_save: true
  auto_save_interval: 60  # seconds
  recent_files_max: 10
```

## 🎨 Customization

### Adding Custom Themes

1. Create a CSS file in `resources/themes/`
2. Load it using the theme manager:

```python
from core.themes import ThemeManager

theme_manager = ThemeManager()
with open('my_theme.css', 'r') as f:
    css = f.read()
theme_manager.load_custom_theme('my_theme', css)
```

### Creating Templates

Add Markdown templates to `resources/templates/` and load them in your documents.

## 🔧 Development

### Running Tests

```powershell
pytest tests/
```

### Code Style

Follow PEP 8 guidelines. Use:

```powershell
# Format code
black .

# Check style
flake8 .
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -am 'Add feature'`
6. Push: `git push origin feature-name`
7. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Known Issues

- ~~Import errors for PyQt6 and weasyprint will appear until packages are installed~~
- PDF export requires GTK libraries on Windows (optional feature)
- Mermaid diagrams require internet connection for CDN

### Alternative to PDF Export

If you don't want to install GTK libraries:
1. Export as HTML (`Ctrl+E`)
2. Open the HTML file in your browser
3. Use browser's "Print to PDF" feature (`Ctrl+P` → Save as PDF)

This provides excellent PDF output without additional dependencies!

## 🚀 Future Enhancements

- [ ] Drag and drop file support
- [ ] Multi-tab document editing
- [ ] Find and replace dialog
- [ ] Presentation mode (slides from markdown)
- [ ] Git integration
- [ ] Plugin system
- [ ] Spell checker
- [ ] Table editor GUI
- [ ] Image paste from clipboard
- [ ] Word count goals and statistics

## 📧 Contact

For questions, issues, or suggestions:
- Create an issue on GitHub
- Email: your.email@example.com

## 🙏 Acknowledgments

- **PyQt6**: Excellent Qt bindings for Python
- **Python-Markdown**: Robust markdown parser
- **Pygments**: Beautiful syntax highlighting
- **WeasyPrint**: High-quality PDF generation

---

**Made with ❤️ using Python and PyQt6**
