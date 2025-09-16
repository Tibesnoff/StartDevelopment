def ask_question(question: str) -> str:
    """
    Prompts the user with a question and returns the input from the command line.
    """
    return input(question + " ")


def ask_selection(question: str, options: list[str]) -> str:
    """
    Prompts the user to select from a list of options and returns the selected value.
    """
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
