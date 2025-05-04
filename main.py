import subprocess
import sys

def display_menu():
    """Display the main menu for dataset selection"""
    print("\nDataset Analysis Tool")
    print("---------------------")
    print("1. Analyze Dataset 1")
    print("2. Analyze Dataset 2")
    print("3. Exit")
    print("---------------------")

def get_user_choice():
    """Get and validate user input"""
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print("Invalid input. Please enter 1, 2, or 3.")

def run_dataset_analysis(script_name):
    """Run a dataset analysis script"""
    try:
        subprocess.run([sys.executable, script_name], check=True)
        input("\nAnalysis complete. Press Enter to return to the main menu...")
    except subprocess.CalledProcessError:
        print(f"\nError running {script_name}")
        input("Press Enter to continue...")

def main():
    """Main program function handling menu navigation"""
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == "1":
            run_dataset_analysis("dataset1.py")
        elif choice == "2":
            run_dataset_analysis("dataset2.py")
        elif choice == "3":
            print("\nExiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()