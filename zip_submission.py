import os
import zipfile

def zip_project():
    zip_filename = "FA23-BCS-161.zip"
    print(f"Creating submission zip bundle: {zip_filename}...")
    
    # Exclude list for clean zipping
    exclude_dirs = {
        ".git", 
        "node_modules", 
        ".venv", 
        "venv", 
        "__pycache__", 
        "build", 
        ".vscode", 
        ".idea",
        "postgres_data"
    }
    exclude_files = {
        zip_filename,
        "sample.txt",
        ".env"
    }
    
    count = 0
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(os.getcwd()):
            # Filter out excluded directories in-place
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files:
                    continue
                if file.endswith(('.pyc', '.log', '.zip', '.tar.gz')):
                    continue
                    
                full_path = os.path.join(root, file)
                # Store relative path inside zip
                rel_path = os.path.relpath(full_path, os.getcwd())
                zipf.write(full_path, rel_path)
                count += 1
                
    print(f"Successfully zipped {count} files into {zip_filename}!")

if __name__ == "__main__":
    zip_project()
