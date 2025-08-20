import mysql.connector
from tabulate import tabulate

conn = mysql.connector.connect(
    host ="localhost",
    user="root",
    password="12345",
    database = "tracker"
)

cursor = conn.cursor()

# cursor.execute('''
#                create table books(book_id int auto_increment primary key,
#                title varchar(100),
#                author varchar(100),
#                total_pages int)
#                ''')

# cursor.execute('''
#                create table reading_progress(progress_id int auto_increment primary key,
#                book_id int,
#                current_page int,
#                status ENUM('Not Started', 'In Progress', 'Completed') DEFAULT 'Not Started',
#                FOREIGN KEY(book_id) REFERENCES books(book_id))
#                ''')

# data = [
#     ("IKIGAI","Hector Garcia",280),
#     ("Mindset","Dr. Carol S Deck",300),
#     ("4 Hour Workweek","Timothy Ferriss",350),
#     ("SHOE DOG","Phil Knight",290),
#     ("The Secret","Rhonda Bryne",310),
#     ("Sneham Kaamam braanth","Joseph Annamkutty Jose",180)
# ]

# data = [
#     (7,35,"In Progress"),
#     (8,300,"Completed"),
#     (9,150,"In Progress"),
#     (10,290,"Completed"),
#     (11,0,"Not Started"),
#     (12,0,"Not Started")        
# ]
# cursor.executemany(
#      "insert into reading_progress(book_id,current_page,status) VALUES(%s,%s,%s)", data)
# conn.commit()


####### 1 - To add a new book
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    total_pages = int(input("Enter total pages: "))

    cursor.execute(
        "insert into books(title,author,total_pages) VALUES(%s,%s,%s)", 
        (title,author,total_pages)  
    )
    conn.commit()
    print("✅ Book added successfully!")



###### 2 - Display all books and its progress
# def view_books():
#     cursor.execute('''
#                select b.book_id,b.title,b.author,r.status,r.current_page,b.total_pages from books b left join reading_progress r on b.book_id = r.book_id
#                ''')
#     rows = cursor.fetchall()
#     print("\n📚 Books List:")
#     for row in rows:
#         print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Status: {row[3]}, Page: {row[4]}/{row[5]}")
#     print()

def view_books():
    cursor.execute('''
        SELECT b.book_id, b.title, b.author, 
               COALESCE(r.status, 'Not Started') AS status, 
               COALESCE(r.current_page, 0) AS current_page, 
               b.total_pages 
        FROM books b 
        LEFT JOIN reading_progress r 
        ON b.book_id = r.book_id
    ''')
    rows = cursor.fetchall()

    if not rows:
        print("\n📚 No books found!\n")
        return

    headers = ["ID", "Title", "Author", "Status", "Page Progress"]
    table_data = [
        [row[0], row[1], row[2], row[3], f"{row[4]}/{row[5]}"] for row in rows
    ]

    print("\n📚 Books List:\n")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()


###### 3 - To Update reading progress
def update_progress():
    book_id = int(input("Enter the book ID: "))
    current_page = int(input("Enter the current page: "))
    status = input("Enter the status (Not Started/In Progress/Completed): ")

    cursor.execute(
        "UPDATE reading_progress SET current_page=%s, status=%s Where book_id=%s",
        (current_page,status,book_id)
    )    
    conn.commit()
    print("✅ Progress updated successfully!")


##### 3 - View books Completed list
def view_completed():
    cursor.execute('''
                select b.title from books b join reading_progress r on r.book_id = b.book_id where r.status = 'Completed'
                ''')
    completed_books = cursor.fetchall()
    print("Completed Books: \n")
    for book in completed_books:
        print("-", book[0])
    print()    

def delete_book():
    t = input("Enter the book title you need to delete: ")
    cursor.execute("SELECT * FROM books WHERE title = %s", (t,))
    book = cursor.fetchone()

    if book:
        cursor.execute("DELETE FROM books WHERE title = %s", (t,))
        conn.commit()
        print(f"\nBook '{t}' deleted successfully!")
    else:
        print(f"\nNo book found with title '{t}'.")


exit = 1    
while exit:
    print("\n===== 📖 Book Tracker Menu =====")
    print("\t\t\t1. Add a new book\n\t\t\t2. To view all books and its progress\n\t\t\t3. Update reading progress\n\t\t\t4. To View completed books\n\t\t\t5. To delete any book ")
    
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        add_book()
    elif choice == 2:
        view_books()  
    elif choice == 3:
        update_progress()
    elif choice == 4:
        view_completed()
    elif choice == 5:
        delete_book()
    else:        
        exit = 0       