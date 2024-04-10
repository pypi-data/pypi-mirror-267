import os
import shutil

def organize_files(source_path):
    # Dictionary to map file extensions to their respective directories
    extension_to_directory = {
        "txt": "Text Files",
        "pdf": "PDFs",
        "jpg": "Images",
        "png": "Images",
        "mp3": "Music",
        "mp4": "Videos",
        "docx": "Documents",
        "py": "Python",
        "exe": "Applications",
        "html": "Hyper Text Markup Language",
        "css": "Cascading Style Sheets",
        "js": "JavaScript",
        "php": "PHP",
        "zis": "ZIS",
        # Add more file extensions and corresponding directories as needed
    }
    
    # Function to organize a single file
    def organize_file(file_path):
        file_name = os.path.basename(file_path)
        file_extension = file_name.split(".")[-1].lower()
        if file_extension in extension_to_directory:
            destination_directory = extension_to_directory[file_extension]
        else:
            destination_directory = "Others"
        
        destination_dir = os.path.join(parent_dir, "OrganizedFiles", destination_directory)
        os.makedirs(destination_dir, exist_ok=True)
        
        destination_file_path = os.path.join(destination_dir, file_name)
        print(f"Moving {file_path} to {destination_file_path}")
        shutil.move(file_path, destination_file_path)
    
    # Determine if the source path is a file or a directory
    if os.path.isdir(source_path):
        source_dir = source_path
    elif os.path.isfile(source_path):
        source_dir = os.path.dirname(source_path)
        organize_file(source_path)
        return
    else:
        print(f"Invalid source path: {source_path}")
        return
    
    # Get the parent directory of the source directory
    parent_dir = os.path.abspath(os.path.join(source_dir, os.pardir))
    
    # Check if "OrganizedFiles" directory exists
    organized_files_dir = os.path.join(parent_dir, "OrganizedFiles")
    if not os.path.exists(organized_files_dir):
        os.makedirs(organized_files_dir)
    
    # Organize files within the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file_path = os.path.join(root, file)
            organize_file(source_file_path)

if __name__ == "__main__":
    source_directory = input("Enter the directory to organize: ")
    organize_files(source_directory)
    print("Files organized successfully!")
