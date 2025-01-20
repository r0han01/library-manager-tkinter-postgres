import csv
import random
import requests

# URL of the CSV file
csv_url = "https://raw.githubusercontent.com/Omair31/BooksCSV/refs/heads/master/BooksCSV/books.csv"

# Path where the modified CSV will be saved
save_path = "/home/r0han/Downloads/modified_books.csv"

def fetch_and_process_csv(url, save_path):
    try:
        # Send GET request to the URL to fetch the CSV data
        response = requests.get(url)
        
        if response.status_code == 200:
            # Read the CSV content from the response text
            lines = response.text.splitlines()
            reader = csv.DictReader(lines)
            
            # Prepare the output fieldnames and data
            fieldnames = ["bookID", "title", "authors", "status"]
            modified_books = []

            # Process each row
            for row in reader:
                book = {
                    "bookID": row["bookID"],
                    "title": row["title"],
                    "authors": row["authors"],
                    "status": random.choice(["Available", "Issued"])  # Random status
                }
                modified_books.append(book)

            # Write the processed data to a new CSV file
            with open(save_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(modified_books)

            print(f"CSV data processed and saved to {save_path}")

        else:
            print(f"Failed to fetch CSV. HTTP Status code: {response.status_code}")
    
    except Exception as e:
        print(f"Error: {e}")

# Call the function to fetch, process, and save the data
fetch_and_process_csv(csv_url, save_path)
