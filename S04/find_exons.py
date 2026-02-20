from pathlib import Path

ada_filename = "sequences/ADA.txt"
ada_file_contents = Path(ada_filename).read_text()  #this opens the file where the complete gene is
ada_lines = ada_file_contents.split("\n")    #splits the text every time there's a new line, turning the sequence into a list
ada_header = ada_lines[0]    #selects only the line of the header
ada_body = "".join(ada_lines[1:])   #we join the lines (not including the header) into a single string

ada_header_parts = ada_header.split(":")  #splits the text every time there's a ':', turning the header into a list
lower_boundary = int(ada_header_parts[4])  #we select the lower boundary from the header
upper_boundary = int(ada_header_parts[5])  #we select the upper boundary from the header
strand = ada_header_parts[6]   #we select the negative strand (-1)
max_coordinate = upper_boundary  #the first base of the file is the biggest number

exons_filename = "ADA_EXONS.txt"
exons_file_contents = Path(exons_filename).read_text()   #this opens the file where the exons of the gene are
exons_lines = exons_file_contents.split("\n")   #splits the text every time there's a new line, turning the sequence into a list
exons = []   #we crate a new list that's empty
for line in exons_lines:   #we go through every line
    if not line.startswith(">"):
        exons.append(line)   #we put into the list only those lines that don't start with ">", which are the real sequences

print("Exon | Long | Start | End")
print("-----------------------------")

exon_number = 1
for exon in exons:  #we go through every exon
    long = len(exon)   #we calculate the length (how many bases does it have) of every exon
    index = ada_body.find(exon)   #it searches that sequence inside of the complete gene (ada); then, it returns the position where it starts
    start = max_coordinate - index  #it's a negaive strand, so, if we go forward through the string, the chromosomal coordinate will decrease. Therefore, real_coordinate = max_coordinate - position_in_the_string
    end = start - long + 1  #the coordinate goes backwards. that's why we substract the length. We sum 1 to adjust it
    print(exon_number, "|", long, "|", start, "|", end)
    exon_number += 1   #we have to do it with all the exons, so we pass to the next one

#Lo que pide el enunciado es que encuentre dónde está cada exón del gen completo y convertir su posición en coordenadas reales del cromosoma 20.
#Para resolverlo, he pasado de una posición dentro de un string a una posición real dentro del cromosoma humano.











