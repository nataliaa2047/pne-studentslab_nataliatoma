import Seq0

FOLDER = "sequences/"
GENE = "U5"

print("-----| Exercise 7 |-----")

FILENAME = FOLDER + GENE + ".txt"
sequence = Seq0.seq_read_fasta(FILENAME)
fragment = sequence[:20]

print("Gene", GENE + ":")
print("Fragment:", fragment)

complementary_seq = Seq0.seq_complement(fragment)
print("Complementary:", complementary_seq)