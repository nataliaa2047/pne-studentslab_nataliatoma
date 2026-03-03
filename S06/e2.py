from e1 import Seq

def print_seqs(seq_list):
    for index, seq in enumerate(seq_list):
        print(f"Sequence {index}: (Length: {seq.len()}) {seq}")

seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]
print_seqs(seq_list)
