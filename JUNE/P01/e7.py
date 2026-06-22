from Seq1 import Seq

print("-----| Practice 1, Exercise 7 |-----")

s1 = Seq()
s2 = Seq("ACTGA")
s3 = Seq("Invalid sequence")

sequences = [s1, s2, s3]

for i, seq in enumerate(sequences):
    print(f"Sequence {i}: (Length: {len(seq)}) {seq}")
    print(f" Bases: {seq.count()}")
    print(f" Rev: {seq.reverse()}")