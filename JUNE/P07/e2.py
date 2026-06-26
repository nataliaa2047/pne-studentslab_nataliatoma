import http.client
import json

# List of gene names to look up
gene_names = [
    "FRAT1", "ADA", "FXN", "RNU6-269P", "MIR633",
    "TTTY4C", "RBMY2YP", "FGFR3", "KDR", "ANK2"
]

# Initialize the empty dictionary as required by the exercise
genes = {}

SERVER = 'rest.ensembl.org'
# Header required to tell the Ensembl server we want JSON data back
HEADERS = {"Content-Type": "application/json"}

# Open a single connection to the Ensembl server
conn = http.client.HTTPConnection(SERVER)

# Loop through each gene name to fetch its stable identifier
for name in gene_names:
    # Build the endpoint path for human (homo_sapiens) gene lookup
    endpoint = f"/lookup/symbol/homo_sapiens/{name}"

    # Send the GET request
    conn.request("GET", endpoint, headers=HEADERS)

    # Get the server's response
    response = conn.getresponse()

    if response.status == 200:
        # Read and decode the raw JSON bytes
        data = response.read()
        json_response = json.loads(data.decode('utf-8'))

        # Extract the 'id' field and save it into our dictionary
        genes[name] = json_response.get('id')
    else:
        # Clear the response buffer in case of an error to prevent connection blocking
        response.read()
        print(f"Error fetching data for {name}: {response.status}")

# Always close the connection when finished
conn.close()

# --- Print the results exactly as shown in the exercise terminal ---
print("Dictionary of Genes!")
print(f"There are {len(genes)} genes in the dictionary:")
print()

for gene, gene_id in genes.items():
    print(f"{gene}: --> {gene_id}")