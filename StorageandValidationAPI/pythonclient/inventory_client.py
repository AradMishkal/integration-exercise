import csv
import json
import requests

API_URL = "http://localhost:3000/inventory_uploads.json"  # API endpoint to interact with Rails server


def generate_csv():  # Create a sample CSV file
    data = [
        {'name': 'Widget A', 'quantity': '10', 'price': '2.50'},
        {'name': 'Widget B', 'quantity': '5', 'price': '3.00'},
        {'name': 'Widget C', 'quantity': '20', 'price': '1.75'}
    ]
    with open('inventory.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'quantity', 'price'])
        writer.writeheader()
        writer.writerows(data)
    print("CSV file generated as inventory.csv")


def upload():  # Read CSV and send data to Rails server
    with open('inventory.csv', newline='') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    response = requests.post(API_URL, json=data)
    if 200 <= response.status_code < 300:
        print(response.json())
    else:
        print(f"Failed to upload: {response.status_code} - {response.text}")


def list_uploads():  # Get batch summaries from Rails server
    response = requests.get(API_URL)
    print(json.dumps(response.json(), indent=2))


if __name__ == '__main__':
    print("What would you like to do?")
    print("1. Generate CSV")
    print("2. Upload CSV to API")
    print("3. List uploads")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == '1':
        generate_csv()
    elif choice == '2':
        upload()
    elif choice == '3':
        list_uploads()
    else:
        print("Invalid choice.")
