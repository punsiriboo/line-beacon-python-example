import sqlite3

con = sqlite3.connect("line_user.db")
cur = con.cursor()  
cur.execute("DROP TABLE IF EXISTS line_user")
cur.execute("CREATE TABLE line_user(user_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, age INTEGER, gender TEXT, dob TEXT)")
data = [
    ('U1234567890abcdef1234567890abcdef', 'Jane', 'Doe', 30, 'Male', '1993-01-15'),
    ('Uabcdef1234567890abcdef1234567890', 'Jane', 'Doe', 25, 'Female', '1998-05-20'),
    ('U7890abcdef1234567890abcdef123456', 'Peter', 'Pan', 18, 'Male', '2005-11-10')
]
cur.executemany("INSERT INTO line_user VALUES(?, ?, ?, ?, ?, ?)", data)
con.commit()
