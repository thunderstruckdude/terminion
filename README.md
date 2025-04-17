# AI Shell

An intelligent terminal assistant powered by Claude and Gemini AI models. This tool helps you interact with your terminal using natural language and provides AI-powered assistance for your command-line tasks.

## Features

- Natural language command processing
- Support for both Claude (Anthropic) and Gemini (Google) AI models
- Direct command execution with '!' prefix
- Question mode with '?' prefix or suffix
- Tab completion for files and directories
- Easy configuration management
- ANSI color support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai_shell.git
cd ai_shell
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

4. Set up your API keys:
- Get an API key from Anthropic (Claude): https://console.anthropic.com/
- Get an API key from Google AI Studio (Gemini): https://makersuite.google.com/app/apikey

5. On first run, you'll be prompted to enter your API keys and select your preferred model.

## Usage

1. Start the assistant:
```bash
ai-shell
```

2. Basic commands:
- Type natural language commands to get AI assistance
- Use '!' prefix to execute commands directly without AI processing
- Use '?' prefix or suffix to ask questions about commands or system
- Type '--config' to update settings
- Type '--help' to see available commands
- Type 'quit' or press Ctrl+C to exit

## Examples

```bash
# Ask about a command
how do I find all python files in the current directory?

# Direct command execution
!ls -la

# Ask about command output
ls -la | grep "py" ?

# Get help with error messages
? what does "permission denied" mean?
```

## Configuration

Your API keys and preferences are stored in `~/.config/ai_shell/config.json`. You can update these settings at any time using the '--config' command within the application.
