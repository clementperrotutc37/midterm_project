import sys
import requests
import csv
import os
import time
import json
import io

token = "UdC5HKZB1aruy8e-Giv_fg"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_file_csv.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"URL passed as parameter: {url}")
    REST_URL = "http://localhost:8090/tasks/create/url"
    HEADERS = {"Authorization": f"Bearer {token}"}

    data = {"url": url}
    r = requests.post(REST_URL, headers=HEADERS, data=data)

    if r.status_code != 200:
        print(f"Error: Failed to create task, status code {r.status_code}")
        sys.exit(1)

    task_id = json.loads(r.text).get("task_id")
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
    processes = report.get('behavior', {}).get('processes', [])
    if not processes:
        print("No processes found in the report.")
        sys.exit(1)

    with open(jsonl_file, 'w', encoding='utf-8') as file:
        for process in processes:
            file.write(json.dumps(process) + '\n')

    csv_file = f"{url[-9:]}.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["category", "api", "time"])  # Write CSV header
        with open(jsonl_file, 'r', encoding='utf-8') as jsonl_file:
            for line in jsonl_file:
                process = json.loads(line)
                calls = process.get('calls', [])
                if not calls:
                    print("No calls found in the report.")
                    sys.exit(1)
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
