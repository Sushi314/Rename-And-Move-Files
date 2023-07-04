import os
import re
import shutil

main_directory = ""  # Declare main_directory as a global variable

def rename_files_to_folder_names(folder_path):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            if filename.endswith((".mkv", ".mp4", ".avi", ".wmv", ".avchd", ".mov", ".mpg")):
                parent_folder_name = os.path.basename(folder_path)
                parent_folder_name = re.sub(r'[^\w\s-]', ' ', parent_folder_name)
                file_name, file_extension = os.path.splitext(filename)
                new_filename = f"{parent_folder_name}{file_extension}"
                new_filepath = os.path.join(folder_path, new_filename)
                os.rename(filepath, new_filepath)
                print(f"Renamed: {filename} to {new_filename}")

def move_files_to_main_directory():
    for root, dirs, files in os.walk(main_directory):
        for file in files:
            file_path = os.path.join(root, file)
            destination_path = os.path.join(main_directory, file)
            shutil.move(file_path, destination_path)
            print(f"Moved: {file_path} to {destination_path}")

def delete_empty_folders():
    for root, dirs, files in os.walk(main_directory, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                print(f"Deleted empty folder: {folder_path}")

def process_folders():
    for entry in os.scandir(main_directory):
        if entry.is_dir():
            folder_path = entry.path
            rename_files_to_folder_names(folder_path)

    move_files_to_main_directory()
    delete_empty_folders()

# Prompt user for input to specify the target directory
while True:
    main_directory = input("What is the target directory? ")
    main_directory = main_directory.strip('"\'')

    if not os.path.isdir(main_directory):
        print("Not a valid directory. Please try again.")
    else:
        break

process_folders()

# Check for files with formats other than specified
other_formats = set()
for root, dirs, files in os.walk(main_directory):
    for file in files:
        if not file.lower().endswith((".mkv", ".mp4", ".avi", ".wmv", ".avchd", ".mov", ".mpg")):
            other_formats.add(file)

# Create "Leftover From Rename" folder if there are other file formats
if other_formats:
    leftover_folder = os.path.join(main_directory, "Leftover From Rename")
    os.makedirs(leftover_folder, exist_ok=True)
    for file in other_formats:
        file_path = os.path.join(main_directory, file)
        destination_path = os.path.join(leftover_folder, file)
        shutil.move(file_path, destination_path)
        print(f"Moved {file_path} to {destination_path}")

def copy_files_to_inputed_directory(move_directory):
    for root, dirs, files in os.walk(main_directory):
        for directory in dirs:
            source_dir = os.path.join(root, directory)
            destination_dir = os.path.join(move_directory, os.path.relpath(source_dir, main_directory))
            os.makedirs(destination_dir, exist_ok=True)
            print(f"Created directory: {destination_dir}")

        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(move_directory, os.path.relpath(source_file, main_directory))
            shutil.copy2(source_file, destination_file)
            print(f"Copied file: {source_file} to {destination_file}")

    print("All files and folders copied successfully.")

def ask_to_move_files():
    while True:
        move_files = input("Would you like to move files to another directory? (yes/no): ").lower()

        if move_files in ["yes", "ya", "y"]:
            # Ask for target directory
            while True:
                move_directory = input("What is the target directory? ").strip('"\'')

                if not os.path.isdir(move_directory):
                    print("Not a valid directory. Please try again.")
                else:
                    break

            # Confirm before copying
            confirm_copy = input(f"Are you sure you want to copy files to {move_directory}? (yes/no): ").lower()

            if confirm_copy in ["yes", "ya", "y", "true"]:
                # Perform the copy
                copy_files_to_inputed_directory(move_directory)
                print("Files copied successfully.")
                break
            elif confirm_copy in ["no", "nope", "na", "n", "false"]:
                print("Files will not be copied.")
                break
            else:
                print("Not a valid response. Please try again.")
        elif move_files in ["no", "na", "nope", "n"]:
            print("Files will not be moved.")
            break
        else:
            print("Not a valid response. Please try again.")

        # Prompt user for input to specify the target directory
        while True:
            main_directory = input("What is the target directory? ")
            main_directory = main_directory.strip('"\'')

            if not os.path.isdir(main_directory):
                print("Not a valid directory. Please try again.")
            else:
                break

ask_to_move_files()





# Pause the console
input("Process completed. Press Enter to exit...")
