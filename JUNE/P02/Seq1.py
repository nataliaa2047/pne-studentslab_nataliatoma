class Seq:
    def __init__(self, strbases=None):
        if strbases is None:
            print("NULL sequence created")
            self.strbases = ""
            return

        for base in strbases:
            if base not in "ATCG":
                print("INVALID sequence!")
                self.strbases = "ERROR"
                return

        self.strbases = strbases
        print("New sequence created!")

    def read_fasta(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        sequence = ""
        for line in lines:
            if line.startswith(">"):
                continue
            sequence += line.strip()
        self.strbases = sequence

    def __len__(self):
        if self.strbases == "" or self.strbases == "ERROR":
            return 0
        return len(self.strbases)

    def count_base(self, base):
        if self.strbases == "" or self.strbases == "ERROR":
            return 0
        return self.strbases.count(base)

    def count(self):
        if self.strbases == "" or self.strbases == "ERROR":
            return {"A": 0, "T": 0, "C": 0, "G": 0}
        return {
            "A": self.strbases.count("A"),
            "T": self.strbases.count("T"),
            "C": self.strbases.count("C"),
            "G": self.strbases.count("G"),
        }

    def reverse(self):
        if self.strbases == "" or self.strbases == "ERROR":
            return "ERROR"
        return self.strbases[::-1]

    def complement(self):
        if self.strbases == "" or self.strbases == "ERROR":
            return "ERROR"
        comp = ""
        for base in self.strbases:
            if base == "A":
                comp += "T"
            elif base == "T":
                comp += "A"
            elif base == "C":
                comp += "G"
            elif base == "G":
                comp += "C"
        return comp

    def __str__(self):
        if self.strbases == "":
            return "NULL"
        return self.strbases