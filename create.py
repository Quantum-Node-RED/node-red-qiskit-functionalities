import os

# Base directory
base_dir = r"C:\Users\Dell\Documents\Ucl\new\node-red-qiskit-functionality\interactive-nodes"

# List of folders to create
folders = [
"X-gate",
"CX-gate",
"SX-gate",
"CZ-gate",
"H-gate",
"RX-gate",
]

def create_folder_and_files(folder_name):
    # Create full path
    full_path = os.path.join(base_dir, folder_name)
    
    # Create folder
    os.makedirs(full_path, exist_ok=True)
    print(f"Created folder: {full_path}")
    
    # Create files
    for ext in ['py', 'html', 'js']:
        file_name = f"{folder_name}.{ext}"
        file_path = os.path.join(full_path, file_name)
        with open(file_path, 'w') as f:
            f.write(f"// This is the {ext} file for {folder_name}")
        print(f"Created file: {file_path}")

# Create folders and files
for folder in folders:
    create_folder_and_files(folder)

print("All folders and files have been created successfully.")