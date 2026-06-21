from Seq0 import *

print("-----| Exercise 4 |-----")

FILENAME_1 = "U5.txt"
FILENAME_2 = "ADA.txt"
FILENAME_3 = "FRAT1.txt"
FILENAME_4 = "FXN.txt"

FOLDER = "sequences/"

filename_1 = FOLDER + FILENAME_1
filename_2 = FOLDER + FILENAME_2
filename_3 = FOLDER + FILENAME_3
filename_4 = FOLDER + FILENAME_4

sequence_1 = seq_read_fasta(filename_1)
sequence_2 = seq_read_fasta(filename_2)
sequence_3 = seq_read_fasta(filename_3)
sequence_4 = seq_read_fasta(filename_4)

print("Gene U5:")
print("A:", seq_count_base(sequence_1, "A"))
print("C:", seq_count_base(sequence_1, "C"))
print("T:", seq_count_base(sequence_1, "T"))
print("G:", seq_count_base(sequence_1, "G"))
print("\n")
print("Gene ADA:")
print("A:", seq_count_base(sequence_2, "A"))
print("C:", seq_count_base(sequence_2, "C"))
print("T:", seq_count_base(sequence_2, "T"))
print("G:", seq_count_base(sequence_2, "G"))
print("\n")
print("Gene FRAT1:")
print("A:", seq_count_base(sequence_3, "A"))
print("C:", seq_count_base(sequence_3, "C"))
print("T:", seq_count_base(sequence_3, "T"))
print("G:", seq_count_base(sequence_3, "G"))
print("\n")
print("Gene FXN:")
print("A:", seq_count_base(sequence_4, "A"))
print("C:", seq_count_base(sequence_4, "C"))
print("T:", seq_count_base(sequence_4, "T"))
print("G:", seq_count_base(sequence_4, "G"))
print("\n")