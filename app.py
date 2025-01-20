import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# Function to fetch books from the database
def fetch_books_from_db():
    try:
        conn = psycopg2.connect(
            dbname="library_management_system",
            user="library_user",
            password="P$b7iIx#6@BJCOw",
            host="localhost",
            port="5432"
        )

        cursor = conn.cursor()
        
        # Query to fetch books data from the 'catalog' table in the 'library_management_system' database
        cursor.execute('SELECT bookid, title, authors, status FROM catalog')
        
        books = []
        rows = cursor.fetchall()
        
        for row in rows:
            book = {
                "bookID": row[0],        # bookid (integer)
                "title": row[1],         # title (string)
                "author": row[2],        # authors (string)
                "status": row[3],        # status (Available/Issued)
            }
            books.append(book)

        cursor.close()
        conn.close()
        
        return books
    
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch data from the database: {str(e)}")
        return []


# Function to add book to the database
def add_book_to_db(book):
    try:
        conn = psycopg2.connect(
            dbname="library_management_system",
            user="library_user",
            password="P$b7iIx#6@BJCOw",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Insert the new book into the catalog table
        cursor.execute('''INSERT INTO catalog (bookid, title, authors, status) 
                          VALUES (%s, %s, %s, %s)''',
                       (book["bookID"], book["title"], book["author"], book["status"]))

        # Commit the transaction to save changes
        conn.commit()

        cursor.close()
        conn.close()
        
        print(f"Added book to DB: {book}")
        
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to add book to the database: {str(e)}")


# Function to update the table with book data
def update_table(books):
    for row in table.get_children():
        table.delete(row)
    for book in books:
        table.insert("", "end", values=(book["bookID"], book["title"], book["author"], book["status"]))


# Function to handle adding a new book
def add_book():
    global books_data  # Declare global inside the function before modifying it
    title = title_entry.get()
    author = author_entry.get()

    if title and author:
        # Create new book dictionary
        new_book = {"bookID": len(books_data) + 1, "title": title, "author": author, "status": "Available"}

        # Add the book to the database
        add_book_to_db(new_book)

        # Re-fetch the updated book data from the database
        books_data = fetch_books_from_db()  # Update books_data

        # Update the table to reflect the new data
        update_table(books_data)

        # Clear input fields
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Input Error", "Please provide both title and author!")


# Function to search books by keyword
def search_books(keyword):
    filtered_books = [book for book in books_data if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower()]
    return filtered_books


# Function to handle search
def search_books_handler():
    keyword = search_entry.get()
    if keyword:
        filtered_books = search_books(keyword)
        update_table(filtered_books)
        search_button.config(text="Home", command=go_home, bg="blue")
    else:
        messagebox.showerror("Input Error", "Please enter a keyword to search!")


# Function to return to the home view (show all books)
def go_home():
    update_table(books_data)
    search_button.config(text="Search", command=search_books_handler, bg="black")


# Function to issue a book
def issue_selected_book():
    selected = table.selection()
    if selected:
        book_id = table.item(selected)["values"][0]
        for book in books_data:
            if book["bookID"] == book_id and book["status"] == "Available":
                book["status"] = "Issued"
                # Update the book status in the database
                update_book_status_in_db(book)
                update_table(books_data)
                return
        messagebox.showerror("Issue Error", "Selected book is already issued!")
    else:
        messagebox.showerror("Selection Error", "No book selected!")


# Function to update the book status in the database
def update_book_status_in_db(book):
    try:
        conn = psycopg2.connect(
            dbname="library_management_system",
            user="library_user",
            password="P$b7iIx#6@BJCOw",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Update the status of the book
        cursor.execute('''UPDATE catalog SET status = %s WHERE bookid = %s''',
                       (book["status"], book["bookID"]))

        # Commit the transaction to save changes
        conn.commit()

        cursor.close()
        conn.close()
        
        print(f"Updated status for book {book['bookID']} to {book['status']}")
        
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to update book status: {str(e)}")


# Function to return a book
def return_selected_book():
    selected = table.selection()
    if selected:
        book_id = table.item(selected)["values"][0]
        for book in books_data:
            if book["bookID"] == book_id and book["status"] == "Issued":
                book["status"] = "Available"
                # Update the book status in the database
                update_book_status_in_db(book)
                update_table(books_data)
                return
        messagebox.showerror("Return Error", "Selected book is already available!")
    else:
        messagebox.showerror("Selection Error", "No book selected!")


# Function to show book details
def view_book_details():
    selected = table.selection()
    if selected:
        book_id = table.item(selected)["values"][0]
        selected_book = next(book for book in books_data if book["bookID"] == book_id)
        show_book_details_window(selected_book)
    else:
        messagebox.showerror("Selection Error", "No book selected!")


# Function to show the window with book details
def show_book_details_window(book):
    details_window = tk.Toplevel(root)
    details_window.title("Book Details")
    title_width = len(book['title']) * 10
    width = max(400, title_width + 40)
    details_window.geometry(f"{width}x170")
    tk.Label(details_window, text=f"Title: {book['title']}", font=("Arial", 14)).pack(pady=5)
    tk.Label(details_window, text=f"Author: {book['author']}", font=("Arial", 14)).pack(pady=5)
    tk.Label(details_window, text=f"Status: {book['status']}", font=("Arial", 14)).pack(pady=5)
    ok_button = tk.Button(details_window, text="OK", command=details_window.destroy, bg="green", fg="white")
    ok_button.pack(pady=10)


# Function to delete the selected book
def delete_selected_book():
    selected = table.selection()
    if selected:
        book_id = table.item(selected)["values"][0]
        book_to_delete = next(book for book in books_data if book["bookID"] == book_id)
        
        # Delete the book from the database
        delete_book_from_db(book_to_delete["bookID"])

        # Remove the book from the local data
        books_data.remove(book_to_delete)
        
        update_table(books_data)
        show_book_deleted_window(book_to_delete['title'])
        print(f"Deleted book: {book_to_delete}")
    else:
        messagebox.showerror("Selection Error", "No book selected!")


# Function to delete a book from the database
def delete_book_from_db(book_id):
    try:
        conn = psycopg2.connect(
            dbname="library_management_system",
            user="library_user",
            password="P$b7iIx#6@BJCOw",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Delete the book from the catalog
        cursor.execute('''DELETE FROM catalog WHERE bookid = %s''', (book_id,))

        # Commit the transaction to save changes
        conn.commit()

        cursor.close()
        conn.close()
        
        print(f"Deleted book with ID {book_id} from DB")
        
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to delete book from database: {str(e)}")


# Function to show a window after a book is deleted
def show_book_deleted_window(book_title):
    delete_window = tk.Toplevel(root)
    delete_window.title("Book Deleted")
    width = max(400, len(book_title) * 10 + 40)
    delete_window.geometry(f"{width}x120")
    
    tk.Label(delete_window, text="Book Deleted Successfully!", font=("Arial", 16, "bold"), fg="red").pack(pady=5)
    tk.Label(delete_window, text=f"Title: {book_title}", font=("Arial", 14), fg="black").pack(pady=5)
    
    ok_button = tk.Button(delete_window, text="OK", command=delete_window.destroy, bg="green", fg="white")
    ok_button.pack(pady=10)


# Create the main window
root = tk.Tk()
root.title("Library Management System")
root.geometry("1920x1080")
root.resizable(True, True)

# Initialize books data
books_data = fetch_books_from_db()

# Add Book Frame
add_book_frame = tk.Frame(root)
add_book_frame.pack(pady=10, padx=10, fill="x")

tk.Label(add_book_frame, text="Title").grid(row=0, column=0, padx=5, pady=5)
title_entry = tk.Entry(add_book_frame)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(add_book_frame, text="Author").grid(row=0, column=2, padx=5, pady=5)
author_entry = tk.Entry(add_book_frame)
author_entry.grid(row=0, column=3, padx=5, pady=5)

add_book_button = tk.Button(add_book_frame, text="Add Book", command=add_book, bg="green", fg="white")
add_book_button.grid(row=0, column=4, padx=5, pady=5)

# Search Frame
search_frame = tk.Frame(root)
search_frame.pack(pady=10, padx=10, fill="x")

tk.Label(search_frame, text="Search").grid(row=0, column=0, padx=5, pady=5)
search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = tk.Button(search_frame, text="Search", command=search_books_handler, bg="black", fg="white")
search_button.grid(row=0, column=2, padx=5, pady=5)

# Table Frame
table_frame = tk.Frame(root)
table_frame.pack(pady=10, padx=10, fill="both", expand=True)

columns = ("ID", "Title", "Author", "Status")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
table.heading("ID", text="ID")
table.heading("Title", text="Title")
table.heading("Author", text="Author")
table.heading("Status", text="Status")
table.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Action Buttons Frame
action_frame = tk.Frame(root)
action_frame.pack(pady=10)

issue_button = tk.Button(action_frame, text="Issue Book", command=issue_selected_book, bg="orange", fg="white")
issue_button.grid(row=0, column=0, padx=10)

return_button = tk.Button(action_frame, text="Return Book", command=return_selected_book, bg="purple", fg="white")
return_button.grid(row=0, column=1, padx=10)

view_button = tk.Button(action_frame, text="View Details", command=view_book_details, bg="cyan", fg="black")
view_button.grid(row=0, column=2, padx=10)

delete_button = tk.Button(action_frame, text="Delete Book", command=delete_selected_book, bg="red", fg="white")
delete_button.grid(row=0, column=3, padx=10)

# Initial load of books into the table
update_table(books_data)

# Run the application
root.mainloop()
