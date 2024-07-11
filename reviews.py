import sqlite3

connection = sqlite3.connect('res/reviews.db', check_same_thread=False)
cursor = connection.cursor()


# Function to create the review table if it doesn't exist
def create_review_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        company TEXT,
        comment TEXT,
        score INTEGER
    )""")
    connection.commit()
    print("Review Table Created")


# Function to insert a new review into the database
def insert_review(user,company, comment, score):
    # Retrieve the latest user count from the database
    cursor.execute("SELECT COUNT(DISTINCT user) FROM reviews")
    latest_user_count = cursor.fetchone()[0]

    # Generate the user identifier with the format "UserX"
    user = f"User{latest_user_count + 1}"

    # Insert the new review into the database
    cursor.execute("INSERT INTO reviews (user, company, comment, score) VALUES (?, ?, ?, ?)",
                   (user, company, comment, score))
    connection.commit()
    print("New Review Inserted")


# Create the review table if it doesn't exist
create_review_table()
