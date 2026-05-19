import http.server
import socketserver
import termcolor
from pathlib import Path
import json
import socket
from Seq import Seq

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True


# -----------------------------------------------------------------
# INTERNET CONNECTION LAYER (Raw sockets to touch rest.ensembl.org)
# -----------------------------------------------------------------
def get_ensembl_data(endpoint):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("rest.ensembl.org", 80))

        request = (
            f"GET {endpoint} HTTP/1.1\r\n"
            f"Host: rest.ensembl.org\r\n"
            f"Accept: application/json\r\n"
            f"Connection: close\r\n\r\n"
        )
        s.sendall(request.encode("utf-8"))

        buffer = []
        while True:
            chunk = s.recv(4096)
            if not chunk:
                s.close()
                full_bytes = b"".join(buffer)
                body = full_bytes.split(b"\r\n\r\n", 1)[1]
                return json.loads(body.decode("utf-8"))
            buffer.append(chunk)
    except Exception:
        return None


class GenomeRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """Processes target path parameters and switches to REST handling rules"""
        termcolor.cprint(self.requestline, 'green')

        # Advanced Tier check: is client demanding JSON raw payload responses?
        is_json_format = False
        if "json=1" in self.path:
            is_json_format = True

        # --- HOME MENU ENDPOINT ---
        if self.path == "/" or self.path == "/?json=1":
            if is_json_format:
                self.send_json_response(200, {"status": "running", "msg": "Genome API Server active"})
                return

            filepath = Path("index.html")
            try:
                with filepath.open("rb") as f:
                    content = f.read()
                    self.send_html_response(200, content)
            except FileNotFoundError:
                self.serve_error_file(is_json_format)

        # --- BASIC ENDPOINTS ---
        elif self.path.startswith("/listSpecies"):
            limit_val = ""
            if "limit=" in self.path:
                # Basic string isolate manipulation to extract values safely
                raw_part = self.path.split("limit=")[1]
                limit_val = raw_part.split("&")[0]
            self.handle_list_species(limit_val, is_json_format)

        elif self.path.startswith("/karyotype"):
            species_val = ""
            if "species=" in self.path:
                raw_part = self.path.split("species=")[1]
                species_val = raw_part.split("&")[0].strip().lower()
            self.handle_karyotype(species_val, is_json_format)

        elif self.path.startswith("/chromosomeLength"):
            if "species=" in self.path and "chromo=" in self.path:
                species_val = self.path.split("species=")[1].split("&")[0].strip().lower()
                chromo_val = self.path.split("chromo=")[1].split("&")[0].strip().lower()
                self.handle_chromosome_length(species_val, chromo_val, is_json_format)
            else:
                self.serve_error_file(is_json_format)

        # --- MEDIUM ENDPOINTS ---
        elif self.path.startswith("/geneLookup"):
            gene_name = ""
            if "gene=" in self.path:
                gene_name = self.path.split("gene=")[1].split("&")[0].strip()
            self.handle_gene_lookup(gene_name, is_json_format)

        elif self.path.startswith("/geneSeq"):
            gene_name = ""
            if "gene=" in self.path:
                gene_name = self.path.split("gene=")[1].split("&")[0].strip()
            self.handle_gene_seq(gene_name, is_json_format)

        elif self.path.startswith("/geneInfo"):
            gene_name = ""
            if "gene=" in self.path:
                gene_name = self.path.split("gene=")[1].split("&")[0].strip()
            self.handle_gene_info(gene_name, is_json_format)

        elif self.path.startswith("/geneCalc"):
            gene_name = ""
            if "gene=" in self.path:
                gene_name = self.path.split("gene=")[1].split("&")[0].strip()
            self.handle_gene_calc(gene_name, is_json_format)

        elif self.path.startswith("/geneList"):
            if "chromo=" in self.path and "start=" in self.path and "end=" in self.path:
                chromo_val = self.path.split("chromo=")[1].split("&")[0].strip()
                start_val = self.path.split("start=")[1].split("&")[0].strip()
                end_val = self.path.split("end=")[1].split("&")[0].strip()
                self.handle_gene_list(chromo_val, start_val, end_val, is_json_format)
            else:
                self.serve_error_file(is_json_format)

        else:
            self.serve_error_file(is_json_format)

    # -------------------------------------------------------------
    # HANDLING EXECUTION BLOCKS
    # -------------------------------------------------------------

    def handle_list_species(self, limit_val, is_json):
        data = get_ensembl_data("/info/species")
        if data is None or "species" not in data:
            self.serve_error_file(is_json)
            return

        species_list = data.get("species", [])
        limit = len(species_list)
        if limit_val.isdigit():
            limit = int(limit_val)

        final_species = []
        for i in range(min(limit, len(species_list))):
            name = species_list[i].get("display_name", "Unknown Species")
            final_species.append(name)

        if is_json:
            self.send_json_response(200, {"species_list": final_species})
            return

        html = "<html><body><h1>Database Species List</h1><ul>"
        for item in final_species:
            html += f"<li>{item}</li>"
        html += "</ul><br><a href='/'>Go to main page</a></body></html>"
        self.send_html_response(200, html.encode("utf-8"))

    def handle_karyotype(self, species, is_json):
        data = get_ensembl_data(f"/info/assembly_info/{species}")
        if data is None or "karyotype" not in data:
            self.serve_error_file(is_json)
            return

        karyotype = data.get("karyotype", [])
        if is_json:
            self.send_json_response(200, {"species": species, "karyotype": karyotype})
            return

        html = f"<html><body><h1>Karyotype for {species}</h1><ul>"
        for chromosome in karyotype:
            html += f"<li>Chromosome {chromosome}</li>"
        html += "</ul><br><a href='/'>Go to main page</a></body></html>"
        self.send_html_response(200, html.encode("utf-8"))

    def handle_chromosome_length(self, species, chromo, is_json):
        data = get_ensembl_data(f"/info/assembly_info/{species}")
        if data is None or "top_level_region" not in data:
            self.serve_error_file(is_json)
            return

        regions = data.get("top_level_region", [])
        for r in regions:
            if str(r.get("name")).lower() == chromo:
                length = r.get("length")

                if is_json:
                    self.send_json_response(200, {"species": species, "chromosome": chromo, "length": length})
                    return

                html = f"""<html><body>
                    <h1>Chromosome Specification</h1>
                    <p><strong>Species:</strong> {species}</p>
                    <p><strong>Chromosome:</strong> {chromo}</p>
                    <p><strong>Total Length:</strong> {length} bp</p>
                    <br><a href='/'>Go to main page</a>
                </body></html>"""
                self.send_html_response(200, html.encode("utf-8"))
                return
        self.serve_error_file(is_json)

    def handle_gene_lookup(self, gene_name, is_json):
        data = get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene_name}")
        if data is None or "id" not in data:
            self.serve_error_file(is_json)
            return

        gene_id = data.get("id")
        if is_json:
            self.send_json_response(200, {"gene": gene_name, "stable_id": gene_id})
            return

        html = f"""<html><body>
            <h1>Gene Lookup</h1>
            <p><strong>Gene Name:</strong> {gene_name}</p>
            <p><strong>Stable ID:</strong> {gene_id}</p>
            <br><a href='/'>Go to main page</a>
        </body></html>"""
        self.send_html_response(200, html.encode("utf-8"))

    def handle_gene_seq(self, gene_name, is_json):
        lookup_data = get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene_name}")
        if lookup_data is None or "id" not in lookup_data:
            self.serve_error_file(is_json)
            return

        gene_id = lookup_data.get("id")
        seq_data = get_ensembl_data(f"/sequence/id/{gene_id}")
        if seq_data is None or "seq" not in seq_data:
            self.serve_error_file(is_json)
            return

        raw_sequence = seq_data.get("seq")
        if is_json:
            self.send_json_response(200, {"gene": gene_name, "stable_id": gene_id, "sequence": raw_sequence})
            return

        html = f"""<html><body>
            <h1>Gene Sequence</h1>
            <p><strong>Gene:</strong> {gene_name} ({gene_id})</p>
            <textarea rows='10' cols='60' readonly>{raw_sequence}</textarea>
            <br><br><a href='/'>Go to main page</a>
        </body></html>"""
        self.send_html_response(200, html.encode("utf-8"))

    def handle_gene_info(self, gene_name, is_json):
        data = get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene_name}")
        if data is None or "id" not in data:
            self.serve_error_file(is_json)
            return

        g_id = data.get("id")
        start = data.get("start")
        end = data.get("end")
        chromo = data.get("seq_region_name")
        length = int(end) - int(start) + 1

        if is_json:
            self.send_json_response(200, {
                "id": g_id, "chromosome": chromo, "start": start, "end": end, "length_bp": length
            })
            return

        html = f"""<html><body>
            <h1>Gene Information</h1>
            <p><strong>ID:</strong> {g_id}</p>
            <p><strong>Chromosome:</strong> Chromosome {chromo}</p>
            <p><strong>Start Position:</strong> {start}</p>
            <p><strong>End Position:</strong> {end}</p>
            <p><strong>Calculated Length:</strong> {length} bp</p>
            <br><a href='/'>Go to main page</a>
        </body></html>"""
        self.send_html_response(200, html.encode("utf-8"))

    def handle_gene_calc(self, gene_name, is_json):
        lookup_data = get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene_name}")
        if lookup_data is None or "id" not in lookup_data:
            self.serve_error_file(is_json)
            return

        gene_id = lookup_data.get("id")
        seq_data = get_ensembl_data(f"/sequence/id/{gene_id}")
        if seq_data is None or "seq" not in seq_data:
            self.serve_error_file(is_json)
            return

        my_sequence_obj = Seq(seq_data.get("seq"))
        length = my_sequence_obj.get_length()
        percentages = my_sequence_obj.get_percentage()

        if is_json:
            self.send_json_response(200, {"gene": gene_name, "length": length, "distribution": percentages})
            return

        html = f"""<html><body>
            <h1>Gene Analysis (Calculations)</h1>
            <p><strong>Gene:</strong> {gene_name}</p>
            <p><strong>Total Length:</strong> {length} bases</p>
            <p><strong>Base Distribution percentages:</strong> {percentages}</p>
            <br><a href='/'>Go to main page</a>
        </body></html>"""
        self.send_html_response(200, html.encode("utf-8"))

    def handle_gene_list(self, chromo, start, end, is_json):
        data = get_ensembl_data(f"/overlap/region/homo_sapiens/{chromo}:{start}-{end}?feature=gene")
        if data is None or type(data) is not list:
            self.serve_error_file(is_json)
            return

        gene_names_found = []
        for entry in data:
            if "external_name" in entry:
                gene_names_found.append(entry.get("external_name"))

        if is_json:
            self.send_json_response(200, {"region": f"{chromo}:{start}-{end}", "genes": gene_names_found})
            return

        html = f"<html><body><h1>Overlapping Genes inside Region {chromo}:{start}-{end}</h1><ul>"
        for name in gene_names_found:
            html += f"<li>{name}</li>"
        html += "</ul><br><a href='/'>Go to main page</a></body></html>"
        self.send_html_response(200, html.encode("utf-8"))

    # -------------------------------------------------------------
    # WRITER UTILS
    # -------------------------------------------------------------

    def send_html_response(self, status_code, content_bytes):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(content_bytes)))
        self.end_headers()
        self.wfile.write(content_bytes)

    def send_json_response(self, status_code, data_dict):
        """Sends clean formatted JSON responses back to the programmatic caller"""
        json_string = json.dumps(data_dict, indent=4)
        json_bytes = json_string.encode("utf-8")

        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(json_bytes)))
        self.end_headers()
        self.wfile.write(json_bytes)

    def serve_error_file(self, is_json):
        if is_json:
            self.send_json_response(404, {"error": "Resource not found or database record entry completely missing."})
            return

        try:
            with Path("error.html").open("rb") as f:
                content = f.read()
                self.send_html_response(404, content)
        except FileNotFoundError:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Server error: missing error html resource canvas layout.")


# ------------------------
# INIT SERVER PROGRAM
# ------------------------
Handler = GenomeRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("REST API Serving active at PORT", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nProcess halted by user interaction sequence.")
        httpd.server_close()