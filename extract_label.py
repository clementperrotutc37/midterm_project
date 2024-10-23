import requests 
import json # Import the json module to handle saving JSON data 
# Replace 'your_api_key' with your actual VirusTotal API key 
api_key = "a3796ea0a8e15ed88bef506f3d084c5326ce2580cbe5e6224f1d6ab197b51ff4" 
# Replace 'file_id_or_hash' with the file's actual hash (MD5, SHA1, or SHA256) 
file_id_or_hash = "aca2d12934935b070df8f50e06a20539" 
# URL for querying file reports on VirusTotal 
url = f"https://www.virustotal.com/api/v3/files/{file_id_or_hash}" 
# Headers need to include your API key for authorization 
headers = { "accept": "application/json", "x-apikey": api_key } 
# Send the GET request to VirusTotal 
response = requests.get(url, headers=headers) 
# Check if the request was successful 
if response.status_code == 200: 
    json_response = response.json() # Save the response to a file in one line 
    with open(f'virustotal_report_{file_id_or_hash}.json', 'w') as json_file: 
        json.dump(json_response, json_file, separators=(',', ':')) # Save JSON in one line print("JSON response saved to file.") 
else: 
    print(f"Error: {response.status_code}")