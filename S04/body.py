from pathlib import Path

FILENAME = "sequences/U5.txt"

file_contents = Path(FILENAME).read_text()

body = file_contents.split("\n")[1:]

print("Body of the U5.txt file:")

for line in body:    #with this loop we process every element on the list individually
    print(line)

