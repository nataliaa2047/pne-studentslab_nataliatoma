import json

# Load the JSON data
with open('S18/people-e1.json', 'r') as file:
    people = json.load(file)

# 1. Print total number of people
print(f"Total people in the database: {len(people)}")
print()

# 2. Iterate and print each person
for person in people:
    print(f"Name: {person['name']}")
    print(f"Age: {person['age']}")

    # Print phone number count
    phones = person['phones']
    print(f"Phone numbers: {len(phones)}")

    # Iterate through phone numbers
    for i, phone in enumerate(phones):
        print(f"Phone {i}:")
        print(f"  Type: {phone['type']}")
        print(f"  Number: {phone['number']}")

    print()  # Adds a blank line for readability between entries