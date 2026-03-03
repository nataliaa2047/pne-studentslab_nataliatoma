class Seq:
    """A class for representing sequences"""

    def __init__(self, strbases):
        valid_bases = {"A", "C", "G", "T"}
        # Initialize the sequence with the value
        # passed as argument when creating the object
        if all(base in valid_bases for base in strbases):
            self.strbases = strbases
            print("New sequence created!")
        else:
            self.strbases = "ERROR"
            print("INCORRECT Sequence detected")
            print("ERROR!")

    def __str__(self):
        """Method called when the object is being printed"""
        # -- We just return the string with the sequence
        return self.strbases

    def len(self):
        """Calculate the length of the sequence"""
        return len(self.strbases)

s1 = Seq("ACCTGC")
s2 = Seq("Hello? Am I a valid sequence?")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")


