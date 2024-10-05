import os
import subprocess

# Step 1: Display the main menu
def display_main_menu():
    print("Select a category:")
    print("1) Games")
    print("2) Apps")
    choice = input("Enter your choice (1 or 2): ")
    return choice

# Step 2: List the contents of the selected category (Games or Apps)
def list_folders_in_category(category):
    if not os.path.exists(category):
        print(f"Error: {category} directory does not exist.")
        return []
    
    folders = [f for f in os.listdir(category) if os.path.isdir(os.path.join(category, f))]
    
    if not folders:
        print(f"No folders found in {category}.")
    else:
        print(f"\n{category} List:")
        for i, folder in enumerate(folders, start=1):
            print(f"{i}) {folder}")
    
    return folders

# Step 3: List the Python (.py) files in the selected folder
def list_files_in_folder(category, folder):
    folder_path = os.path.join(category, folder)
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder} does not exist.")
        return []
    
    files = [f for f in os.listdir(folder_path) if f.endswith('.py')]
    
    if not files:
        print(f"No Python files found in {folder}.")
    else:
        print(f"\n{folder} Python files:")
        for i, file in enumerate(files, start=1):
            print(f"{i}) {file}")
    
    return files

# Step 4: Run the selected Python file
def run_python_file(category, folder, file):
    file_path = os.path.join(category, folder, file)
    if os.path.exists(file_path):
        print(f"Running {file}...")
        subprocess.run(["python3", file_path])  # Change "python3" to "python" if needed
    else:
        print(f"Error: {file} does not exist.")

# Main function
def main():
    while True:
        choice = display_main_menu()
        
        if choice == '1':
            category = "Games"
        elif choice == '2':
            category = "Apps"
        else:
            print("Invalid choice, please enter 1 or 2.")
            continue
        
        folders = list_folders_in_category(category)
        if not folders:
            continue
        
        folder_choice = input(f"Select a folder (1-{len(folders)}): ")
        if not folder_choice.isdigit() or int(folder_choice) < 1 or int(folder_choice) > len(folders):
            print("Invalid folder choice.")
            continue
        
        selected_folder = folders[int(folder_choice) - 1]
        files = list_files_in_folder(category, selected_folder)
        
        if not files:
            continue
        
        file_choice = input(f"Select a Python file to run (1-{len(files)}) or 'q' to go back: ")
        if file_choice == 'q':
            continue
        
        if not file_choice.isdigit() or int(file_choice) < 1 or int(file_choice) > len(files):
            print("Invalid file choice.")
            continue
        
        selected_file = files[int(file_choice) - 1]
        run_python_file(category, selected_folder, selected_file)
        
        # Optional: Add a way to exit the program
        exit_choice = input("Do you want to exit? (y/n): ")
        if exit_choice.lower() == 'y':
            break

if __name__ == "__main__":
    main()
