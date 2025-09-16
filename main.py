
from project_ops import run_selection_manager, allowed_projects, AllowedProject
from cli_utils import ask_question, ask_selection

SELECTION_OPTIONS = [
    "Full Project",
    "Chatbot + Switchboard",
    "Chatbot + Emulator",
    "Chatbot",
    "Switchboard",
    "Chatstats",
    "SwitchboardAPI",
    "Reset"
]

def main():
    print("Hello, World! This is your Python project entry point.")
    selection = ask_selection("Select a project option:", SELECTION_OPTIONS)
    print(f"You selected: {selection}")
    run_selection_manager(selection)

if __name__ == "__main__":
    main()
