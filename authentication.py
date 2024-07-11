import sqlite3

connection = sqlite3.connect('res/database.db', check_same_thread=False)
cursor = connection.cursor()


#Table creation
def create_table(table_name):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
        fullname TEXT,
        email TEXT,
        username TEXT,
        password TEXT
    )""")
    connection.commit()
    print("Table Created")




def insert_data(list):
    cursor.execute("INSERT INTO userbase VALUES(?,?,?,?)",list)
    connection.commit()
    print("New Entry Done")

def search(username,password):
    cursor.execute(f"SELECT fullname from userbase where username='{username}' and password='{password}'")
    connection.commit()
    return cursor.fetchall()

def getall():
    cursor.execute(f"SELECT * from userbase")
    connection.commit()
    return cursor.fetchall()

def account_creation(data):
    insert_data(data)

def login_acc(username,password):
    fullname = search(username , password)
    if len(fullname) >= 1:
        return fullname

