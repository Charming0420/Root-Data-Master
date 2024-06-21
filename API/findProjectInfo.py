import requests

def get_project_info(apikey, project_id=None, include_team=False, include_investors=False, contract_address=None):
    url = "https://api.rootdata.com/open/get_item"
    headers = {
        "apikey": apikey,
        "language": "en",
        "Content-Type": "application/json"
    }
    payload = {
        "project_id": project_id,
        "include_team": include_team,
        "include_investors": include_investors,
        "contract_address": contract_address
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "result": response.status_code,
            "message": response.text
        }

# Example usage
apikey = "6YMs21ZbMTI4ADVjzaBhiqYstawe1iFj"  # Insert your API key here
project_id = 471
include_team = True
include_investors = True

project_info = get_project_info(apikey, project_id, include_team, include_investors)
print(project_info)