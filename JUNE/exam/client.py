import socket
import json

def test_api_endpoint(path_query):                # "test_api_endpoint expects us to give it a specific request address, which it'll temporarily call "path_query"
    print(f"\n[CLIENT] Requesting raw target data string: http://localhost:8080{path_query}")
    try:                      #Attempt ot use the following code, but if the network is broken or the server is turned off, you can use the error net at the bottom
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect(("127.0.0.1", 8080))

        http_req = (                      #text message asking for data
            f"GET {path_query} HTTP/1.1\r\n"     #It asks the server to get him the data at this path
            f"Host: localhost:8080\r\n"         #It says that it's talking with localhost:8080
            f"Connection: close\r\n\r\n"          #It says that the connection can be closed right after answering the message
        )
        c.sendall(http_req.encode("utf-8"))

        stream_chunks = []       #we create an empty list for the data that the server is going to send us
        while True:
            chunk = c.recv(4096)
            if not chunk:      #if the server stops talking, the loop breaks and stops listening
                break
            stream_chunks.append(chunk)    #we pour all of our data into the list we created before
        c.close()      #we officially close the socket

        full_payload = b"".join(stream_chunks)      #It takes all the elements from the list we created and puts them together into one giant data package called "full_payload"

        if b"\r\n\r\n" in full_payload:       #If there is an empty line inside the received internet data...
            body_bytes = full_payload.split(b"\r\n\r\n", 1)[1]     #Take the internet message, split it into headers and body, and save the body part
            body_string = body_bytes.decode("utf-8")    #Convert the body from computer bytes into readable text

            parsed_json = json.loads(body_string)    #Takes the JSON text and converts it into usable Python data.
            print(json.dumps(parsed_json, indent=2))    #Prints the Python data as nicely formatted JSON.
        else:
            print("[CLIENT ERROR] Received invalid data transmission envelope framework.")

    except Exception as err:
        print(f"[CLIENT CONNECTION FAILURE] Make sure your server script is active! Error: {err}")       #If the server wasn't running or the network is broken, the computer jumps straight down here and prints a helpful warning, instead of directly turing into a red error screen


if __name__ == "__main__":     #when the human doubl clicks the specific file, the following file will be done in order
    print("=== STARTING ADVANCED SUITE DEMO PIPELINE ===")    #starting banner

    test_api_endpoint("/listSpecies?limit=3&json=1")   #Tells the messenger drone to ask for a list of species, but limits the answer to just 3 species

    test_api_endpoint("/chromosomeLength?species=human&chromo=Y&json=1")   #It asks the server for the length of the Y chromosome in a human

    test_api_endpoint("/geneLookup?gene=FRAT1&json=1")     #It asks the server to look up a specific gene called FRAT1

    test_api_endpoint("/geneCalc?gene=FRAT1&json=1")      #It asks the server to perform math calculations on that FRAT1 gene (likely using the percentage math code we used in Seq.py)

    print("\n=== PIPELINE DEMO TESTS CONCLUDED RECOVERY SUCCESSFUL ===")      #final closing banner