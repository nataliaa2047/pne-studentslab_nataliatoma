import http.server
import socketserver
import termcolor

# Define the Server's port
PORT = 8081

# Prevent "Address already in use"
socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle GET requests"""

        # Print request line
        termcolor.cprint(self.requestline, 'green')

        # Decide which file to serve
        if self.path in ["/", "/index.html"]:
            filepath = "index.html"
            status_code = 200
        else:
            filepath = "error.html"
            status_code = 404

        try:
            with open(filepath, "rb") as f:
                content = f.read()

                self.send_response(status_code)
                self.send_header('Content-Type', 'text/html')  # FIXED
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()

                self.wfile.write(content)

        except FileNotFoundError:
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