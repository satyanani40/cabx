import os, json
import requests
url = "http://localhost:8000/api/mongodb-metrics/feqor-metrics"
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }
path_to_json = '/mnt/git/feqor/mongodb_feqor_metrics/'
json_files = [os.path.join(path_to_json,pos_json) for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for json_file in json_files:
    with open(json_file, 'r') as f:
        payload = json.load(f)
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        print(response.status_code)
print("completed")