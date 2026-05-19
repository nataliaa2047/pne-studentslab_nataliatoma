import socket
import json


def test_api_endpoint(path_query):
    """Sends a programmatic request to our local server and prints the JSON content payload"""
    print(f"\n[CLIENT] Requesting raw target data string: http://localhost:8080{path_query}")
    try:
        # Connect strictly to your local running python server port
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect(("127.0.0.1", 8080))

        # Build standard text protocol delivery format
        http_req = (
            f"GET {path_query} HTTP/1.1\r\n"
            f"Host: localhost:8080\r\n"
            f"Connection: close\r\n\r\n"
        )
        c.sendall(http_req.encode("utf-8"))

        # Assemble incoming raw socket data streams
        stream_chunks = []
        while True:
            chunk = c.recv(4096)
            if not chunk:
                break
            stream_chunks.append(chunk)
        c.close()

        full_payload = b"".join(stream_chunks)

        # Isolate body out from the response headers structure
        if b"\r\n\r\n" in full_payload:
            body_bytes = full_payload.split(b"\r\n\r\n", 1)[1]
            body_string = body_bytes.decode("utf-8")

            # Print parsed object map cleanly onto screen
            parsed_json = json.loads(body_string)
            print(json.dumps(parsed_json, indent=2))
        else:
            print("[CLIENT ERROR] Received invalid data transmission envelope framework.")

    except Exception as err:
        print(f"[CLIENT CONNECTION FAILURE] Make sure your server script is active! Error: {err}")


# -----------------------------------------------------------------
# SEQUENTIAL DEMO TEST SEQUENCE
# -----------------------------------------------------------------
if __name__ == "__main__":
    print("=== STARTING ADVANCED SUITE DEMO PIPELINE ===")

    # 1. Test Listing with constraint parameter tracking
    test_api_endpoint("/listSpecies?limit=3&json=1")

    # 2. Test Chromosome structural length extraction metrics
    test_api_endpoint("/chromosomeLength?species=human&chromo=Y&json=1")

    # 3. Test Molecular Gene ID Lookup properties
    test_api_endpoint("/geneLookup?gene=FRAT1&json=1")

    # 4. Test Automated calculations pipeline via standard class definitions
    test_api_endpoint("/geneCalc?gene=FRAT1&json=1")

    print("\n=== PIPELINE DEMO TESTS CONCLUDED RECOVERY SUCCESSFUL ===")