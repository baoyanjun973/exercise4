import sqlite3

# connect database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN of the book: ")
    status = input("Enter the status of the book: ")

    cursor.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)",
                   (title, author, isbn, status))
    conn.commit()
    print("Book added successfully!")

def find_book_details():
    book_id = input("Enter the BookID: ")

    cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                      Users.Name, Users.Email
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID
                      WHERE Books.BookID = ?''', (book_id,))
    result = cursor.fetchone()

    if result:
        book_id, title, author, isbn, status, user_name, user_email = result
        if user_name and user_email:
            print(f"BookID: {book_id}\nTitle: {title}\nAuthor: {author}\nISBN: {isbn}\nStatus: {status}")
            print(f"Reserved by: {user_name} ({user_email})")
        else:
            print(f"BookID: {book_id}\nTitle: {title}\nAuthor: {author}\nISBN: {isbn}\nStatus: {status}")
            print("This book is not reserved.")
    else:
        print("Book not found.")

def find_reservation_status():
    search_text = input("Enter BookID, Title, UserID, or ReservationID: ")

    if search_text.startswith("LB"):
        book_id = search_text[2:]  # Extract the numeric part from BookID
        cursor.execute('''SELECT Books.Status
                          FROM Books
                          WHERE Books.BookID = ?''', (book_id,))
        result = cursor.fetchone()

        if result:
            print(f"Reservation status for BookID {book_id}: {result[0]}")
        else:
            print("Book not found.")
    elif search_text.startswith("LU"):
        user_id = search_text[2:]  # Extract the numeric part from UserID
        cursor.execute('''SELECT Books.Status
                          FROM Books
                          INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                          INNER JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Users.UserID = ?''', (user_id,))
        result = cursor.fetchone()

        if result:
            print(f"Reservation status for UserID {user_id}: {result[0]}")
        else:
            print("User not found.")
    elif search_text.startswith("LR"):
        reservation_id = search_text[2:]  # Extract the numeric part from ReservationID
        cursor.execute('''SELECT Books.Status
                          FROM Books
                          INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                          WHERE Reservations.ReservationID = ?''', (reservation_id,))
        result = cursor.fetchone()

        if result:
            print(f"Reservation status for ReservationID {reservation_id}: {result[0]}")
        else:
            print("Reservation not found.")
    else:
        cursor.execute('''SELECT Books.Status
                          FROM Books
                          WHERE Books.Title = ?''', (search_text,))
        result = cursor.fetchone()

        if result:
            print(f"Reservation status for Title '{search_text}': {result[0]}")
        else:
            print("Book not found.")

def find_all_books():
    cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                      Users.Name, Users.Email
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    results = cursor.fetchall()

    if results:
        for result in results:
            book_id, title, author, isbn, status, user_name, user_email = result
            if user_name and user_email:
                print(f"BookID: {book_id}\nTitle: {title}\nAuthor: {author}\nISBN: {isbn}\nStatus: {status}")
                print(f"Reserved by: {user_name} ({user_email})\n")
            else:
                print(f"BookID: {book_id}\nTitle: {title}\nAuthor: {author}\nISBN: {isbn}\nStatus: {status}")
                print("This book is not reserved.\n")
    else:
        print("No books found.")

def update_book_details():
    book_id = input("Enter the BookID of the book to update: ")

    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    result = cursor.fetchone()

    if result:
        print("Current book details:")
        print(f"BookID: {result[0]}\nTitle: {result[1]}\nAuthor: {result[2]}\nISBN: {result[3]}\nStatus: {result[4]}")

        choice = input("Do you want to update the reservation status? (y/n): ")

        if choice.lower() == "y":
            new_status = input("Enter the new reservation status: ")

            cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
            cursor.execute("UPDATE Reservations SET Status = ? WHERE BookID = ?", (new_status, book_id))
            conn.commit()
            print("Reservation status updated successfully!")
        else:
            new_title = input("Enter the new title (leave blank to keep the current title): ")
            new_author = input("Enter the new author (leave blank to keep the current author): ")
            new_isbn = input("Enter the new ISBN (leave blank to keep the current ISBN): ")

            if new_title or new_author or new_isbn:
                cursor.execute("UPDATE Books SET Title = ?, Author = ?, ISBN = ? WHERE BookID = ?",
                               (new_title, new_author, new_isbn, book_id))
                conn.commit()
                print("Book details updated successfully!")
            else:
                print("No changes made.")
    else:
        print("Book not found.")

def delete_book():
    book_id = input("Enter the BookID of the book to delete: ")

    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully!")
    else:
        print("Book not found.")

def exit_program():
    conn.close()
    print("Exiting the program...")
    exit()

# 主程序循环
while True:
    print("\nLibrary Management System")
    print("1. Add a new book to the database")
    print("2. Find a book's detail based on BookID")
    print("3. Find a book's reservation status based on BookID, Title, UserID, and ReservationID")
    print("4. Find all the books in the database")
    print("5. Modify/update book details based on its BookID")
    print("6. Delete a book based on its BookID")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_details()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        update_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        exit_program()
    else:
        print("Invalid choice. Please try again.")
