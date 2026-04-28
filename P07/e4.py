import http.client
import json


class Seq:
    def __init__(self, sequence):
        self.sequence = sequence.upper()

    def get_length(self):
        return len(self.sequence)

    def count_bases(self):
        # Returns a dictionary of counts for A, C, G, T
        return {base: self.sequence.count(base) for base in "ACGT"}

    def get_percentages(self, counts, total):
        # Returns a dictionary of percentages
        return {base: (count / total) * 100 for base, count in counts.items()}

    def get_most_frequent(self, counts):
        # Finds the key with the maximum value
        return max(counts, key=counts.get)


def get_gene_id(gene_name):
    # Lookup the Ensembl ID from the gene symbol
    conn = http.client.HTTPConnection('rest.ensembl.org')
    params = f'/xrefs/symbol/homo_sapiens/{gene_name}?content-type=application/json'
    conn.request("GET", params)
    response = conn.getresponse()

    if response.status != 200:
        return None

    data = json.loads(response.read().decode('utf-8'))
    # The API returns a list, we take the first 'id' found
    return data[0].get('id') if data else None


def get_gene_data(gene_id):
    # Fetch sequence and metadata using the Ensembl ID
    conn = http.client.HTTPConnection('rest.ensembl.org')
    params = f'/sequence/id/{gene_id}?content-type=application/json'
    conn.request("GET", params)
    response = conn.getresponse()

    if response.status != 200:
        return None

    return json.loads(response.read().decode('utf-8'))


# --- Main Program ---
gene_name = input("Write the gene name: ")

# 1. Get the ID
gene_id = get_gene_id(gene_name)
if not gene_id:
    print(f"Error: Could not find ID for {gene_name}")
else:
    # 2. Get the Sequence info
    data = get_gene_data(gene_id)

    print(f"\nServer: rest.ensembl.org")
    print(f"URL: rest.ensembl.org/sequence/id/{gene_id}?content-type=application/json")
    print(f"Response received!: 200 OK\n")

    print(f"Gene: {gene_name}")
    print(f"Description: {data['desc']}")

    # 3. Process using Seq class
    seq_obj = Seq(data['seq'])
    print("New sequence created!")

    total = seq_obj.get_length()
    counts = seq_obj.count_bases()
    percentages = seq_obj.get_percentages(counts, total)
    most_freq = seq_obj.get_most_frequent(counts)

    print(f"Total length: {total}")
    for base in "ACGT":
        print(f"{base}: {counts[base]} ({percentages[base]:.1f}%)")
    print(f"Most frequent Base: {most_freq}")