import http.server
import socketserver
import termcolor
from pathlib import Path
import json
import socket
from Seq import Seq

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True      #The "allow_reuse_address = True" setting allows us to restart the script immediately without the operating system blocking the port


def get_ensembl_data(endpoint):       #Its goal is to contact the official Ensembl Genome Database REST API server and return raw data
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #It establishes a network socket
        s.connect(("rest.ensembl.org", 80))     #the socket is directly connected to the IP address of rest.ensembl.org with port 80

        request = (
            f"GET {endpoint} HTTP/1.1\r\n"   #it asks for a specific endpoint
            f"Host: rest.ensembl.org\r\n"        
            f"Accept: application/json\r\n"    #it wants the database to return raw data data maps instead of a webpage
            f"Connection: close\r\n\r\n"
        )
        s.sendall(request.encode("utf-8"))

        buffer = []
        while True:
            chunk = s.recv(4096)
            if not chunk:    #when transmission stops, the socket closes
                s.close()
                full_bytes = b"".join(buffer)
                body = full_bytes.split(b"\r\n\r\n", 1)[1]    #separates the HTTP header headers from the actual data package
                return json.loads(body.decode("utf-8"))    #json.loads() converts that raw data string into a live Python dictionary object
            buffer.append(chunk)
    except Exception:
        return None      #If any network crash happens, it falls into the except block and returns None

class GenomeRequestHandler(http.server.BaseHTTPRequestHandler):     #This class evaluates what a user typed in their browser, directing them to the correct execution block
    def do_GET(self):               #Every time a user requests a URL from this server, this do_GET method automatically runs
        termcolor.cprint(self.requestline, 'green')

        is_json_format = False
        if "json=1" in self.path:
            is_json_format = True

        if self.path == "/" or self.path == "/?json=1":    #If the user requests the root homepage (/),...
            if is_json_format:                                    # and they want JSON,...
                self.send_json_response(200, {"status": "running", "msg": "Genome API Server active"})       #it sends back a raw code confirmation dictionary
                return

            filepath = Path("index.html")        #if the homepage is requested but we do not specify the JSON format, the server opens the file index.html
            try:
                with filepath.open("rb") as f:
                    content = f.read()
                    self.send_html_response(200, content)

            except FileNotFoundError:          #however, if the index.html is missing, its runs a custom error-handling method called serve_error_file
                self.serve_error_file(
                    is_json_format,
                    title="Missing Homepage",
                    message="The index.html file is missing from the server root directory."
                )

        elif self.path.startswith("/listSpecies"):
            limit_val = ""
            if "limit=" in self.path:
                raw_part = self.path.split("limit=")[1]     #the code string-splits the text to extract whatever number the user typed into the limit box on the index
                limit_val = raw_part.split("&")[0]
            self.handle_list_species(limit_val, is_json_format)

        elif self.path.startswith("/karyotype"):      #If the path is /karyotype, it extracts the species parameter from the URL, validates that it isn't empty, and forwards it to handle_karyotype()
            species_val = ""
            if "species=" in self.path:
                raw_part = self.path.split("species=")[1]
                species_val = raw_part.split("&")[0].strip().lower()
            if not species_val:
                self.serve_error_file(is_json_format, title="Missing Parameter",
                                      message="Please provide a ?species= parameter.")
            else:
                self.handle_karyotype(species_val, is_json_format)

        elif self.path.startswith("/chromosomeLength"):       #If the path is /chromosomeLength, it parses out two separate parameters: the target species and the specific target chromosome
            if "species=" in self.path and "chromo=" in self.path:
                species_val = self.path.split("species=")[1].split("&")[0].strip().lower()
                chromo_val = self.path.split("chromo=")[1].split("&")[0].strip().lower()
                self.handle_chromosome_length(species_val, chromo_val, is_json_format)     #It sends both variables to handle_chromosome_length()
                    #The code repeats this exact pattern for /geneLookup, /geneSeq, /geneInfo, /geneCalc, and /geneList. In each block, it isolates the parameters from the URL string and calls their respective execution handlers.

            else:
                self.serve_error_file(
                    is_json_format,
                    title="Invalid Parameters",
                    message="Chromosome length requests require both 'species' and 'chromo' parameters."
                )

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
                self.serve_error_file(
                    is_json_format,
                    title="Invalid Parameters",
                    message="Region search requires 'chromo', 'start', and 'end' parameters."
                )

        else:  #If a URL doesn't match any known endpoints, it activates the serve_error_file() routine to generate a standard HTTP 404 Not Found status response
            self.serve_error_file(
                is_json_format,
                title="404 Page Not Found",
                message=f"The requested path '{self.path}' does not exist on this server."
            )

    def handle_list_species(self, limit_val, is_json):       #it calls the external function to fetch a full JSON list of every species in the Ensembl database
        data = get_ensembl_data("/info/species")

        if data is None or "species" not in data:     #If the external server returns empty or invalid data, it stops immediately and serves an error.
            self.serve_error_file(is_json, title="Ensembl Error",
                                  message="Failed to retrieve species list from Ensembl database.")
            return

        species_list = data.get("species", [])
        limit = len(species_list)
        if limit_val.isdigit():    #t checks if the limit_val string isolated from the URL is a real digit
            limit = int(limit_val)

        final_species = []
        for i in range(min(limit, len(species_list))):      #Runs a loop that iterates up to the limit specified
            name = species_list[i].get("display_name", "Unknown Species")     #It pulls out the specific data point key "display_name" for each animal and pushes it into a list named final_species
            final_species.append(name)

        if is_json:       #we make sure that the request flag was set to JSON format
            self.send_json_response(200, {"species_list": final_species})         #if so, it encodes our previous list into JSON text format and finishes
            return

        html = "<html><body><h1>Database Species List</h1><ul>"
        for item in final_species:
            html += f"<li>{item}</li>"        #it builds a raw string of HTML elements by looping through the names and enclosing them inside <li> (List Item) markup tags
        html += "</ul><br><a href='/'>Go to main page</a></body></html>"
        self.send_html_response(200, html.encode("utf-8"))

    def handle_karyotype(self, species, is_json):
        data = get_ensembl_data(f"/info/assembly/{species}")
        if data is None or "karyotype" not in data:
            self.serve_error_file(is_json, title="Species Not Found",
                                  message=f"Could not find karyotype data for species: '{species}'.")
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
        data = get_ensembl_data(f"/info/assembly/{species}")
        if data is None or "top_level_region" not in data:
            self.serve_error_file(is_json, title="Data Error", message=f"Could not fetch data for species '{species}'.")
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

        self.serve_error_file(is_json, title="Chromosome Not Found",
                              message=f"Chromosome '{chromo}' not found for species '{species}'.")

    def handle_gene_lookup(self, gene_name, is_json):
        data = get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene_name}")
        if data is None or "id" not in data:
            self.serve_error_file(is_json, title="Gene Not Found",
                                  message=f"The gene symbol '{gene_name}' could not be found.")
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

    def handle_gene_seq(self, gene_name, is_json):       #It looks up the gene metadata to get its tracking ID, then fetches the raw DNA text string for that gene from the Ensembl database
        lookup_data = get_ensembl_data(f"/lookup/symbol/homo_sapiens/{gene_name}")
        if lookup_data is None or "id" not in lookup_data:
            self.serve_error_file(is_json, title="Gene Not Found",
                                  message=f"Cannot look up sequence because gene '{gene_name}' does not exist.")
            return

        gene_id = lookup_data.get("id")
        seq_data = get_ensembl_data(f"/sequence/id/{gene_id}")
        if seq_data is None or "seq" not in seq_data:
            self.serve_error_file(is_json, title="Sequence Missing",
                                  message=f"Failed to extract base sequence pairs for ID {gene_id}.")
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
            self.serve_error_file(is_json, title="Gene Not Found",
                                  message=f"No information available for gene '{gene_name}'.")
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
            self.serve_error_file(is_json, title="Gene Not Found",
                                  message=f"Cannot run analytics on missing gene '{gene_name}'.")
            return

        gene_id = lookup_data.get("id")
        seq_data = get_ensembl_data(f"/sequence/id/{gene_id}")
        if seq_data is None or "seq" not in seq_data:
            self.serve_error_file(is_json, title="Sequence Error",
                                  message="Could not read sequence to process calculations.")
            return

        my_sequence_obj = Seq(seq_data.get("seq"))            # It passes the raw sequence string fetched from Ensembl into Seq class. This instantiates a specific object instance named my_sequence_obj
        length = my_sequence_obj.get_length()          #It executes the method call .get_length() belonging to a specific object instance, and stores the calculated output into a local method variable
        percentages = my_sequence_obj.get_percentage()        ##It executes the method call .get_percentage() belonging to a specific object instance, and stores the calculated output into a local method variable

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
            self.serve_error_file(is_json, title="Region Error",
                                  message="Failed to extract mapping data for the requested coordinates.")
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

    def send_html_response(self, status_code, content_bytes):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(content_bytes)))
        self.end_headers()
        self.wfile.write(content_bytes)

    def send_json_response(self, status_code, data_dict):     #formats the text data payload specifically as application/json data structure types.
        json_string = json.dumps(data_dict, indent=4)
        json_bytes = json_string.encode("utf-8")
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(json_bytes)))
        self.end_headers()
        self.wfile.write(json_bytes)

    def serve_error_file(self, is_json, title="Error", message="An unexpected error occurred."):
        if is_json:                      #If an error occurs and the caller demands a JSON format, it bypasses the template engine entirely and returns a structured error data object map
            self.send_json_response(404, {"error": title, "details": message})
            return

        try:
            with Path("error.html").open("r", encoding="utf-8") as f:     #it opens error.html file
                template = f.read()
            formatted_html = template.format(title=title, message=message)     #overwrites the {title} and {message} in the error.html file
            self.send_html_response(404, formatted_html.encode("utf-8"))

        except FileNotFoundError:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Server error: missing error html resource canvas layout.")


Handler = GenomeRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("REST API Serving active at PORT", PORT)
    try:
        httpd.serve_forever()       #.serve_forever() places the script into an infinite loop, constantly listening for network connections on port 8080
    except KeyboardInterrupt:
        print("\nProcess halted by user interaction sequence.")
        httpd.server_close()