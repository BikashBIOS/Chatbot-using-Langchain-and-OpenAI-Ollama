import sqlite3

## connect to sqllite
connection = sqlite3.connect('student.db')

## create a cursor object
cursor = connection.cursor()

## create a table
table_info = """
create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)
"""

cursor.execute(table_info)

## insert data into the table
cursor.execute('''insert into STUDENT values('John', '10th', 'A', 85)''')
cursor.execute('''insert into STUDENT values('Alice', '10th', 'B', 90)''')
cursor.execute('''insert into STUDENT values('Bob', '10th', 'A', 78)''')
cursor.execute('''insert into STUDENT values('Eve', '10th', 'B', 92)''')
cursor.execute('''insert into STUDENT values('Bikash', '10th', 'A', 88)''')


## Display
print("The inserted data is:")
data = cursor.execute('''select * from STUDENT''')
for row in data:
    print(row)

## commit the changes
connection.commit()
connection.close()
