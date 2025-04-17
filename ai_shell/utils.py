import os
import sys
import platform
import shutil
from typing import Tuple

def enable_ansi_support():
    """Enable ANSI escape sequences for Windows."""
    if platform.system() == "Windows":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def format_text(color: str, bold: bool = False) -> str:
    """Format text with ANSI color codes."""
    colors = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37'
    }
    
    if color not in colors:
        return ''
    
    bold_code = '1;' if bold else ''
    return f'\033[{bold_code}{colors[color]}m'

def reset_format() -> str:
    """Reset text formatting."""
    return '\033[0m'

def get_terminal_size() -> Tuple[int, int]:
    """Get the terminal size."""
    return shutil.get_terminal_size()

def get_system_info() -> dict:
    """Get system information."""
    return {
        'os': platform.system(),
        'os_release': platform.release(),
        'python_version': platform.python_version(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'hostname': platform.node(),
        'username': os.getlogin() if hasattr(os, 'getlogin') else os.getenv('USER', 'unknown')
    }

def setup_readline():
    """Setup readline with proper configuration."""
    try:
        import readline
        import atexit
        import os
        
        # Set up history file
        histfile = os.path.expanduser('~/.ai_shell_history')
        try:
            readline.read_history_file(histfile)
        except FileNotFoundError:
            pass
        
        atexit.register(readline.write_history_file, histfile)
        
        # Enable tab completion
        readline.parse_and_bind('tab: complete')
        
    except ImportError:
        # Fall back to pyreadline3 on Windows
        try:
            import pyreadline3
            pyreadline3.parse_and_bind('tab: complete')
        except ImportError:
            pass  # Skip if neither is available 