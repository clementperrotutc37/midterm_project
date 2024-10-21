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


    """

    REST_URL = "http://localhost:8090/tasks/create/file"
    SAMPLE_FILE = "/path/to/malwr.exe"
    HEADERS = {"Authorization": f"Bearer {token}"}

    with open(SAMPLE_FILE, "rb") as sample:
        files = {"file": ("temp_file_name", sample)}
        r = requests.post(REST_URL, headers=HEADERS, files=files)
        if r.status_code != 200:
            print(f"Error: Failed to create task, status code {r.status_code}")
            sys.exit(1)


    # Add your code to error checking for r.status_code.

    task_id = r.json()["task_id"]
    print(f"Task ID: {task_id}")

    if task_id is None:
        print("Error: task_id is None")
        sys.exit(1)

    REPORT_URL = f"http://localhost:8090/tasks/report/{task_id}"
    report_response = requests.get(REPORT_URL, headers=HEADERS)

    while report_response.status_code != 200:
        print("Waiting for 5 seconds before retrying...")
        time.sleep(5)
        report_response = requests.get(REPORT_URL, headers=HEADERS)

    jsonl_file = "report.jsonl"
    report = report_response.json()
    report = json.loads(json.dumps(report, ensure_ascii=False))
    processes = report.get('behavior', {}).get('processes', [])
    if not processes:
        print("No processes found in the report.")
        sys.exit(1)

    with open(jsonl_file, 'w', encoding='utf-8') as file:
        for process in processes:
            file.write(json.dumps(process) + '\n')

    
    with open(jsonl_file, 'r', encoding='utf-8') as jsonl_lines:
        i = 0 
        for line in jsonl_lines:
            i+=1
            process = json.loads(line)
            print(process)
            print(f"Processing line {i}")
            csv_file = f"{url[-9:]}_{i}.csv"
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["category", "api", "time"])  # Write CSV header
                calls = process.get('calls', [])
                print(calls)
                if not calls:
                    print("No calls found in the report.")
                    #sys.exit(1)
                for call in calls:
                    category = call.get('category', 'N/A')
                    api = call.get('api', 'N/A')
                    time = call.get('time', 'N/A')
                    writer.writerow([category, api, time])
                    
                print(f"CSV file '{csv_file}' created successfully.")
                if os.path.exists(csv_file):
                    print(f"CSV file '{csv_file}' has been saved successfully.")
                else:
                    print(f"Error: CSV file '{csv_file}' was not saved.")


    """
