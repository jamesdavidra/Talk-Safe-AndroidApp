import sqlite3

# Create your own database
connection = sqlite3.connect('#Put your database here')
c = connection.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS Keyword(
                            key_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                            pass_key CHAR(255) NOT NULL);""")

connection.commit()

c.execute("""CREATE TABLE IF NOT EXISTS Contact(
                            contact_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                            full_name CHAR(255) NOT NULL,
                            email CHAR(255) UNIQUE,
                            contact_number CHAR(255) UNIQUE);""")

connection.commit()
