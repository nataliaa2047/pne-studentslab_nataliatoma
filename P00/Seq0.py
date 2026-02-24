from pathlib import Path

def seq_ping():
    print("OK")

def seq_read_fasta(FILENAME):
    file_contents = Path(FILENAME).read_text()
    body = file_contents.split("\n")[1:]
    sequence = "".join(body)  #we transform the list into a string
    return sequence

def seq_len(seq):
    count = 0
    for base in seq:
        count += 1
    return count

def seq_count_base(seq, base):
    count = seq.count(base)
    return count

def seq_count(seq):
    d = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
    for base in seq:
        if base in d:
            d[base] += 1
    return d

def seq_reverse(seq, n):
    fragment = seq[:n]
    return fragment[::-1]

def seq_complement(seq):
    complementary_bases = {"A": "T", "C": "G", "G": "C", "T": "A"}
    new_seq = ""
    for base in seq:
        new_seq += complementary_bases[base]
    return new_seq




