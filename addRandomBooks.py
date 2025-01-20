import psycopg2
import random

# List of book names and authors for random selection
book_titles = [
    "Pride and Prejudice", "The Catcher in the Rye", "Moby Dick",
    "Crime and Punishment", "To Kill a Mockingbird", "The Great Gatsby",
    "1984", "Brave New World", "The Hobbit", "The Odyssey"
]

book_authors = [
    "Jane Austen", "J.D. Salinger", "Herman Melville",
    "Fyodor Dostoevsky", "Harper Lee", "F. Scott Fitzgerald",
    "George Orwell", "Aldous Huxley", "J.R.R. Tolkien", "Homer"
]

# Function to add random books to the database
def add_random_books():
    try:
        conn = psycopg2.connect(
            dbname="library_management_system",
            user="library_user",
            password="P$b7iIx#6@BJCOw",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Fetch the current maximum bookid to set the next value for sequence
        cursor.execute("SELECT MAX(bookid) FROM catalog")
        max_bookid = cursor.fetchone()[0]
        
        if max_bookid is not None:
            # Set the sequence to the max bookid
            cursor.execute(f"SELECT setval('catalog_bookid_seq', {max_bookid})")
            conn.commit()

        # Add 10 random books to the catalog
        for _ in range(10):
            title = random.choice(book_titles)
            author = random.choice(book_authors)

            # Insert a new book
            cursor.execute("INSERT INTO catalog (title, authors, status) VALUES (%s, %s, %s)", 
                           (title, author, "Available"))
            print(f"Added book: {title} by {author}")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Failed to add books to the database: {str(e)}")

# Run the function to add random books
add_random_books()
