from pathlib import Path

def get_exons_from_file(FILENAME):
    file_contents = Path(FILENAME).read_text()
    lines = file_contents.split("\n")
    exons = []
    for line in lines:
        if not line.startswith(">"):
            exons.append(line)
    return exons



apoe_exons = get_exons_from_file("APOE_EXONS.txt")
print(apoe_exons)

