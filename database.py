import sqlite3

# Connect to SQLLite database
conn = sqlite3.connect('bookwarrior.db')

c = conn.cursor()

# Create table
c.execute("""CREATE TABLE books
          (title text, genre text, pages integer, format text, library text)""")

conn.commit()

conn.close()


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

add_book()

