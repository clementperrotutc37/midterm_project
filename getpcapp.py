import requests
import csv
import sys

# Define the base URL and headers
base_url = "http://localhost:8090/pcap/get/"
headers = {"Authorization": "Bearer UdC5HKZB1aruy8e-Giv_fg"}

# Open the CSV file
#with open("TaskIDtoFilename.csv", newline='') as csvfile:
#    csv_reader = csv.reader(csvfile)
    
    # Loop through each row in the CSV
task_id = sys.argv[1]      # First column: Task ID
filename = sys.argv[2]       # Second column: Filename

# Construct the URL for the current task ID
url = f"{base_url}{task_id}"

# Send the request to download the PCAP for the current task ID
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Save the PCAP with the corresponding filename
    with open(f"{filename}.pcap", "wb") as file:
        file.write(response.content)
    print(f"PCAP file for Task ID {task_id} saved as {filename}.pcap")
else:
    print(f"Failed to retrieve PCAP for Task ID {task_id}. Status code: {response.status_code}")

