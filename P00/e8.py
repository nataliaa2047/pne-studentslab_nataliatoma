import Seq0

FOLDER = "sequences/"
GENES = ["U5", "ADA", "FRAT1", "FXN"]
BASES = ["A", "C", "T", "G"]

print("-----| Exercise 8 |-----")

for gene in GENES:
    FILENAME = FOLDER + gene + ".txt"
    sequence = Seq0.seq_read_fasta(FILENAME)
    base_count_dictionary = Seq0.seq_count(sequence)

    most_frequent_base = ""
    highest_count = -1
    for base in base_count_dictionary:
        if base_count_dictionary[base] > highest_count:
            highest_count = base_count_dictionary[base]
            most_frequent_base = base
    print("Gene", gene + ": Most frequent Base:", most_frequent_base)
