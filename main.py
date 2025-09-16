
from project_ops import run_selection_manager
from cli_utils import show_menu_with_navigation

def main():
    menu_options = [
        ("F", "Full Project (All components)"),
        ("CS", "Chatbot + Switchboard"), 
        ("CE", "Chatbot + Emulator"),
        ("C", "Chatbot Only"),
        ("S", "Switchboard Only"),
        ("ST", "Chatstats Only"),
        ("API", "Switchboard API Only"),
        ("R", "Reset All Configs")
    ]
    
    choice = show_menu_with_navigation("Project Launcher", menu_options)
    run_selection_manager(choice)

if __name__ == "__main__":
    main()
