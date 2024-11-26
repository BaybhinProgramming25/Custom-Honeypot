import requests 
import json 
import os 

from dotenv import load_dotenv

# Load environmental variable
load_dotenv()

# Send the data to Kibana
def post_to_kibana(json_data):

    kibana_url = os.getenv('KIBANA_URL')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(kibana_url, data=json.dumps(json_data), headers=headers)

    if response.status_code == 201:
        print(f"Data sent to Kibana: {json_data}")
    else:
        print(f"Failed to send data to Kibana: {response.status_code}, {response.text}")