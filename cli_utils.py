import os
import sys
import msvcrt

def ask_question(question: str) -> str:
    return input(question + " ")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu_with_navigation(title: str, options: list[tuple[str, str]]) -> str:
    selected_index = 0
    
    while True:
        clear_screen()
        print(f"🚀 {title}")
        print("=" * (len(title) + 4))
        print("Use ↑↓ arrows to navigate, Enter to select, Q to quit")
        print()
        
        for i, (key, description) in enumerate(options):
            if i == selected_index:
                print(f"  ▶ {description} ◀")
            else:
                print(f"    {description}")
        
        print()
        print("Press Enter to select, Q to quit")
        
        key = get_key()
        
        if key == 'up' and selected_index > 0:
            selected_index -= 1
        elif key == 'down' and selected_index < len(options) - 1:
            selected_index += 1
        elif key == 'enter':
            return options[selected_index][0]
        elif key == 'q':
            return 'Q'

def get_key():
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H':
                    return 'up'
                elif key == b'P':
                    return 'down'
            elif key == b'\r':
                return 'enter'
            elif key == b'q' or key == b'Q':
                return 'q'

def show_menu(title: str, options: dict[str, str]) -> str:
    print(f"\n{title}")
    print("=" * len(title))
    for key, description in options.items():
        print(f"  {key}. {description}")
    print()

def get_choice(options: dict[str, str]) -> str:
    while True:
        choice = input("Enter your choice: ").strip().upper()
        if choice in options:
            return choice
        print("Invalid choice. Please try again.")

def ask_selection(question: str, options: list[str]) -> str:
    print(question)
    for idx, option in enumerate(options, 1):
        print(f"  {idx}. {option}")
    while True:
        choice = input("Enter the number of your choice: ")
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        print("Invalid selection. Please try again.")
