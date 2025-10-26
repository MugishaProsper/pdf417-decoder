"""Configuration file support for PDF417 decoder."""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from .logger import get_logger

logger = get_logger(__name__)


class Config:
    """Configuration manager for PDF417 decoder."""
    
    DEFAULT_CONFIG = {
        'preprocessing': {
            'methods': 'all',  # or list of method indices
            'enabled': True
        },
        'output': {
            'format': 'txt',
            'verbose': False
        },
        'cache': {
            'enabled': True,
            'ttl': 86400,  # 24 hours
            'directory': '.cache'
        },
        'batch': {
            'recursive': False,
            'show_progress': True
        },
        'logging': {
            'level': 'INFO',
            'file': None
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path:
            self.load(config_path)
        else:
            # Try to load from default locations
            self._load_default()
    
    def _load_default(self) -> None:
        """Try to load configuration from default locations."""
        default_paths = [
            '.pdf417rc',
            '.pdf417rc.json',
            '.pdf417rc.yaml',
            '.pdf417rc.yml',
            'config.yaml',
            'config.yml',
            'config.json'
        ]
        
        for path in default_paths:
            if Path(path).exists():
                logger.debug(f"Found config file: {path}")
                self.load(path)
                return
        
        logger.debug("No config file found, using defaults")
    
    def load(self, config_path: str) -> None:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
        """
        path = Path(config_path)
        
        if not path.exists():
            logger.warning(f"Config file not found: {config_path}")
            return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    loaded_config = yaml.safe_load(f)
                elif path.suffix == '.json':
                    loaded_config = json.load(f)
                else:
                    # Try YAML first, then JSON
                    content = f.read()
                    try:
                        loaded_config = yaml.safe_load(content)
                    except yaml.YAMLError:
                        loaded_config = json.loads(content)
            
            # Merge with defaults
            self._merge_config(loaded_config)
            logger.info(f"Loaded configuration from {config_path}")
            
        except Exception as e:
            logger.error(f"Error loading config file {config_path}: {e}")
    
    def _merge_config(self, loaded_config: Dict[str, Any]) -> None:
        """
        Merge loaded configuration with defaults.
        
        Args:
            loaded_config: Configuration loaded from file
        """
        for section, values in loaded_config.items():
            if section in self.config and isinstance(values, dict):
                self.config[section].update(values)
            else:
                self.config[section] = values
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'cache.enabled')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, config_path: str) -> None:
        """
        Save configuration to file.
        
        Args:
            config_path: Path to save configuration
        """
        path = Path(config_path)
        
        try:
            with open(path, 'w', encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    yaml.dump(self.config, f, default_flow_style=False, indent=2)
                else:
                    json.dump(self.config, f, indent=2)
            
            logger.info(f"Saved configuration to {config_path}")
            
        except Exception as e:
            logger.error(f"Error saving config file {config_path}: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Load configuration from file or defaults.
    
    Args:
        config_path: Path to configuration file (optional)
        
    Returns:
        Config instance
    """
    return Config(config_path)
