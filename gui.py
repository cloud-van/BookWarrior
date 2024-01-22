import tkinter as tk
from tkinter import messagebox, simpledialog
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
    window.mainloop()

if __name__ == "__main__":
    main_menu_window()
