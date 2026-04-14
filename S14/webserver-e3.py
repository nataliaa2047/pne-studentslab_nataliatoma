import http.server
import socketserver
import termcolor
from pathlib import Path

# Define the Server's port
PORT = 8081

# Prevent "Address already in use"
socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle GET requests"""

        # Print request line
        termcolor.cprint(self.requestline, 'green')

        # Get requested file
        filename = self.path.lstrip("/")
        if filename == "":
            filename = "index.html"

        filepath = Path(filename)

        try:
            # Try to open requested file
            with filepath.open("rb") as f:
                content = f.read()

                self.send_response(200)
                self.send_header('Content-Type', 'text/html')  # FIXED
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()

                self.wfile.write(content)

        except FileNotFoundError:
            try:
                # If file not found → send error.html
                with Path("error.html").open("rb") as f:
                    content = f.read()

                    self.send_response(404)
                    self.send_header('Content-Type', 'text/html')  # FIXED
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()

                    self.wfile.write(content)

            except FileNotFoundError:
                # If even error.html is missing
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Server error: required HTML file not found.")


# ------------------------
# Server MAIN program
# ------------------------

Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()