import tkinter as tk
from tkinter import messagebox, simpledialog
from database import add_book, view_library, pick_book_of_the_week, add_note, get_notes
import sqlite3
import random
import math

# GUI function to add a book
def add_book_gui():
    def submit_book():
        title = title_entry.get()
        genre = genre_entry.get()
        pages = pages_entry.get()
        format = format_entry.get()
        library = library_entry.get()
        add_book(title, genre, int(pages), format, library)
        messagebox.showinfo("Success", "Book added successfully")
        add_window.destroy()

    # Create a new window for adding a book
    add_window = tk.Toplevel()
    add_window.title("Add a Book")

    tk.Label(add_window, text="Book Title:").grid(row=0, column=0)
    title_entry = tk.Entry(add_window)
    title_entry.grid(row=0, column=1)

    tk.Label(add_window, text="Book Genre:").grid(row=1, column=0)
    genre_entry = tk.Entry(add_window)
    genre_entry.grid(row=1, column=1)

    tk.Label(add_window, text="Number of Pages:").grid(row=2, column=0)
    pages_entry = tk.Entry(add_window)
    pages_entry.grid(row=2, column=1)

    tk.Label(add_window, text="Format (Digital/Physical):").grid(row=3, column=0)
    format_entry = tk.Entry(add_window)
    format_entry.grid(row=3, column=1)

    tk.Label(add_window, text="Library Book (Yes/No):").grid(row=4, column=0)
    library_entry = tk.Entry(add_window)
    library_entry.grid(row=4, column=1)

    submit_button = tk.Button(add_window, text="Add", command=submit_book)
    submit_button.grid(row=5, column=0, columnspan=2)

# GUI function to view the library
def view_library_gui():
    books = view_library()

    view_window = tk.Toplevel()
    view_window.title("View Library")

    text = ""
    if books:
        for book in books:
            text += f"Title: {book[0]}, Genre: {book[1]}, Pages: {book[2]}, Format: {book[3]}, Library Book: {book[4]}\n"
    else:
        text = "Your library is empty."

    tk.Label(view_window, text=text).pack()

def pick_book_of_the_week_gui():
    # Function to interact with the user and call pick_book_of_the_week
    max_pages = simpledialog.askinteger("Book-of-the-Week", "Around how many pages?")
    if max_pages is None:  # User closed the dialog or clicked cancel
        return

    format_choice = simpledialog.askstring("Book-of-the-Week", "Digital or Physical?")
    if format_choice is None:  # User closed the dialog or clicked cancel
        return

    format_choice = format_choice.lower()
    title, pages = pick_book_of_the_week(max_pages, format_choice)
    pages_per_week = math.ceil(pages / 7)
    messagebox.showinfo("Book-of-the-Week", f"Your Book-of-the-Week will be '{title}', you will need to reach {pages_per_week} pages per week to finish it.")

# Function to add a book to the database
def add_book(title, genre, pages, format, library):
    conn = sqlite3.connect('bookwarrior.db')
    c = conn.cursor()
    c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?)", (title, genre, pages, format, library))
    conn.commit()
    conn.close()

# Function to get all books from the database
def view_library():
    conn = sqlite3.connect('bookwarrior.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    all_books = c.fetchall()
    conn.close()
    return all_books

def pick_book_of_the_week(max_pages, format_choice):
    # Read the already picked books
    try:
        with open("picked_books.txt", "r") as file:
            picked_books = file.read().splitlines()
    except FileNotFoundError:
        picked_books = []

    # Connect to the database
    conn = sqlite3.connect('bookwarrior.db')
    c = conn.cursor()

    # Dynamically build the query
    query = "SELECT * FROM books WHERE pages <= ? AND LOWER(format) = ?"
    params = [max_pages, format_choice]

    if picked_books:
        placeholders = ','.join('?' * len(picked_books))
        query += " AND title NOT IN ({})".format(placeholders)
        params.extend(picked_books)

    c.execute(query, params)
    eligible_books = c.fetchall()

    conn.close()

    if not eligible_books:
        return None

    # Pick a random book
    chosen_book = random.choice(eligible_books)
    title, _, pages, _, _ = chosen_book

    # Store the chosen book
    with open("picked_books.txt", "a") as file:
        file.write(title + "\n")

    return title, pages

def book_notes_gui():
    def add_note_gui():
        book_titles = [book[0] for book in view_library()]
        if not book_titles:
            messagebox.showinfo("No Books", "No books in the library to add a note.")
            return

        title = simpledialog.askstring("Add a Note", "Enter the book title:", initialvalue=book_titles[0])
        if title not in book_titles:
            messagebox.showinfo("Invalid Book", "The book title entered is not in the library.")
            return

        note = simpledialog.askstring("Add a Note", "Enter your note:")
        add_note(title, note)
        messagebox.showinfo("Note Added", "Your note has been added.")

    def view_notes_gui():
        book_titles = [book[0] for book in view_library()]
        if not book_titles:
            messagebox.showinfo("No Books", "No books in the library to view notes.")
            return

        title = simpledialog.askstring("View Notes", "Enter the book title:", initialvalue=book_titles[0])
        if title not in book_titles:
            messagebox.showinfo("Invalid Book", "The book title entered is not in the library.")
            return

        notes = get_notes(title)
        notes_text = "\n".join(notes) if notes else "No notes for this book."
        messagebox.showinfo("Notes for " + title, notes_text)

    action = simpledialog.askstring("Book Notes", "Choose an action: Add a Note or View Notes")
    if action.lower() == "add a note":
        add_note_gui()
    elif action.lower() == "view notes":
        view_notes_gui()

def setup_database():
    conn = sqlite3.connect('bookwarrior.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS books
                 (title text, genre text, pages integer, format text, library text)""")
    c.execute("""CREATE TABLE IF NOT EXISTS notes
                 (title text, note text)""")

    conn.commit()
    conn.close()

# Main menu window
def main_menu_window():
    window = tk.Tk()
    window.title("BookWarrior")

    # Set the size of the window
    window.geometry("800x600") # Example size: 800 width and 600 height

    # Configure button size and font
    button_width = 20 # Width of the button
    button_height = 2 # Height of the button 
    button_font = ('Arial', 14) # Font type and size

    # Create and pack the "Add a Book" button
    add_book_button = tk.Button(window, text="Add a Book", command=add_book_gui, width=button_width, height=button_height, font=button_font)
    add_book_button.pack(pady=10)  # pady adds some vertical space around the button

    # Create and pack the "View Library" button
    view_library_button = tk.Button(window, text="View Library", command=view_library_gui, width=button_width, height=button_height, font=button_font)
    view_library_button.pack(pady=10)  # pady adds some vertical space around the button

    # Create and pack the "Book of the Week" button
    book_of_week_button = tk.Button(window, text="Pick Book-of-the-Week", command=pick_book_of_the_week_gui, width=button_width, height=button_height, font=button_font)
    book_of_week_button.pack(pady=10)

    # Create add notes button
    tk.Button(window, text="Book Notes", command=book_notes_gui, width=20, height=2, font=('Arial', 14)).pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    setup_database()  # Initialize the database and create tables
    main_menu_window() # Start the GUI application
