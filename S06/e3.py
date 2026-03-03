from e1 import Seq
from e2 import print_seqs

def generate_seqs(pattern, number):
    seq_list = []

    for i in range(1, number + 1):
        new_sequence = pattern * i
        seq_obj = Seq(new_sequence)
        seq_list.append(seq_obj)

    return seq_list


# ---- Main program (for testing)

seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

print("List 1:")
print_seqs(seq_list1)

print()
print("List 2:")
print_seqs(seq_list2)