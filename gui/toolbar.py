"""
Toolbar component with formatting buttons and actions
"""
from PyQt6.QtWidgets import QToolBar, QWidget, QLabel
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt, pyqtSignal

class MarkdownToolbar(QToolBar):
    """Toolbar with markdown formatting actions"""
    
    # Signals for actions
    newFileClicked = pyqtSignal()
    openFileClicked = pyqtSignal()
    saveFileClicked = pyqtSignal()
    saveAsClicked = pyqtSignal()
    exportHtmlClicked = pyqtSignal()
    exportPdfClicked = pyqtSignal()
    
    boldClicked = pyqtSignal()
    italicClicked = pyqtSignal()
    codeClicked = pyqtSignal()
    linkClicked = pyqtSignal()
    heading1Clicked = pyqtSignal()
    heading2Clicked = pyqtSignal()
    heading3Clicked = pyqtSignal()
    
    findClicked = pyqtSignal()
    togglePreviewClicked = pyqtSignal()
    
    themeChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setMovable(False)
        self.setFloatable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        self._create_actions()
    
    def _create_actions(self):
        """Create toolbar actions"""
        
        # File actions
        self.new_action = QAction("New", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.setStatusTip("Create a new file")
        self.new_action.triggered.connect(self.newFileClicked.emit)
        self.addAction(self.new_action)
        
        self.open_action = QAction("Open", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.setStatusTip("Open a file")
        self.open_action.triggered.connect(self.openFileClicked.emit)
        self.addAction(self.open_action)
        
        self.save_action = QAction("Save", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.setStatusTip("Save the current file")
        self.save_action.triggered.connect(self.saveFileClicked.emit)
        self.addAction(self.save_action)
        
        self.addSeparator()
        
        # Formatting actions
        self.bold_action = QAction("Bold", self)
        self.bold_action.setShortcut("Ctrl+B")
        self.bold_action.setStatusTip("Make text bold")
        self.bold_action.triggered.connect(self.boldClicked.emit)
        self.addAction(self.bold_action)
        
        self.italic_action = QAction("Italic", self)
        self.italic_action.setShortcut("Ctrl+I")
        self.italic_action.setStatusTip("Make text italic")
        self.italic_action.triggered.connect(self.italicClicked.emit)
        self.addAction(self.italic_action)
        
        self.code_action = QAction("Code", self)
        self.code_action.setShortcut("Ctrl+K")
        self.code_action.setStatusTip("Insert inline code")
        self.code_action.triggered.connect(self.codeClicked.emit)
        self.addAction(self.code_action)
        
        self.link_action = QAction("Link", self)
        self.link_action.setShortcut("Ctrl+L")
        self.link_action.setStatusTip("Insert link")
        self.link_action.triggered.connect(self.linkClicked.emit)
        self.addAction(self.link_action)
        
        self.addSeparator()
        
        # Heading actions
        self.h1_action = QAction("H1", self)
        self.h1_action.setShortcut("Ctrl+1")
        self.h1_action.setStatusTip("Insert heading 1")
        self.h1_action.triggered.connect(self.heading1Clicked.emit)
        self.addAction(self.h1_action)
        
        self.h2_action = QAction("H2", self)
        self.h2_action.setShortcut("Ctrl+2")
        self.h2_action.setStatusTip("Insert heading 2")
        self.h2_action.triggered.connect(self.heading2Clicked.emit)
        self.addAction(self.h2_action)
        
        self.h3_action = QAction("H3", self)
        self.h3_action.setShortcut("Ctrl+3")
        self.h3_action.setStatusTip("Insert heading 3")
        self.h3_action.triggered.connect(self.heading3Clicked.emit)
        self.addAction(self.h3_action)
        
        self.addSeparator()
        
        # View actions
        self.find_action = QAction("Find", self)
        self.find_action.setShortcut(QKeySequence.StandardKey.Find)
        self.find_action.setStatusTip("Find text")
        self.find_action.triggered.connect(self.findClicked.emit)
        self.addAction(self.find_action)
        
        self.toggle_preview_action = QAction("Toggle Preview", self)
        self.toggle_preview_action.setShortcut("Ctrl+P")
        self.toggle_preview_action.setStatusTip("Toggle preview pane")
        self.toggle_preview_action.triggered.connect(self.togglePreviewClicked.emit)
        self.addAction(self.toggle_preview_action)
    
    def set_file_modified(self, modified: bool):
        """
        Update UI to show file modified status
        
        Args:
            modified: Whether file has unsaved changes
        """
        if modified:
            self.save_action.setEnabled(True)
        else:
            self.save_action.setEnabled(True)  # Keep enabled for Ctrl+S convenience
