import os
import json
import questionary
from pathlib import Path

CONFIG_DIR = os.path.expanduser("~/.config/ai_shell")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "active_model": "gemini",
    "api_keys": {
        "google": ""
    },
    "models": {
        "gemini": {
            "name": "gemini-1.5-flash",
            "provider": "google"
        }
    }
}

def ensure_config_dir():
    """Ensure the configuration directory exists."""
    os.makedirs(CONFIG_DIR, exist_ok=True)

def load_config():
    """Load the configuration from file."""
    ensure_config_dir()
    if not os.path.exists(CONFIG_FILE):
        return None
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def save_config(config):
    """Save the configuration to file."""
    ensure_config_dir()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def setup_wizard():
    """Run the setup wizard to configure the assistant."""
    config = load_config() or DEFAULT_CONFIG.copy()
    
    print("\nWelcome to AI Shell Setup!")
    
    # Configure API key
    print("\nAPI Key Configuration:")
    
    google_key = questionary.password(
        "Enter your Google AI API key (Gemini):").ask()
    if google_key:
        config["api_keys"]["google"] = google_key

    save_config(config)
    return config

def get_active_model():
    """Get the currently active model name."""
    return "gemini" 