import os
import platform
from .utils import format_text, reset_format, get_terminal_size, setup_readline, enable_ansi_support
from .config import setup_wizard, load_config
from .assistant import AIAssistant

def main():
    """Main entry point for the AI Shell application."""
    config = load_config()
    if not config:
        print("First-time setup required!")
        setup_wizard()
        config = load_config()

    enable_ansi_support()
    setup_readline()

    assistant = AIAssistant(config=config, model_name="gemini")
    
    while True:
        try:
            columns, _ = get_terminal_size()
            prompt = f"\n{format_text('green', bold=True)}{os.getcwd()}$ {reset_format()}"
            user_input = input(prompt)

            if len(prompt) + len(user_input) > columns:
                print()  # Move to the next line if input is too long

            if user_input.lower() == 'quit':
                print(format_text('red', bold=True) + "\nTerminating..." + reset_format())
                break

            if user_input.lower() == "--config":
                setup_wizard()
                config = load_config()
                assistant = AIAssistant(config=config, model_name="gemini")
                print(f"{format_text('yellow', bold=True)}Configuration updated!{reset_format()}")
                continue

            if user_input.lower() == "--help":
                print(f"""{format_text('blue')}Available Commands:
- Use natural language to ask questions or request actions
- Start with '!' to execute commands directly
- End with '?' to ask about a command or its output
- Use 'clear' to clear the terminal
- Use '--config' to update settings
- Use 'quit' or Ctrl+C to exit
- Tab completion is enabled for files and folders{reset_format()}""")
                continue

            if not user_input.strip():
                continue

            result = assistant.execute_command(user_input)
            if result:
                print(result)

        except KeyboardInterrupt:
            print(format_text('red', bold=True) + "\nTerminating..." + reset_format())
            break
        except Exception as e:
            print(f"{format_text('red')}Error: {str(e)}{reset_format()}")

if __name__ == "__main__":
    main() 