from typing import Dict
from .utils import format_text, reset_format

# ASCII Art for Santra
SANTRA_ART = r"""
   _____              _                 
  / ____|            | |                
 | (___   __ _ _ ___ | |_ _ __ __ _ 
  \___ \ / _` | '__  | __| '__/ _` |
  ____) | (_| | |  | | |_| | | (_| |   
 |_____/ \__,_|_|  |_\__ |_|  \__,_|  
"""


def get_welcome_message() -> str:
    """Return formatted welcome message with ASCII art."""
    return f"""
{format_text('cyan', bold=True)}{SANTRA_ART}{reset_format()}
{format_text('yellow')}╭──────────────────────────────────────────────╮{reset_format()}
{format_text('yellow')}│  Welcome to Santra Shell Assistant!          │{reset_format()}
{format_text('yellow')}│  Your AI-powered terminal companion          │{reset_format()}
{format_text('yellow')}╰──────────────────────────────────────────────╯{reset_format()}
{format_text('green')}Type 'help' for available commands or ask me anything!{reset_format()}
"""

def format_command_output(command: str, output: str) -> str:
    """Format command output."""
    return f"{output}"

def format_error(message: str) -> str:
    """Format error messages."""
    return f"{format_text('red', bold=True)}Error: {reset_format()}{format_text('red')}{message}{reset_format()}"

def format_success(message: str) -> str:
    """Format success messages."""
    return f"{format_text('green', bold=True)}Success: {reset_format()}{format_text('green')}{message}{reset_format()}"

def format_info(message: str) -> str:
    """Format informational messages."""
    return f"{format_text('cyan', bold=True)}Thinking: {reset_format()}{format_text('cyan')}{message}{reset_format()}"

def format_command_prompt() -> str:
    """Format the command input prompt."""
    return f"{format_text('magenta', bold=True)}santra ❯ {reset_format()}"

def format_command_suggestion(command: str) -> str:
    """Format command suggestions."""
    return f"""
{format_text('yellow', bold=True)}Command: {reset_format()}{format_text('cyan', bold=True)}{command}{reset_format()}
{format_text('yellow')}Execute command? (y/n): {reset_format()}"""