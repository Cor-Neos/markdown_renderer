"""
Text editor component with markdown syntax highlighting
"""
from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt6.QtGui import (QColor, QPainter, QTextFormat, QFont, 
                         QSyntaxHighlighter, QTextCharFormat, QPalette)
import re
import os
import config

class LineNumberArea(QWidget):
    """Widget for displaying line numbers"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

class MarkdownHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Markdown"""
    
    def __init__(self, document):
        super().__init__(document)
        self._setup_formats()
    
    def _setup_formats(self):
        """Setup text formats for different markdown elements"""
        # Heading format
        self.heading_format = QTextCharFormat()
        self.heading_format.setForeground(QColor("#0366d6"))
        self.heading_format.setFontWeight(QFont.Weight.Bold)
        
        # Bold format
        self.bold_format = QTextCharFormat()
        self.bold_format.setFontWeight(QFont.Weight.Bold)
        
        # Italic format
        self.italic_format = QTextCharFormat()
        self.italic_format.setFontItalic(True)
        
        # Code format
        self.code_format = QTextCharFormat()
        self.code_format.setForeground(QColor("#24292e"))
        self.code_format.setBackground(QColor("#f6f8fa"))
        self.code_format.setFontFamily("Consolas")
        
        # Link format
        self.link_format = QTextCharFormat()
        self.link_format.setForeground(QColor("#0366d6"))
        self.link_format.setFontUnderline(True)
        
        # Quote format
        self.quote_format = QTextCharFormat()
        self.quote_format.setForeground(QColor("#6a737d"))
        
        # List format
        self.list_format = QTextCharFormat()
        self.list_format.setForeground(QColor("#0366d6"))
        
        # Comment format
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#6a737d"))
        self.comment_format.setFontItalic(True)
    
    def highlightBlock(self, text):
        """Apply syntax highlighting to a block of text"""
        
        # Headings
        heading_pattern = r'^#{1,6}\s+.+$'
        for match in re.finditer(heading_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.heading_format)
        
        # Bold: **text** or __text__
        bold_pattern = r'(\*\*|__)(.*?)\1'
        for match in re.finditer(bold_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.bold_format)
        
        # Italic: *text* or _text_
        italic_pattern = r'(\*|_)(.*?)\1'
        for match in re.finditer(italic_pattern, text):
            if match.group(0) not in ['**', '__']:  # Don't match bold markers
                self.setFormat(match.start(), match.end() - match.start(), self.italic_format)
        
        # Inline code: `code`
        code_pattern = r'`([^`]+)`'
        for match in re.finditer(code_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.code_format)
        
        # Links: [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        for match in re.finditer(link_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.link_format)
        
        # Blockquotes
        quote_pattern = r'^>\s+.+$'
        for match in re.finditer(quote_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.quote_format)
        
        # Lists: - or * or +
        list_pattern = r'^[\s]*[-*+]\s+'
        for match in re.finditer(list_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.list_format)
        
        # Numbered lists
        numbered_list_pattern = r'^[\s]*\d+\.\s+'
        for match in re.finditer(numbered_list_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.list_format)

class MarkdownEditor(QPlainTextEdit):
    """Enhanced text editor for markdown with line numbers and syntax highlighting"""
    
    textChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Setup editor
        self._setup_editor()
        
        # Line numbers
        self.line_number_area = LineNumberArea(self)
        
        # Syntax highlighter
        self.highlighter = MarkdownHighlighter(self.document())
        
        # Connect signals
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        
        self.update_line_number_area_width(0)
    
    def _setup_editor(self):
        """Configure editor settings"""
        # Font - use multiple font families for emoji support on Windows
        if os.name == 'nt':
            # Windows: Use Consolas with Segoe UI Emoji fallback
            font = QFont()
            font.setFamilies(["Consolas", "Segoe UI Emoji", "Segoe UI Symbol", "Arial"])
            font.setPointSize(config.DEFAULT_FONT_SIZE)
            # Set font strategy to prefer quality for better emoji rendering
            font.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
        else:
            # macOS/Linux
            font = QFont()
            font.setFamilies([config.DEFAULT_FONT_FAMILY, "Apple Color Emoji", "Noto Color Emoji"])
            font.setPointSize(config.DEFAULT_FONT_SIZE)
            font.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
        
        self.setFont(font)
        
        # Enable better text rendering for Unicode/emoji
        self.document().setDefaultFont(font)
        
        # Tab settings
        tab_width = config.DEFAULT_TAB_SIZE * self.fontMetrics().horizontalAdvance(' ')
        self.setTabStopDistance(tab_width)
        
        # Line wrap
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        
        # Placeholder
        self.setPlaceholderText("Start typing your markdown here...")
    
    def line_number_area_width(self):
        """Calculate the width needed for line numbers"""
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self, _):
        """Update the width of line number area"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        """Update line number area on scroll"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), 
                                        self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(),
                                               self.line_number_area_width(), cr.height()))
    
    def line_number_area_paint_event(self, event):
        """Paint line numbers"""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#f6f8fa"))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#6a737d"))
                painter.drawText(0, int(top), self.line_number_area.width() - 3,
                               self.fontMetrics().height(), Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
    
    def insert_markdown_syntax(self, syntax_type: str):
        """
        Insert markdown syntax at cursor position
        
        Args:
            syntax_type: Type of markdown syntax to insert
        """
        cursor = self.textCursor()
        
        if syntax_type == 'bold':
            if cursor.hasSelection():
                text = cursor.selectedText()
                cursor.insertText(f"**{text}**")
            else:
                cursor.insertText("****")
                cursor.movePosition(cursor.MoveOperation.Left, cursor.MoveMode.MoveAnchor, 2)
                self.setTextCursor(cursor)
        
        elif syntax_type == 'italic':
            if cursor.hasSelection():
                text = cursor.selectedText()
                cursor.insertText(f"*{text}*")
            else:
                cursor.insertText("**")
                cursor.movePosition(cursor.MoveOperation.Left, cursor.MoveMode.MoveAnchor, 1)
                self.setTextCursor(cursor)
        
        elif syntax_type == 'code':
            if cursor.hasSelection():
                text = cursor.selectedText()
                cursor.insertText(f"`{text}`")
            else:
                cursor.insertText("``")
                cursor.movePosition(cursor.MoveOperation.Left, cursor.MoveMode.MoveAnchor, 1)
                self.setTextCursor(cursor)
        
        elif syntax_type == 'link':
            if cursor.hasSelection():
                text = cursor.selectedText()
                cursor.insertText(f"[{text}](url)")
            else:
                cursor.insertText("[text](url)")
        
        elif syntax_type.startswith('heading'):
            level = int(syntax_type[-1])
            cursor.movePosition(cursor.MoveOperation.StartOfLine)
            cursor.insertText('#' * level + ' ')
    
    def get_statistics(self) -> dict:
        """Get editor statistics"""
        text = self.toPlainText()
        return {
            'lines': self.blockCount(),
            'words': len(text.split()),
            'characters': len(text),
            'characters_no_spaces': len(text.replace(' ', '').replace('\n', '')),
        }
