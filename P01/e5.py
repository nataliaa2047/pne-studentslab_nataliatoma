from Seq1 import Seq

print("-----| Practice 1, Exercise 5 |-----")

s0 = Seq()
s1 = Seq("ACTGA")
s2 = Seq("Invalid sequence")

sequences = [s0, s1, s2]

for i, seq in enumerate(sequences):
    print(f"Sequence {i}: (Length: {len(seq)}) {seq}")
    print(f" A: {seq.count_base("A")}, C: {seq.count_base("C")}, T: {seq.count_base("T")}, G: {seq.count_base("G")}")
