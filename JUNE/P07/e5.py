import http.client
import json


# Reusing the Seq class from Exercise 4
class Seq:
    def __init__(self, sequence):
        self.sequence = sequence.upper()

    def get_length(self):
        return len(self.sequence)

    def count_bases(self):
        return {base: self.sequence.count(base) for base in "ACGT"}

    def get_percentages(self, counts, total):
        return {base: (count / total) * 100 for base, count in counts.items()}

    def get_most_frequent(self, counts):
        return max(counts, key=counts.get)


# Dictionary of genes (from Exercise 2)
genes = {
    "FRAT1": "ENSG00000104683",
    "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060",
    "RNU6-269P": "ENSG00000277856",
    "MIR633": "ENSG00000207865",
    "TTTY4C": "ENSG00000227918",
    "RBMY2YP": "ENSG00000231649",
    "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
}

# Iterate through the dictionary
for gene_name, gene_id in genes.items():
    # 1. Fetch data
    conn = http.client.HTTPConnection('rest.ensembl.org')
    params = f'/sequence/id/{gene_id}?content-type=application/json'
    conn.request("GET", params)
    response = conn.getresponse()

    # 2. Print status and process
    print(f"Server: rest.ensembl.org")
    print(f"URL: rest.ensembl.org{params}")
    print(f"Response received!: {response.status} {response.reason}\n")

    if response.status == 200:
        data = json.loads(response.read().decode('utf-8'))

        # 3. Output info
        print(f"Gene: {gene_name}")
        print(f"Description: {data['desc']}")

        seq_obj = Seq(data['seq'])
        print("New sequence created!")

        total = seq_obj.get_length()
        counts = seq_obj.count_bases()
        percentages = seq_obj.get_percentages(counts, total)
        most_freq = seq_obj.get_most_frequent(counts)

        print(f"Total length: {total}")
        for base in "ACGT":
            print(f"{base}: {counts[base]} ({percentages[base]:.1f}%)")
        print(f"Most frequent Base: {most_freq}\n")
    else:
        print(f"Error fetching {gene_name}: {response.status}")

    conn.close()