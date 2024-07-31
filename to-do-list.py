# todo_list.py

import sqlite3
from sqlite3 import Error

# Connect to SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("todo_list.db")
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

# Create table
def create_table(conn):
    sql = """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            );"""
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

# Create a new task
def create_task(conn, task):
    sql = """INSERT INTO tasks (task) VALUES (?)"""
    try:
        c = conn.cursor()
        c.execute(sql, (task,))
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(e)

# Read all tasks
def read_tasks(conn):
    sql = """SELECT * FROM tasks"""
    try:
        c = conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        for row in rows:
            print(f"{row[0]} - {row[1]} - {'Done' if row[2] else 'Not Done'}")
    except Error as e:
        print(e)

# Update a task
def update_task(conn, id, task):
    sql = """UPDATE tasks SET task = ? WHERE id = ?"""
    try:
        c = conn.cursor()
        c.execute(sql, (task, id))
        conn.commit()
    except Error as e:
        print(e)

# Delete a task
def delete_task(conn, id):
    sql = """DELETE FROM tasks WHERE id = ?"""
    try:
        c = conn.cursor()
        c.execute(sql, (id,))
        conn.commit()
    except Error as e:
        print(e)

# Main function
def main():
    conn = create_connection()
    create_table(conn)
    
    while True:
        print("\n1. Create Task")
        print("2. Read Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Quit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            task = input("Enter a task: ")
            create_task(conn, task)
        elif choice == "2":
            read_tasks(conn)
        elif choice == "3":
            id = int(input("Enter task ID: "))
            task = input("Enter new task: ")
            update_task(conn, id, task)
        elif choice == "4":
            id = int(input("Enter task ID: "))
            delete_task(conn, id)
        elif choice == "5":
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()