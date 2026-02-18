from pathlib import Path

FILENAME = "sequences/RNU6_269P.txt"

file_contents = Path(FILENAME).read_text()

header = file_contents.split("\n")[0]

print("First line of the RNU6_269P.txt file:")
print(header)

#.split("\n") --> splits the text every time there's a new line, turning the sequence into a list
#[0] --> we only take the first of the list (the header) --> that's why the output is not into a list
