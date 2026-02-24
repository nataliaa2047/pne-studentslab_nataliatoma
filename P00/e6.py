import Seq0

FOLDER = "sequences/"
GENE = "U5"

print("-----| Exercise 6 |-----")

FILENAME = FOLDER + GENE + ".txt"
sequence = Seq0.seq_read_fasta(FILENAME)
fragment = sequence[:20]

print("Gene", GENE)
print("Fragment:", fragment)

reversed_seq = Seq0.seq_reverse(sequence, 20)
print("Reverse:", reversed_seq)