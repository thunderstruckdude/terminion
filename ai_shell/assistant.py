import os
import subprocess
import platform
import re
from typing import Dict, Any
import google.generativeai as genai
from .utils import get_system_info, format_text, reset_format
from .visuals import (
    get_welcome_message,
    format_command_output,
    format_error,
    format_success,
    format_info,
    format_command_prompt,
    format_command_suggestion
)

class AIAssistant:
    def __init__(self, config: Dict[str, Any], model_name: str):
        self.config = config
        self.setup_client()
        self.system_info = get_system_info()
        print(get_welcome_message())
        
    def setup_client(self):
        """Initialize Gemini client."""
        genai.configure(api_key=self.config["api_keys"]["google"])
        self.client = genai.GenerativeModel('gemini-1.5-flash')
    
    def get_context(self) -> str:
        """Get the current system context."""
        return f"""Current working directory: {os.getcwd()}
Operating System: {self.system_info['os']} {self.system_info['os_release']}
Python Version: {self.system_info['python_version']}
Shell: {os.environ.get('SHELL', 'unknown')}"""

    def execute_command(self, command: str) -> str:
        """Execute a command or process it through AI."""
        # Direct command execution
        if command.startswith('!'):
            result = self._execute_shell_command(command[1:])
            return format_command_output(command[1:], result)
        
        # Clear command
        if command.lower() == 'clear':
            os.system('cls' if platform.system() == 'Windows' else 'clear')
            print(get_welcome_message())
            return ""
        
        # Process through AI
        return self._process_with_ai(command)
    
    def _execute_shell_command(self, command: str) -> str:
        """Execute a shell command directly."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                text=True,
                capture_output=True
            )
            output = result.stdout or result.stderr
            return output if output else format_success("Command executed successfully.")
        except Exception as e:
            return format_error(f"Error executing command: {str(e)}")
    
    def _process_with_ai(self, user_input: str) -> str:
        """Process user input through Gemini and handle command execution."""
        context = self.get_context()
        try:
            response = self.client.generate_content(
                f"""Context:\n{context}\n\nUser Input: {user_input}\n\n
You are a helpful terminal assistant. If the user wants to execute a command, respond with just the command in backticks.
For example, if the user asks to list files, respond with: `ls -la`
If the user asks a question, provide a helpful answer.
Keep responses concise and focused on the task."""
            )
            
            # Extract command if found
            command_match = re.search(r'`([^`]+)`', response.text)
            if command_match:
                command = command_match.group(1)
                print(format_command_suggestion(command))
                
                # Get user approval
                approval = input().lower().strip()
                if approval == 'y':
                    result = self._execute_shell_command(command)
                    return format_command_output(command, result)
                else:
                    return format_info("Command execution cancelled.")
            
            return format_info(response.text)
            
        except Exception as e:
            return format_error(f"Error processing with Gemini: {str(e)}") 