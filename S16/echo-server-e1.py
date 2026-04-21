from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2 as j


def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    return j.Template(contents)


class EchoServer(BaseHTTPRequestHandler):

    def do_GET(self):
        url_path = urlparse(self.path)
        path = url_path.path
        arguments = parse_qs(url_path.query)

        # MAIN PAGE → show form
        if path == "/":
            html = read_html_file("form-e1.html").render()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        # ECHO PAGE
        elif path == "/echo":
            text = arguments.get("message", [""])[0]

            # ✅ Exercise 2: checkbox logic
            if "caps" in arguments:
                text = text.upper()

            html = f"""
            <html>
            <body>
                <h1>Echo Server</h1>
                <p>{text}</p>
                <a href="/">Back</a>
            </body>
            </html>
            """

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        # ERROR PAGE
        else:
            html = read_html_file("error.html").render()
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())


# RUN SERVER
server = HTTPServer(("localhost", 8080), EchoServer)
print("Server running at http://localhost:8080")
server.serve_forever()