from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check if the client is asking for '/listusers'
        if self.path == '/listusers':
            # 1. Read the JSON file
            with open('S18/people-e1.json', 'r') as f:
                data = json.load(f)

            # 2. Send the HTTP response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # 3. Write the data to the response body
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")


# Start the server on localhost, port 8000
server = HTTPServer(('localhost', 8000), RequestHandler)
print("Server running on port 8000. Press Ctrl+C to stop.")
server.serve_forever()