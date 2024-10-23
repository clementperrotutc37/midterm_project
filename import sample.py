import requests
import os
import csv
import sys

# Your API token
token = "UdC5HKZB1aruy8e-Giv_fg"

# Specify the folder path here (including subfolders)
folder_path = "/home/username/Downloads/virushare-20-fusion/virushare-20/PEs"

# CSV file to write the task ID and filename
csv_file_path = "TaskIDtoFilename.csv"

# Cuckoo API URL for file submission
REST_URL = "http://localhost:8090/tasks/create/file"
HEADERS = {"Authorization": f"Bearer {token}"}

def process_folder(folder_path, csv_writer):
    # Walk through all subfolders and files in the directory
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Check if the file is a valid executable (.exe)
            if filename.lower():#.endswith('.exe'):
                print(f"Processing file: {file_path}")
                
                # Submit file to Cuckoo
                with open(file_path, 'rb') as file:
                    response = requests.post(REST_URL, headers=HEADERS, files={'file': file})
                    
                    if response.status_code == 200:
                        task_id = response.json().get("task_id")
                        print(f"Task ID: {task_id} for {filename}")

                        # Write task ID and filename to CSV
                        csv_writer.writerow([task_id, filename])
                    else:
                        print(f"Failed to submit {filename}. Status code: {response.status_code}")
            else:
                print(f"Skipping {file_path} (not a valid .exe file).")

if __name__ == "__main__":
    print(f"Processing folder: {folder_path}")

    # Open CSV file for writing task IDs and filenames
    with open(csv_file_path, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Task ID', 'Filename'])  # Write header row

        # Process the folder
        process_folder(folder_path, csv_writer)

    print("Processing completed.")
