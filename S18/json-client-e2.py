import http.client
import json

# 1. Connect to the local server
conn = http.client.HTTPConnection('localhost', 8000)

# 2. Request the specific resource
conn.request("GET", "/listusers")

# 3. Get the response
response = conn.getresponse()
data = json.loads(response.read().decode('utf-8'))

# 4. Print the output (using the logic from the previous exercise)
print(f"Total people in the database: {len(data)}")
print()

for person in data:
    print(f"Name: {person['name']}")
    print(f"Age: {person['age']}")
    phones = person['phones']
    print(f"Phone numbers: {len(phones)}")
    for i, phone in enumerate(phones):
        print(f"Phone {i}:")
        print(f"  Type: {phone['type']}")
        print(f"  Number: {phone['number']}")
    print()

conn.close()