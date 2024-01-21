import sqlite3

def add_book():
   title = input("Enter book title: ")
   genre = input("Enter book genre: ")
   pages = int(input("Enter number of pages: "))
   format = input("Is the book digital or physical? ")
   library = input("Is the book a library book? ")
   
   # Insert data into database
   conn = sqlite3.connect('bookwarrior.db')
   c = conn.cursor()
   c.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?)", (title, genre, pages, format, library))
   conn.commit()
   conn.close()


def view_library():
    # Connect to SQLite database
    conn = sqlite3.connect('bookwarrior.db')
    c = conn.cursor()

    # Query all books
    c.execute("SELECT * FROM books")
    all_books = c.fetchall()

    # Check if there are books in the library
    if all_books:
        print("\nLibrary:")
        for book in all_books:
            title, genre, pages, format, library = book
            print(f"Title: {title}, Genre: {genre}, Pages: {pages}, Format: {format}, Library Book: {library}")
    else:
        print("Your library is empty.")

    # Close the database connection
    conn.close()

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Add a Book")
        print("2. View Library")
        print("3. Pick Book-of-the-Week")
        print("4. Book Notes")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            view_library()
        elif choice == '3':
            # Code for Pick Book-of-the-Week
            pass
        elif choice == '4':
            # Code for Book Notes
            pass
        elif choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

def setup_database():
    conn = sqlite3.connect('bookwarrior.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS books
                 (title text, genre text, pages integer, format text, library text)""")

    conn.commit()
    conn.close()

# Main entry point of the script
if __name__ == "__main__":
    setup_database()  # Set up the database first
    main_menu()       # Then show the main menu