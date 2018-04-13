import sqlite3 as SQL

connection = SQL.connect("LoginPage.db")
cursor = connection.cursor()

def create_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS UserDetails ('PhoneNumber' INTEGER, Name TEXT, Password TEXT, AccountType TEXT)")

def data_entry():
	cursor.execute("INSERT INTO UserDetails VALUES (9876543210, 'Abc Def', 'xyz', 'Private')")
	connection.commit()

create_table()
data_entry()

cursor.close()
connection.close()