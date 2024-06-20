"""
Program: File_Explorer_DND_demo.py
Created by: Joshua Merritt
Created Date: Thursday, June 20, 2024 (10:39.49)
Notes: This script prints the full path of a file dropped on the
script from the file explorer as a demo of how to add this
feature to futer scripts.
"""

import sys
import os

def process_file(file_path):
    if not os.path.isfile(file_path):
        print(f"The path {file_path} is not a valid file.")
        return

    # Your processing logic here
    print(f"Processing file: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please drag and drop a file onto this script.")
    else:
        for file_path in sys.argv[1:]:
            process_file(file_path)
    input("Press any key to continue...")
