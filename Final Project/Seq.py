class Seq:
    def __init__(self, sequence_string):
        self.seq = sequence_string.upper().strip()

    def get_length(self):
        return len(self.seq)

    def get_percentage(self):
        """Calculates the percentage of A, T, C, G bases"""
        total = len(self.seq)
        if total == 0:
            return "A:0%, T:0%, C:0%, G:0%"

        a_pct = (self.seq.count('A') / total) * 100
        t_pct = (self.seq.count('T') / total) * 100
        c_pct = (self.seq.count('C') / total) * 100
        g_pct = (self.seq.count('G') / total) * 100

        return f"A: {a_pct:.1f}%, T: {t_pct:.1f}%, C: {c_pct:.1f}%, G: {g_pct:.1f}%"