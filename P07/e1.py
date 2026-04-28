import http.client
import json

SERVER = 'rest.ensembl.org'
ENDPOINT = '/info/ping'
PARAMS = '?content-type=application/json'
FULL_PATH = ENDPOINT + PARAMS

print(f"Server: {SERVER}")
print(f"URL: {SERVER}{FULL_PATH}")

conn = http.client.HTTPConnection(SERVER)
conn.request("GET", FULL_PATH)

response = conn.getresponse()
print(f"Response received!: {response.status} {response.reason}")

data = response.read()
json_response = json.loads(data.decode('utf-8'))

if json_response.get('ping') == 1:
    print("PING OK! The database is running!")

conn.close()