## Library Management System with PostgreSQL Integration
This project involves building a `Library Management System (LMS)` using Python and PostgreSQL. The application allows users to view, search, add, issue, return, and delete books, while the backend is powered by a PostgreSQL database. Additionally, we fetch a `CSV file` of books, process the data, and import it into PostgreSQL.

### Features
- `View Books`: Displays a list of all books in the library.
- `Add Book`: Adds new books to the library.
- `Search Books`: Search books by title or author.
- `Issue/Return Book`: Mark books as issued or returned.
- `Delete Book`: Delete books from the system.
- `Book Details`: View details about individual books.
## Data Engineering Process
#### 1. Fetching and Processing CSV Data
We used a publicly available CSV file from Omair31's GitHub repo that contains book data - https://github.com/Omair31/BooksCSV/blob/master/BooksCSV/books.csv. This data is processed and saved with a randomly assigned status of either Available or Issued.

#### 2. Importing Data into PostgreSQL
After downloading and modifying the CSV data, we import it into the PostgreSQL database using the following steps:

### Step 1: Save the CSV file to a local directory
```python
import requests
import csv
import random

# URL of the CSV file
csv_url = "https://raw.githubusercontent.com/Omair31/BooksCSV/refs/heads/master/BooksCSV/books.csv"
save_path = "/tmp/modified_books.csv"

def fetch_and_process_csv(url, save_path):
    try:
        # Fetching CSV data from the URL
        response = requests.get(url)
        if response.status_code == 200:
            # Processing CSV data and adding random 'status'
            lines = response.text.splitlines()
            reader = csv.DictReader(lines)
            fieldnames = ["bookID", "title", "authors", "status"]
            modified_books = []

            for row in reader:
                modified_books.append({
                    "bookID": row["bookID"],
                    "title": row["title"],
                    "authors": row["authors"],
                    "status": random.choice(["Available", "Issued"])
                })

            # Saving processed CSV
            with open(save_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(modified_books)

            print(f"CSV data processed and saved to {save_path}")
        else:
            print(f"Failed to fetch CSV. HTTP Status code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

# Run the fetch and process function
fetch_and_process_csv(csv_url, save_path)
```
### Step 2: Import CSV into PostgreSQL
- Once the CSV is processed and saved locally (/tmp/modified_books.csv), you can import it into PostgreSQL.

```bash
-- Ensure the table 'catalog' exists in your PostgreSQL database:
CREATE TABLE IF NOT EXISTS catalog (
    bookid SERIAL PRIMARY KEY,
    title VARCHAR(255),
    authors TEXT,
    status VARCHAR(20)
);

-- Grant permissions to the database user
GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE catalog TO library_user;

-- Load the CSV into PostgreSQL using COPY command
COPY catalog(bookid, title, authors, status)
FROM '/tmp/modified_books.csv'
DELIMITER ','
CSV HEADER;
```
### Permissions
- Ensure that the user library_user has the necessary permissions for reading and writing to the database:

```bash
-- Grant necessary permissions
GRANT CONNECT, USAGE ON SCHEMA public TO library_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO library_user;

-- If running into permission issues with the COPY command, ensure the user has the necessary file access:
-- You can run the PostgreSQL server as a superuser or configure appropriate file access.
```
# PostgreSQL Commands for Data Operations

To interact with and manipulate the data in your PostgreSQL database, you can use the following SQL commands. These commands will allow you to view the books, search, update the book status, and perform other operations.

## 1. View All Books

To view all books in the catalog, execute the following query:

```sql
SELECT * FROM catalog;

```
- This will return all the columns (bookid, title, authors, status) for every book in the catalog.
## 2. Search Books by Title or Author
To search for books by title or author, use the following query:

```sql
SELECT * FROM catalog 
WHERE LOWER(title) LIKE LOWER('%search_keyword%') 
   OR LOWER(authors) LIKE LOWER('%search_keyword%');
```
- Replace search_keyword with the keyword you're looking for (e.g., "Moby Dick", "Harper Lee"). This query will return books whose title or author matches the provided keyword.

## 3. Add a New Book
To add a new book to the catalog, you can insert a new row into the catalog table:

```sql
INSERT INTO catalog (title, authors, status)
VALUES ('Book Title', 'Book Author', 'Available');
```
- Replace 'Book Title', 'Book Author', and 'Available' with the actual book title, author, and its initial status.

## 4. Update the Status of a Book
To update the status of a book (e.g., from "Available" to "Issued"), use the following query:

```sql
UPDATE catalog 
SET status = 'Issued' 
WHERE bookid = 1;  -- Replace 1 with the actual bookid of the book you want to update
```
- This will update the status of the book with the specified bookid to "Issued".

## 5. Delete a Book
To delete a book from the catalog, use the following command:

```sql
DELETE FROM catalog
WHERE bookid = 1;  -- Replace 1 with the actual bookid of the book you want to delete
```
- This will delete the book with the specified bookid from the catalog.

## 6. Count the Number of Books by Status
To count how many books are available or issued, use the following query:

```sql
SELECT status, COUNT(*) 
FROM catalog
GROUP BY status;
```
- This will give you the number of books for each status (Available and Issued).

## 7. Get the Latest Added Book
To fetch the most recently added book to the catalog, use the following query:

```sql
SELECT * FROM catalog
ORDER BY bookid DESC
LIMIT 1;
```
- This will return the book with the highest bookid, which corresponds to the most recently added book.

## 8. Find Books by Author
To search for books by a specific author, use the following query:

```sql
SELECT * FROM catalog
WHERE LOWER(authors) = LOWER('author_name');
```
- Replace 'author_name' with the name of the author you are searching for (e.g., 'Harper Lee').

## 9. Get the Books with the Longest Title
To fetch the books with the longest titles, use the following query:

```sql
SELECT * FROM catalog
ORDER BY LENGTH(title) DESC
LIMIT 5;
```
- This will return the top 5 books with the longest titles.

### Conclusion
- This project integrates a Python-based application with a PostgreSQL database to manage library books. It also includes processing a CSV file containing book data, modifying the data, and importing it into the PostgreSQL database for further operations.





