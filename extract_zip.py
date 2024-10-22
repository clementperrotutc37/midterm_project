import sys
import requests
import csv
import os
import time
import json
import io
import zipfile

token = "UdC5HKZB1aruy8e-Giv_fg"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_file_csv.py <URL>")
        sys.exit(1)
    
    path_zip = sys.argv[1]
    print(f"Path passed as parameter: {path_zip}")

    # Create the path if it does not exist
    extracted_files_path = "/home/username/extracted_files"
    if not os.path.exists(extracted_files_path):
        os.makedirs(extracted_files_path)

    # Extract the zip file with password
    zip_password = b"infected"  # Replace with your actual password
    with zipfile.ZipFile(path_zip, 'r') as zip_ref:
        zip_ref.extractall("/home/username/extracted_files", pwd=zip_password)

    # Loop through the extracted files
    extracted_files_path = "/home/username/extracted_files"
    for root, dirs, files in os.walk(extracted_files_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Extracted file: {file_path}")