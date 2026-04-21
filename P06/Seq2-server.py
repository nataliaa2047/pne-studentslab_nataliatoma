import http.server
import socketserver
import urllib.parse
import os


# --- Seq Class ---
class Seq:
    def __init__(self, str_seq=""):
        self.str_seq = str_seq.upper()  # Standardize to uppercase

    def get_info(self):
        length = len(self.str_seq)
        if length == 0: return "Empty sequence"
        res = f"Sequence: {self.str_seq}\nTotal length: {length}\n"
        for base in ['A', 'C', 'G', 'T']:
            count = self.str_seq.count(base)
            perc = (count / length) * 100
            res += f"{base}: {count} ({perc:.1f}%)\n"
        return res

    def get_complement(self):
        table = str.maketrans("ATCG", "TAGC")
        return self.str_seq.translate(table)

    def get_reverse(self):
        return self.str_seq[::-1]

    def read_from_file(self, gene_name):
        filename = f"sequences/{gene_name}.txt"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                content = f.read().strip()
                lines = content.split("\n")[1:]
                self.str_seq = "".join(lines).replace(" ", "")
            return True
        return False


# --- Data ---
GENE_LIST = [
    "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA",
    "CCCTAGCCTGACTCCCTTTCCCTTTCCATCCTCACCAGACGCCCGGCATGCCGGACCTCAAA",
    "CAAGGTCCCCTTCTTCCTTTCCATTCCCGTCAGCTTCATTTCCTAATCTCCGTACAAAT",
    "GATTACA_SEQ_3",
    "TTAGGG_SEQ_4"
]


# --- Server Handler ---
class SeqRequestHandler(http.server.BaseHTTPRequestHandler):

    def serve_file(self, filename, status=200, replacements=None):
        path = os.path.join("html", filename)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            if replacements:
                for key, value in replacements.items():
                    content = content.replace(f"{{{{{key}}}}}", str(value))
            self.send_response(status)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        else:
            self.send_error(404, "File not found")

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        # 1. Main Page
        if path == "/" or path == "/index.html":
            self.serve_file("index.html")

        # 2. PING
        elif path == "/ping":
            self.serve_file("ping.html")

        # 3. GET
        elif path == "/get" and "n" in query:
            idx = int(query["n"][0])
            if 0 <= idx < len(GENE_LIST):
                self.serve_file("get.html", replacements={"N": idx, "SEQUENCE": GENE_LIST[idx]})
            else:
                self.serve_file("error.html", status=404)

        # 4. GENE
        elif path == "/gene" and "name" in query:
            gene_name = query["name"][0]
            s = Seq()
            if s.read_from_file(gene_name):
                self.serve_file("gene.html", replacements={"NAME": gene_name, "GENE": s.str_seq})
            else:
                self.serve_file("error.html", status=404)

        # 5. OPERATION (Exercise 4)
        elif path == "/operation" and "seq" in query and "op" in query:
            seq_val = query["seq"][0]
            op_val = query["op"][0]
            s = Seq(seq_val)

            result = ""
            if op_val == "info":
                result = s.get_info()
            elif op_val == "comp":
                result = s.get_complement()
            elif op_val == "rev":
                result = s.get_reverse()

            self.serve_file("operation.html", replacements={"RESULT": result})

        else:
            self.serve_file("error.html", status=404)


# --- Start Server ---
def start_server(port=8080):
    for folder in ["html", "sequences"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    with socketserver.TCPServer(("", port), SeqRequestHandler) as httpd:
        print(f"Server running at http://localhost:{port}")
        httpd.serve_forever()


if __name__ == '__main__':
    start_server()