import requests
import json

def search_rootdata(apikey, query, language='en'):
    url = "https://api.rootdata.com/open/ser_inv"
    headers = {
        "apikey": apikey,
        "language": language,
        "Content-Type": "application/json"
    }
    payload = {
        "query": query
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        filtered_data = [{"name": item["name"], "id": item["id"], "Type":item["type"],"rootdataurl": item.get("rootdataurl", "")} for item in data]
        return filtered_data
    else:
        return {
            "result": response.status_code,
            "message": response.text
        }
    
# Example usage
apikey = "6YMs21ZbMTI4ADVjzaBhiqYstawe1iFj"
query = "DWF"

result = search_rootdata(apikey, query)
print(json.dumps(result, indent=4))