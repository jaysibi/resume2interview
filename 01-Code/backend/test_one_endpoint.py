import requests

response = requests.post('http://127.0.0.1:8000/gap-analysis/?resume_id=5&jd_id=4')
print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')
