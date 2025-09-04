import requests
import json

API_KEY = "your_n8n_api_key"
N8N_URL = "https://your-subdomain.n8n.cloud/api/v1/workflows"

with open("workflows/task_automation.json") as f:
    workflow = json.load(f)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(N8N_URL, headers=headers, json=workflow)
print(response.status_code, response.json())
