from Seq1 import Seq

print("-----| Practice 1, Exercise 9 |-----")

s = Seq()
s.read_fasta("sequences/U5.txt")

print(f"Sequence: (Length: {len(s)}) {s}")
print(f" Bases: {s.count()}")
print(f" Rev: {s.reverse()}")
print(f" Comp: {s.complement()}")