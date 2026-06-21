from pathlib import Path

def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    file_contents = Path(filename).read_text()
    lines = file_contents.splitlines()
    sequence = "".join(lines[1:])
    return sequence

def seq_len(seq):
    return len(seq)

def seq_count_base(seq, base):
    count = 0
    for i in seq:
        if base == i:
            count += 1
    return count

def seq_count(seq):
    d = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
    for i in seq:
        d[i] += 1
    return d

def seq_reverse(seq, n):
    my_seq = seq[:n+1]
    print(f"Fragment: {my_seq}")
    reversed = my_seq[::-1]
    return reversed

def seq_complement(seq):
    comp = ""
    for i in seq:
        if i == 'A':
            comp += 'T'
        if i == 'T':
            comp += 'A'
        if i == 'C':
            comp += 'G'
        if i == 'G':
            comp += 'C'
    return comp

def most_frequent(seq):
    most_freq = None
    for i in seq:
        if most_freq is None or i > most_freq:
            most_freq = i
    return most_freq





