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
        
        # Git start command
        git_start_match = re.match(r'^git\s+start\s+(.+)$', command)
        if git_start_match:
            repo_url = git_start_match.group(1)
            return self._git_start(repo_url)
        
        # Clear command
        if command.lower() == 'clear':
            os.system('cls' if platform.system() == 'Windows' else 'clear')
            print(get_welcome_message())
            return ""
        
        if command.strip().endswith('?'):
            # Get explanation for the command
            return self._explain_command(command.rstrip('?'))
        
        # Process through AI
        return self._process_with_ai(command)
    
    def _git_start(self, repo_url: str) -> str:
        """Initialize a git repository and set up remote."""
        git_commands = f"git init && git add . && git commit -m \"first commit\" && git branch -M main && git remote add origin {repo_url} && git push -u origin main"
        print(format_command_suggestion(git_commands))
        
        # Get user approval
        approval = input().lower().strip()
        if approval == 'y':
            result = self._execute_shell_command(git_commands)
            return format_command_output(git_commands, result)
        else:
            return format_info("Git initialization cancelled.")
    
    def _execute_shell_command(self, command: str) -> str:
        """Execute a shell command directly."""
        try:
            # Use an actual shell process to properly handle shell operators like &&
            if platform.system() == 'Windows':
                shell_cmd = ['cmd.exe', '/c', command]
            else:
                shell_cmd = [os.environ.get('SHELL', '/bin/bash'), '-c', command]
            
            result = subprocess.run(
                shell_cmd,
                text=True,
                capture_output=True,
                stdin=subprocess.DEVNULL,
            )
            output = result.stdout or result.stderr
            return output if output else format_success("Command executed successfully.")
        except Exception as e:
            return format_error(f"Error executing command: {str(e)}")
        
    def _explain_command(self, command: str) -> str:
        """Get explanation for a command from Gemini."""
        context = self.get_context()
        try:
            response = self.client.generate_content(
                f"""Context:\n{context}\n\nCommand to explain: {command}\n\n
    You are a helpful terminal assistant. Provide a clear, one-line explanation of what this command does.
    Focus on practical effects and key options/flags. Keep it concise and user-friendly.
    Do not provide the command syntax or examples - just explain what it does.

    Example format:
    For 'dir /s': "Lists all files and folders recursively in the current directory and all subdirectories"
    For 'ping 8.8.8.8': "Tests network connectivity by sending data packets to Google's DNS server"

    NOTE: Consider the OS from Context when explaining OS-specific commands."""
            )
            return format_info(response.text.strip())
        except Exception as e:
            return format_error(f"Error getting explanation: {str(e)}")
    
    def _process_with_ai(self, user_input: str) -> str:
        """Process user input through Gemini and handle command execution."""
        context = self.get_context()
        try:
            response = self.client.generate_content(
                f"""Context:\n{context}\n\nUser Input: {user_input}\n\n
You are a helpful terminal assistant. If the user wants to execute a command or a set of commands, respond with just the command(s) in backticks.
For example, if the user asks to list files, respond with: `ls -la`
If the user asks a question, provide a helpful answer.
Keep responses concise and focused on the task.
"""
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