from pathlib import Path

def seq_ping():
    print("OK")

def seq_read_fasta(FILENAME):
    file_contents = Path(FILENAME).read_text()
    body = file_contents.split("\n")[1:]
    sequence = "".join(body)  #we transform the list into a string
    return sequence
