# Dictionary containing the gene names and their Ensembl stable identifiers
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

print("Dictionary of Genes!")
print(f"There are {len(genes)} genes in the dictionary:")
print()

for gene, gene_id in genes.items():
    print(f"{gene}: --> {gene_id}")