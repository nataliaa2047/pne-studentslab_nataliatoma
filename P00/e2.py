import Seq0

FOLDER = "sequences/"
FILENAME = "U5.txt"
print("DNA file:", FILENAME)

COMPLETE_FILENAME = FOLDER + FILENAME
sequence = Seq0.seq_read_fasta(COMPLETE_FILENAME)

print("The first 20 bases are:")
print(sequence[:20])





