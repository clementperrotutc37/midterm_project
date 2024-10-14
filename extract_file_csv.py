import sys
import requests
import csv
import os


token = "UdC5HKZB1aruy8e-Giv_fg"

# Add your code to error checking if task_id is None.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_file_csv.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    print("URL passed as parameter: {}".format(url))
    REST_URL = "http://localhost:8090/tasks/create/url"
    HEADERS = {"Authorization": f"Bearer {token}"}

    data = {"url": url}
    r = requests.post(REST_URL, headers=HEADERS, data=data)

    # Add your code to error checking for r.status_code.

    task_id = r.json()["task_id"]
    print(f"Task ID: {task_id}")

    if task_id is None:
        print("Error: task_id is None")
        sys.exit(1)

    REPORT_URL = f"http://localhost:8090/tasks/report/{task_id}"
    report_response = requests.get(REPORT_URL, headers=HEADERS)

    if report_response.status_code != 200:
        print(f"Error fetching report: {report_response.status_code}")
        sys.exit(1)

    report = report_response.json()
    print(f"Report: {report}")
    
    #parse the report and extract the csv file
    calls = report.get("calls", [])
    if not calls:
        print("No calls found in the report.")
        sys.exit(1)

    csv_file = f"{url}.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["category", "api", "time"])  # Write CSV header

        for call in calls:
            category = call.get("category", "N/A")
            api = call.get("api", "N/A")
            time = call.get("time", "N/A")
            writer.writerow([category, api, time])

    print(f"CSV file '{csv_file}' created successfully.")
    if os.path.exists(csv_file):
        print(f"CSV file '{csv_file}' has been saved successfully.")
    else:
        print(f"Error: CSV file '{csv_file}' was not saved.")






