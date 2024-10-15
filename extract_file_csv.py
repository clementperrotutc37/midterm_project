import sys
import requests
import csv
import os
import time
import json




token = "UdC5HKZB1aruy8e-Giv_fg"

# Add your code to error checking if task_id is None.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_file_csv.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    print("URL passed as parameter: {}".format(url))
    REST_URL = "http://localhost:8090/tasks/create/url"
    HEADERS = {"Authorization": "Bearer {}".format(token)}

    data = {"url": url}
    r = requests.post(REST_URL, headers=HEADERS, data=data)

    # Add your code to error checking for r.status_code.
    if r.status_code != 200:
        print("Error: Failed to create task, status code {}".format(r.status_code))
        sys.exit(1)

    task_id = json.loads(r.text).get("task_id")
    print("Task ID: {}".format(task_id))

    if task_id is None:
        print("Error: task_id is None")
        sys.exit(1)

    REPORT_URL = "http://localhost:8090/tasks/report/{}".format(task_id)
    report_response = requests.get(REPORT_URL, headers=HEADERS)

    while report_response.status_code != 200:
        #print("Error fetching report: {}".format(report_response.status_code))
        print("Waiting for 5 seconds before retrying...")
        time.sleep(5)
        report_response = requests.get(REPORT_URL, headers=HEADERS)

    report = json.loads(report_response.text)

    print("Report: {}".format(report))
    
    #parse the report and extract the csv file

    processes = report['behavior']['processes']
    if not processes:
        print("No processes found in the report.")
        sys.exit(1)

    csv_file = "{}.csv".format(url)
    with open(csv_file, mode='wb') as file:
        writer = csv.writer(file)
        writer.writerow(["category", "api", "time"])  # Write CSV header
        for process in processes:
            calls = process['calls']
            if not calls:
                print("No calls found in the report.")
                sys.exit(1)
            for call in calls:
                category = call['category']                 
                api = call['api']
                time = call['time']
                writer.writerow([category, api, time])

    print("CSV file '{}' created successfully.".format(csv_file))
    if os.path.exists(csv_file):
        print("CSV file '{}' has been saved successfully.".format(csv_file))
    else:
        print("Error: CSV file '{}' was not saved.".format(csv_file))
