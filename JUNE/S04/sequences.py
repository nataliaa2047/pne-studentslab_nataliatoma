from pathlib import Path

FILENAME = "sequences/ADA.txt"

file_contents = Path(FILENAME).read_text()

body = file_contents.split("\n")[1:]

def body_counter(b):
    total_count = 0
    for line in b:
        count = 0
        for base in line:
            count += 1
        total_count += count
    return total_count

print(f"Total number of bases of the ADA sequence: {body_counter(body)}")