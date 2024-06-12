import os
class File:
    
    def exists(file_name):
        return os.path.isfile(file_name)
    def list_files(directory):
        try:
            # Get all entries in the directory
            entries = os.listdir(directory)
            
            # Filter out directories
            files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry))]
            
            return files
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def list_folders(directory):
        try:
            # Get all entries in the directory
            entries = os.listdir(directory)
            
            # Filter out non-directories
            folders = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]
            
            return folders
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def make_directory(path):
        try:
            os.makedirs(path)
            print(f"Directory '{path}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{path}': {e}")

    def write(file_name, content):
        with open(file_name, 'w') as file:
                file.write(content)
        
