import http.client
import json

SERVER = 'rest.ensembl.org'
GENE_ID = 'ENSG00000207865' # ID for MIR633
ENDPOINT = f'/sequence/id/{GENE_ID}'
PARAMS = '?content-type=application/json'
URL = ENDPOINT + PARAMS

conn = http.client.HTTPConnection(SERVER)
conn.request("GET", URL)

response = conn.getresponse()

print(f"Server: {SERVER}")
print(f"URL: {SERVER}{URL}")
print(f"Response received!: {response.status} {response.reason}")

data = response.read().decode('utf-8')
gene_data = json.loads(data)

print(f"\nGene: MIR633")
print(f"Description: {gene_data.get('desc')}")
print(f"Bases: {gene_data.get('seq')}")

conn.close()