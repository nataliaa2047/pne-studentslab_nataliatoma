from len_methods import Seq

seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]

def print_seqs(seq_list):
    for i, seq in enumerate(seq_list):
        print(f"Sequence {i}: (Length: {seq.len()}) {seq}")

print_seqs(seq_list)

