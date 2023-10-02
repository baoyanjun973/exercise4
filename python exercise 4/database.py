import sqlite3

# Connect to the database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create the Books table
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                    BookID INTEGER PRIMARY KEY,
                    Title TEXT,
                    Author TEXT,
                    ISBN TEXT,
                    Status TEXT
                )''')

# Create the Users table
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    UserID INTEGER PRIMARY KEY,
                    Name TEXT,
                    Email TEXT
                )''')

# Create the Reservations table
cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                    ReservationID INTEGER PRIMARY KEY,
                    BookID INTEGER,
                    UserID INTEGER,
                    ReservationDate TEXT,
                    FOREIGN KEY (BookID) REFERENCES Books (BookID),
                    FOREIGN KEY (UserID) REFERENCES Users (UserID)
                )''')

# Add sample data to the Books table
cursor.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES ('Book 1', 'Author 1', 'ISBN 123456789', 'Reserved')")
cursor.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES ('Book 2', 'Author 2', 'ISBN 987654321', 'Available')")
cursor.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES ('Book 3', 'Author 3', 'ISBN 456789123', 'Reserved')")

# Add sample data to the Users table
cursor.execute("INSERT INTO Users (Name, Email) VALUES ('User 1', 'user1@example.com')")
cursor.execute("INSERT INTO Users (Name, Email) VALUES ('User 2', 'user2@example.com')")
cursor.execute("INSERT INTO Users (Name, Email) VALUES ('User 3', 'user3@example.com')")

# Add sample data to the Reservations table
cursor.execute("INSERT INTO Reservations (BookID, UserID, ReservationDate) VALUES (1, 1, '2023-09-30')")
cursor.execute("INSERT INTO Reservations (BookID, UserID, ReservationDate) VALUES (3, 3, '2023-09-28')")

# Commit the changes and close the connection
conn.commit()
conn.close()