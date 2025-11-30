# Quick Start Guide

## Installation

1. **Install Python 3.8+** if not already installed

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```powershell
   python main.py
   ```

## First Steps

### 1. Create Your First Document

- Click **New** button or press `Ctrl+N`
- Start typing in the left pane
- Watch the live preview on the right!

### 2. Try Basic Formatting

Type these examples:

```markdown
# This is a heading

**This is bold**
*This is italic*
`This is code`

- List item 1
- List item 2
```

### 3. Save Your Work

- Press `Ctrl+S` to save
- Choose a filename ending in `.md`
- Auto-save will keep your work safe

### 4. Change the Theme

- Go to **View → Theme**
- Try "Dark" for night coding
- Select "GitHub" for the classic look

### 5. Export Your Document

#### As HTML:
- Press `Ctrl+E`
- Choose save location
- Open in any web browser

#### As PDF:
- Press `Ctrl+Shift+E`
- Choose save location
- Get a professional document

## Keyboard Shortcuts Reference

| Action | Shortcut |
|--------|----------|
| **File Operations** |
| New File | `Ctrl+N` |
| Open File | `Ctrl+O` |
| Save | `Ctrl+S` |
| Save As | `Ctrl+Shift+S` |
| **Formatting** |
| Bold | `Ctrl+B` |
| Italic | `Ctrl+I` |
| Code | `Ctrl+K` |
| Link | `Ctrl+L` |
| **Headings** |
| Heading 1 | `Ctrl+1` |
| Heading 2 | `Ctrl+2` |
| Heading 3 | `Ctrl+3` |
| **View** |
| Toggle Preview | `Ctrl+P` |
| Zoom In | `Ctrl++` |
| Zoom Out | `Ctrl+-` |
| Reset Zoom | `Ctrl+0` |
| **Export** |
| Export HTML | `Ctrl+E` |
| Export PDF | `Ctrl+Shift+E` |

## Tips & Tricks

### Tip 1: Use Templates
- Check `resources/templates/` for starter templates
- Great for README files, documentation, blog posts

### Tip 2: Organize with Headings
- Use `#` for main sections
- Use `##` for subsections
- The preview shows clear hierarchy

### Tip 3: Code Blocks with Language
```markdown
```python
def hello():
    print("Hello World")
```
```

### Tip 4: Recent Files
- Access recent files from File menu
- Quick way to continue work

### Tip 5: Statistics
- Check the status bar for word/character count
- Track your progress in real-time

## Troubleshooting

### Problem: Application won't start
**Solution:** Make sure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

### Problem: Import errors
**Solution:** Check Python version (3.8+ required):
```powershell
python --version
```

### Problem: PDF export fails
**Solution:** WeasyPrint may need system dependencies. See [WeasyPrint docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)

### Problem: Preview is blank
**Solution:** Try refreshing by editing the text or changing themes

## Learn More

### Markdown Syntax
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)

### Application Features
- See `README.md` for complete feature list
- Check `DEMO.md` for examples

## Support

Need help? 
- Create an issue on GitHub
- Check the documentation
- Review example files

---

**Now you're ready to start creating beautiful markdown documents!** 🎉
