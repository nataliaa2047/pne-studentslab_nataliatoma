from pathlib import Path

FILENAME = "sequences/ADA.txt"

file_contents = Path(FILENAME).read_text()

body = file_contents.split("\n")[1:]

new_seq = "".join(body) #with this, we join the lines into a single string

total_number_bases = len(new_seq)

print("The total number of bases of the ADA.txt file is:", total_number_bases)




