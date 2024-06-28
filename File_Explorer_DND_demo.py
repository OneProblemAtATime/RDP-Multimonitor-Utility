"""
Program: File_Explorer_DND_demo.py
Created by: OPAAT
Created Date: Thursday, June 20, 2024 (10:39.49)
Notes: This script prints the full path of a file dropped on the
script from the file explorer as a demo of how to add this
feature to futer scripts.
"""

import sys
import os

def process_file(file_path):
    if os.path.isfile(file_path):
        # Your processing logic here
        print(f"Processing file: {file_path}")
    elif os.path.isdir(file_path):
        print(f"The path {file_path} is a directory. Listing all files:")
        for root, dirs, files in os.walk(file_path):
            for name in files:
                file_full_path = os.path.join(root, name)
                print(f"Found file: {file_full_path}")
    else:
        print(f"The path {file_path} is not valid.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please drag and drop a file or directory onto this script.")
    else:
        for file_path in sys.argv[1:]:
            process_file(file_path)
    
    input("Press any key to continue...")
