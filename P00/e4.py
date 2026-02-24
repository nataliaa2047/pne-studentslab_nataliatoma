import Seq0

FOLDER = "sequences/"
GENES = ["U5", "ADA", "FRAT1", "FXN"]
BASES = ["A", "C", "T", "G"]

print("-----| Exercise 4 |-----")

for gene in GENES:
    FILENAME = FOLDER + gene + ".txt"
    sequence = Seq0.seq_read_fasta(FILENAME)
    print("Gene", gene + ":")
    for base in BASES:
        base_count = Seq0.seq_count_base(sequence, base)
        print("  ", base + ":", base_count)





