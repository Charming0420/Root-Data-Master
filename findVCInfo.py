import requests

def get_org_info(apikey, org_id, include_team=False, include_investments=False):
    url = "https://api.rootdata.com/open/get_org"
    headers = {
        "apikey": apikey,
        "Content-Type": "application/json"
    }
    payload = {
        "org_id": org_id,
        "include_team": include_team,
        "include_investments": include_investments
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "result": response.status_code,
            "message": response.text
        }

# 在這裡輸入你的apikey和org_id
apikey = "6YMs21ZbMTI4ADVjzaBhiqYstawe1iFj"
org_id = 4075

result = get_org_info(apikey, org_id, include_team=True, include_investments=True)
print(result)