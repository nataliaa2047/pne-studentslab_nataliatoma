class Seq:
    def __init__(self, strbases):
        self.strbases = strbases
        bases = "ACGT"
        valid = True
        for i in strbases:
            if i not in bases:
                valid = False
        if valid:
            print("New sequence created!")
        else:
            print("ERROR!!")

    def __str__(self):
        bases = "ACGT"
        for i in self.strbases:
            if i not in bases:
                return "ERROR"
        return self.strbases


# --- Main program
s1 = Seq("ACCTGC")
s2 = Seq("ACXTGC")

print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")