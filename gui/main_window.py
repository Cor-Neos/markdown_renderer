"""
Main application window
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QSplitter, QFileDialog, QMessageBox, QStatusBar,
                            QLabel, QMenuBar, QMenu)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence

from gui.editor import MarkdownEditor
from gui.preview import MarkdownPreview
from gui.toolbar import MarkdownToolbar
from core.markdown_processor import MarkdownProcessor
from core.file_handler import FileHandler
from core.themes import ThemeManager
from core.exporter import Exporter
import config

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.file_handler = FileHandler()
        self.markdown_processor = MarkdownProcessor()
        self.theme_manager = ThemeManager()
        self.exporter = Exporter(self.markdown_processor)
        
        # Setup UI
        self.setWindowTitle(config.APP_NAME)
        self.resize(config.DEFAULT_WINDOW_WIDTH, config.DEFAULT_WINDOW_HEIGHT)
        
        # Create UI components (order matters - central widget must be created first)
        self._create_central_widget()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        
        # Setup auto-save timer
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self._auto_save)
        self.auto_save_timer.start(config.AUTO_SAVE_INTERVAL * 1000)
        
        # Preview update timer (debounce)
        self.preview_timer = QTimer(self)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self._update_preview)
        
        # Connect signals
        self._connect_signals()
        
        # Initial state
        self._update_title()
        self._update_preview()
    
    def _create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)
        
        # Recent files submenu
        self.recent_menu = QMenu("Open &Recent", self)
        self._update_recent_files_menu()
        file_menu.addMenu(self.recent_menu)
        
        file_menu.addSeparator()
        
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self._save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Export submenu
        export_menu = QMenu("&Export", self)
        
        export_html_action = QAction("Export as &HTML...", self)
        export_html_action.setShortcut("Ctrl+E")
        export_html_action.triggered.connect(self._export_html)
        export_menu.addAction(export_html_action)
        
        export_pdf_action = QAction("Export as &PDF...", self)
        export_pdf_action.setShortcut("Ctrl+Shift+E")
        export_pdf_action.triggered.connect(self._export_pdf)
        export_menu.addAction(export_pdf_action)
        
        file_menu.addMenu(export_menu)
        
        file_menu.addSeparator()
        
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        select_all_action = QAction("Select &All", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_all_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        toggle_preview_action = QAction("Toggle &Preview", self)
        toggle_preview_action.setShortcut("Ctrl+P")
        toggle_preview_action.triggered.connect(self._toggle_preview)
        view_menu.addAction(toggle_preview_action)
        
        view_menu.addSeparator()
        
        zoom_in_action = QAction("Zoom &In", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(self.preview.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom &Out", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(self.preview.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        zoom_reset_action = QAction("&Reset Zoom", self)
        zoom_reset_action.setShortcut("Ctrl+0")
        zoom_reset_action.triggered.connect(self.preview.zoom_reset)
        view_menu.addAction(zoom_reset_action)
        
        view_menu.addSeparator()
        
        # Theme submenu
        theme_menu = QMenu("&Theme", self)
        for theme_name in self.theme_manager.get_available_themes():
            theme_action = QAction(theme_name.replace('-', ' ').title(), self)
            theme_action.triggered.connect(lambda checked, t=theme_name: self._change_theme(t))
            theme_menu.addAction(theme_action)
        view_menu.addMenu(theme_menu)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self):
        """Create the toolbar"""
        self.toolbar = MarkdownToolbar(self)
        self.addToolBar(self.toolbar)
        
        # Connect toolbar signals
        self.toolbar.newFileClicked.connect(self._new_file)
        self.toolbar.openFileClicked.connect(self._open_file)
        self.toolbar.saveFileClicked.connect(self._save_file)
        self.toolbar.boldClicked.connect(lambda: self.editor.insert_markdown_syntax('bold'))
        self.toolbar.italicClicked.connect(lambda: self.editor.insert_markdown_syntax('italic'))
        self.toolbar.codeClicked.connect(lambda: self.editor.insert_markdown_syntax('code'))
        self.toolbar.linkClicked.connect(lambda: self.editor.insert_markdown_syntax('link'))
        self.toolbar.heading1Clicked.connect(lambda: self.editor.insert_markdown_syntax('heading1'))
        self.toolbar.heading2Clicked.connect(lambda: self.editor.insert_markdown_syntax('heading2'))
        self.toolbar.heading3Clicked.connect(lambda: self.editor.insert_markdown_syntax('heading3'))
        self.toolbar.togglePreviewClicked.connect(self._toggle_preview)
    
    def _create_central_widget(self):
        """Create the central widget with editor and preview"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for editor and preview
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create editor
        self.editor = MarkdownEditor()
        self.splitter.addWidget(self.editor)
        
        # Create preview
        self.preview = MarkdownPreview()
        self.splitter.addWidget(self.preview)
        
        # Set initial splitter sizes (50-50)
        self.splitter.setSizes([
            int(config.DEFAULT_WINDOW_WIDTH * config.DEFAULT_SPLITTER_RATIO),
            int(config.DEFAULT_WINDOW_WIDTH * (1 - config.DEFAULT_SPLITTER_RATIO))
        ])
        
        layout.addWidget(self.splitter)
    
    def _create_status_bar(self):
        """Create the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status labels
        self.status_label = QLabel("Ready")
        self.stats_label = QLabel()
        
        self.status_bar.addWidget(self.status_label, 1)
        self.status_bar.addPermanentWidget(self.stats_label)
        
        self._update_stats()
    
    def _connect_signals(self):
        """Connect signals and slots"""
        self.editor.textChanged.connect(self._on_text_changed)
    
    def _on_text_changed(self):
        """Handle editor text changes"""
        self.file_handler.set_modified(True)
        self._update_title()
        self._update_stats()
        
        # Debounce preview update
        self.preview_timer.start(300)  # 300ms delay
    
    def _update_preview(self):
        """Update the preview pane"""
        markdown_text = self.editor.toPlainText()
        theme_css = self.theme_manager.get_theme_css()
        html = self.markdown_processor.convert(markdown_text, theme_css)
        
        # Get base URL for relative paths
        base_url = ""
        if self.file_handler.current_file:
            base_url = str(self.file_handler.current_file.parent)
        
        self.preview.set_html(html, base_url)
    
    def _update_title(self):
        """Update window title"""
        filename = self.file_handler.get_current_file_name()
        modified = "*" if self.file_handler.is_modified else ""
        self.setWindowTitle(f"{filename}{modified} - {config.APP_NAME}")
    
    def _update_stats(self):
        """Update statistics in status bar"""
        stats = self.editor.get_statistics()
        self.stats_label.setText(
            f"Lines: {stats['lines']} | "
            f"Words: {stats['words']} | "
            f"Characters: {stats['characters']}"
        )
    
    def _new_file(self):
        """Create a new file"""
        if self._check_save_changes():
            self.file_handler.new_file()
            self.editor.clear()
            self._update_title()
            self._update_preview()
            self.status_label.setText("New file created")
    
    def _open_file(self):
        """Open a file"""
        if not self._check_save_changes():
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            "",
            "Markdown Files (*.md *.markdown *.mdown);;All Files (*.*)"
        )
        
        if file_path:
            self._load_file(file_path)
    
    def _load_file(self, file_path: str):
        """Load a file from path"""
        success, content, error = self.file_handler.open_file(file_path)
        
        if success:
            self.editor.setPlainText(content)
            self._update_title()
            self._update_preview()
            self._update_recent_files_menu()
            self.status_label.setText(f"Opened: {self.file_handler.get_current_file_name()}")
        else:
            QMessageBox.critical(self, "Error Opening File", error)
    
    def _save_file(self):
        """Save the current file"""
        if self.file_handler.current_file:
            self._save_to_file(str(self.file_handler.current_file))
        else:
            self._save_file_as()
    
    def _save_file_as(self):
        """Save file as a new file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Markdown File",
            "",
            "Markdown Files (*.md);;All Files (*.*)"
        )
        
        if file_path:
            self._save_to_file(file_path)
    
    def _save_to_file(self, file_path: str):
        """Save content to file"""
        content = self.editor.toPlainText()
        success, error = self.file_handler.save_file(content, file_path)
        
        if success:
            self._update_title()
            self._update_recent_files_menu()
            self.status_label.setText(f"Saved: {self.file_handler.get_current_file_name()}")
        else:
            QMessageBox.critical(self, "Error Saving File", error)
    
    def _auto_save(self):
        """Auto-save the current file"""
        if self.file_handler.is_modified and self.file_handler.current_file:
            content = self.editor.toPlainText()
            success, _ = self.file_handler.save_file(content)
            if success:
                self._update_title()
                self.status_label.setText("Auto-saved", 2000)
    
    def _export_html(self):
        """Export as HTML"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export as HTML",
            "",
            "HTML Files (*.html);;All Files (*.*)"
        )
        
        if file_path:
            markdown_content = self.editor.toPlainText()
            theme_css = self.theme_manager.get_theme_css()
            success, error = self.exporter.export_html(markdown_content, file_path, theme_css)
            
            if success:
                QMessageBox.information(self, "Export Successful", 
                                      f"File exported to:\n{file_path}")
            else:
                QMessageBox.critical(self, "Export Failed", error)
    
    def _export_pdf(self):
        """Export as PDF"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export as PDF",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if file_path:
            markdown_content = self.editor.toPlainText()
            theme_css = self.theme_manager.get_theme_css()
            success, error = self.exporter.export_pdf(markdown_content, file_path, theme_css)
            
            if success:
                QMessageBox.information(self, "Export Successful", 
                                      f"File exported to:\n{file_path}")
            else:
                # Show error with option to export as HTML instead
                reply = QMessageBox.critical(
                    self, 
                    "PDF Export Failed", 
                    f"{error}\n\nWould you like to export as HTML instead?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    self._export_html()
    
    def _toggle_preview(self):
        """Toggle preview pane visibility"""
        if self.preview.isVisible():
            self.preview.hide()
        else:
            self.preview.show()
    
    def _change_theme(self, theme_name: str):
        """Change preview theme"""
        self.theme_manager.set_theme(theme_name)
        self._update_preview()
        self.status_label.setText(f"Theme changed to: {theme_name}")
    
    def _update_recent_files_menu(self):
        """Update recent files menu"""
        self.recent_menu.clear()
        
        recent_files = self.file_handler.get_recent_files()
        
        if recent_files:
            for file_path in recent_files:
                action = QAction(file_path, self)
                action.triggered.connect(lambda checked, p=file_path: self._load_file(p))
                self.recent_menu.addAction(action)
            
            self.recent_menu.addSeparator()
            
            clear_action = QAction("Clear Recent Files", self)
            clear_action.triggered.connect(self._clear_recent_files)
            self.recent_menu.addAction(clear_action)
        else:
            no_recent_action = QAction("No recent files", self)
            no_recent_action.setEnabled(False)
            self.recent_menu.addAction(no_recent_action)
    
    def _clear_recent_files(self):
        """Clear recent files list"""
        self.file_handler.clear_recent_files()
        self._update_recent_files_menu()
    
    def _check_save_changes(self) -> bool:
        """
        Check if there are unsaved changes and prompt user
        
        Returns:
            True if it's safe to continue, False if user cancelled
        """
        if not self.file_handler.is_modified:
            return True
        
        reply = QMessageBox.question(
            self,
            "Unsaved Changes",
            "Do you want to save your changes?",
            QMessageBox.StandardButton.Save | 
            QMessageBox.StandardButton.Discard | 
            QMessageBox.StandardButton.Cancel
        )
        
        if reply == QMessageBox.StandardButton.Save:
            self._save_file()
            return True
        elif reply == QMessageBox.StandardButton.Discard:
            return True
        else:
            return False
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            f"About {config.APP_NAME}",
            f"""<h2>{config.APP_NAME}</h2>
            <p>Version {config.APP_VERSION}</p>
            <p>A modern, lightweight Markdown editor with live preview.</p>
            <p>Features:</p>
            <ul>
                <li>Live preview with syntax highlighting</li>
                <li>Multiple themes</li>
                <li>Export to HTML and PDF</li>
                <li>GitHub Flavored Markdown support</li>
            </ul>
            """
        )
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self._check_save_changes():
            event.accept()
        else:
            event.ignore()
