from termcolor import colored
from e1 import Seq


def print_seqs(seq_list, color):
    for index, seq in enumerate(seq_list):
        text = f"Sequence {index}: (Length: {seq.len()}) {seq}"
        print(colored(text, color))


def generate_seqs(pattern, number):
    seq_list = []
    for i in range(1, number + 1):
        seq_list.append(Seq(pattern * i))
    return seq_list


# ---- Main program

seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

print(colored("List 1:", "blue"))
print_seqs(seq_list1, "blue")

print()
print(colored("List 2:", "green"))
print_seqs(seq_list2, "green")