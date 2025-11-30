"""
Configuration manager for persistent settings
"""
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
import config

class ConfigManager:
    """Manage application configuration and settings"""
    
    def __init__(self):
        """Initialize configuration manager"""
        self.config_file = config.SETTINGS_FILE
        self.settings: Dict[str, Any] = {}
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.settings = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Could not load settings: {e}")
                self.settings = {}
        else:
            self.settings = self._get_default_settings()
            self.save_settings()
    
    def save_settings(self):
        """Save settings to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.settings, f, default_flow_style=False)
        except Exception as e:
            print(f"Warning: Could not save settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value
        
        Args:
            key: Setting key (can use dot notation for nested keys)
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set a setting value
        
        Args:
            key: Setting key (can use dot notation for nested keys)
            value: Value to set
        """
        keys = key.split('.')
        current = self.settings
        
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        self.save_settings()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings"""
        return {
            'editor': {
                'font_family': config.DEFAULT_FONT_FAMILY,
                'font_size': config.DEFAULT_FONT_SIZE,
                'tab_size': config.DEFAULT_TAB_SIZE,
                'line_wrap': True,
                'show_line_numbers': True,
            },
            'preview': {
                'theme': config.DEFAULT_THEME,
                'sync_scroll': config.SYNC_SCROLL_ENABLED,
                'zoom': config.DEFAULT_ZOOM,
            },
            'window': {
                'width': config.DEFAULT_WINDOW_WIDTH,
                'height': config.DEFAULT_WINDOW_HEIGHT,
                'splitter_ratio': config.DEFAULT_SPLITTER_RATIO,
            },
            'general': {
                'auto_save': True,
                'auto_save_interval': config.AUTO_SAVE_INTERVAL,
                'recent_files_max': config.MAX_RECENT_FILES,
            }
        }
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self._get_default_settings()
        self.save_settings()
