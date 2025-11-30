"""
Keyboard shortcuts handler
"""
from typing import Dict, Callable, Optional
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QWidget
import config

class ShortcutManager:
    """Manage keyboard shortcuts for the application"""
    
    def __init__(self, parent_widget: QWidget):
        """
        Initialize shortcut manager
        
        Args:
            parent_widget: Parent widget to attach shortcuts to
        """
        self.parent = parent_widget
        self.shortcuts: Dict[str, QShortcut] = {}
        self.callbacks: Dict[str, Callable] = {}
    
    def register_shortcut(self, name: str, key_sequence: str, callback: Callable):
        """
        Register a keyboard shortcut
        
        Args:
            name: Shortcut name/identifier
            key_sequence: Key sequence (e.g., 'Ctrl+S')
            callback: Function to call when shortcut is triggered
        """
        # Create shortcut
        shortcut = QShortcut(QKeySequence(key_sequence), self.parent)
        shortcut.activated.connect(callback)
        
        # Store
        self.shortcuts[name] = shortcut
        self.callbacks[name] = callback
    
    def unregister_shortcut(self, name: str):
        """
        Unregister a keyboard shortcut
        
        Args:
            name: Shortcut name to remove
        """
        if name in self.shortcuts:
            self.shortcuts[name].setEnabled(False)
            del self.shortcuts[name]
            del self.callbacks[name]
    
    def update_shortcut(self, name: str, new_key_sequence: str):
        """
        Update a shortcut's key sequence
        
        Args:
            name: Shortcut name
            new_key_sequence: New key sequence
        """
        if name in self.shortcuts:
            callback = self.callbacks[name]
            self.unregister_shortcut(name)
            self.register_shortcut(name, new_key_sequence, callback)
    
    def enable_shortcut(self, name: str, enabled: bool = True):
        """
        Enable or disable a shortcut
        
        Args:
            name: Shortcut name
            enabled: Whether to enable or disable
        """
        if name in self.shortcuts:
            self.shortcuts[name].setEnabled(enabled)
    
    def get_shortcut_key(self, name: str) -> Optional[str]:
        """
        Get the key sequence for a shortcut
        
        Args:
            name: Shortcut name
            
        Returns:
            Key sequence string or None
        """
        if name in self.shortcuts:
            return self.shortcuts[name].key().toString()
        return None
    
    def load_default_shortcuts(self):
        """Load default shortcuts from config"""
        return config.SHORTCUTS.copy()
