# Welcome to MDRender! 🎉

This is a demonstration file showing the capabilities of the MDRender application.

## Table of Contents

- [Features Demo](#features-demo)
- [Text Formatting](#text-formatting)
- [Lists and Tasks](#lists-and-tasks)
- [Code Examples](#code-examples)
- [Tables](#tables)
- [Links and Images](#links-and-images)

---

## Features Demo

This application supports **GitHub Flavored Markdown** with many enhancements.

### Text Formatting

You can make text **bold** or *italic* or ***both***.

You can also use ~~strikethrough~~ text.

Inline `code` is supported with syntax highlighting.

> Blockquotes are styled beautifully
> 
> And can span multiple lines

### Headings

# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

---

## Lists and Tasks

### Unordered Lists

- Item 1
- Item 2
  - Nested item 2.1
  - Nested item 2.2
- Item 3

### Ordered Lists

1. First item
2. Second item
   1. Nested item 2.1
   2. Nested item 2.2
3. Third item

### Task Lists

- [x] Completed task
- [x] Another completed task
- [ ] Pending task
- [ ] Another pending task

---

## Code Examples

### Inline Code

Use `print()` to output text in Python.

### Code Blocks

Here's a Python example:

```python
def greet(name):
    """Greet someone by name"""
    return f"Hello, {name}!"

# Usage
message = greet("World")
print(message)
```

JavaScript example:

```javascript
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(factorial(5)); // Output: 120
```

SQL example:

```sql
SELECT 
    users.name,
    COUNT(orders.id) as order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id
HAVING order_count > 5;
```

---

## Tables

| Feature | Status | Priority |
|---------|--------|----------|
| Syntax Highlighting | ✅ Complete | High |
| Live Preview | ✅ Complete | High |
| Export to PDF | ✅ Complete | Medium |
| Git Integration | 🚧 Planned | Low |

### Aligned Tables

| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Left         | Center         | Right         |
| Content      | Content        | Content       |

---

## Links and Images

### Links

Visit [GitHub](https://github.com) for amazing open-source projects.

You can also use [reference-style links][1].

[1]: https://www.python.org "Python Homepage"

### Images

![Placeholder](https://via.placeholder.com/400x200?text=Markdown+Renderer)

---

## Advanced Features

### Keyboard Keys

Press <kbd>Ctrl</kbd>+<kbd>S</kbd> to save your document.

Use <kbd>Ctrl</kbd>+<kbd>B</kbd> for **bold** text.

### Highlighted Text

This is ==highlighted text== using marks.

### Horizontal Rules

You can create horizontal rules:

---

***

___

---

## Math Equations

Inline math: $E = mc^2$

Block math:

$$
\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

---

## Emojis

Use emojis to make your documents more expressive! 😊

- 🎉 Party
- 🚀 Rocket
- 💡 Idea
- ✅ Check
- ❌ Cross
- 📝 Note
- 🔥 Fire

---

## Tips for Using This Application

1. **Keyboard Shortcuts**: Use `Ctrl+B`, `Ctrl+I`, `Ctrl+K` for quick formatting
2. **Auto-Save**: Your work is automatically saved every 60 seconds
3. **Themes**: Try different themes from the View menu
4. **Export**: Export to HTML or PDF from the File menu
5. **Live Preview**: Watch your markdown render in real-time!

---

## Statistics

This document demonstrates:
- Multiple heading levels
- Text formatting options
- Code syntax highlighting
- Tables with alignment
- Lists and task lists
- Links and references
- Emojis and special characters

---

**Created with MDRender v1.0.0**

*Happy writing! 📝✨*
