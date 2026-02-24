import Seq0

FOLDER = "sequences/"
GENES = ["U5", "ADA", "FRAT1", "FXN"]
BASES = ["A", "C", "T", "G"]

print("-----| Exercise 5 |-----")

for gene in GENES:
    FILENAME = FOLDER + gene + ".txt"
    sequence = Seq0.seq_read_fasta(FILENAME)
    base_count_dictionary = Seq0.seq_count(sequence)
    print("Gene", gene + ":", base_count_dictionary)