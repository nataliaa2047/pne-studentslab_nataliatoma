from Seq1 import Seq

FOLDER = "sequences/"
GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

print("-----| Practice 1, Exercise 10 |-----")

for gene in GENES:
    s = Seq()
    s.read_fasta(FOLDER + gene + ".txt")
    base_count_dictionary = s.count()

    most_frequent_base = ""
    highest_count = -1
    for base in base_count_dictionary:
        if base_count_dictionary[base] > highest_count:
            highest_count = base_count_dictionary[base]
            most_frequent_base = base
    print("Gene", gene + ": Most frequent Base:", most_frequent_base)
