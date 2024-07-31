# todo_list_gui.py

import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("todo_list.db")
        print(sqlite3.version)
    except sqlite3.Error as e:
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
    except sqlite3.Error as e:
        print(e)

# Create a new task
def create_task(conn, task):
    sql = """INSERT INTO tasks (task) VALUES (?)"""
    try:
        c = conn.cursor()
        c.execute(sql, (task,))
        conn.commit()
        return c.lastrowid
    except sqlite3.Error as e:
        print(e)

# Read all tasks
def read_tasks(conn):
    sql = """SELECT * FROM tasks"""
    try:
        c = conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        return rows
    except sqlite3.Error as e:
        print(e)

# Update a task
def update_task(conn, id, task):
    sql = """UPDATE tasks SET task = ? WHERE id = ?"""
    try:
        c = conn.cursor()
        c.execute(sql, (task, id))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Delete a task
def delete_task(conn, id):
    sql = """DELETE FROM tasks WHERE id = ?"""
    try:
        c = conn.cursor()
        c.execute(sql, (id,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# GUI class
class TodoListGUI:
    def __init__(self, root):
        self.root = root
        self.conn = create_connection()
        create_table(self.conn)
        self.tasks = read_tasks(self.conn)
        self.task_list = tk.Listbox(self.root, width=40)
        self.task_list.pack(padx=10, pady=10)
        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(padx=10, pady=10)
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(padx=10, pady=10)
        self.update_button = tk.Button(self.root, text="Update Task", command=self.update_task)
        self.update_button.pack(padx=10, pady=10)
        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(padx=10, pady=10)
        self.refresh_list()

    def refresh_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            self.task_list.insert(tk.END, f"{task[0]} - {task[1]} - {'Done' if task[2] else 'Not Done'}")

    def add_task(self):
        task = self.entry.get()
        if task:
            create_task(self.conn, task)
            self.tasks = read_tasks(self.conn)
            self.refresh_list()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a task")

    def update_task(self):
        try:
            id = int(self.task_list.curselection()[0])
            task = self.entry.get()
            if task:
                update_task(self.conn, id, task)
                self.tasks = read_tasks(self.conn)
                self.refresh_list()
                self.entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Please enter a task")
        except IndexError:
            messagebox.showerror("Error", "Please select a task to update")

    def delete_task(self):
        try:
            id = int(self.task_list.curselection()[0])
            delete_task(self.conn, id)
            self.tasks = read_tasks(self.conn)
            self.refresh_list()
        except IndexError:
            messagebox.showerror("Error", "Please select a task to delete")

# Main function
def main():
    root = tk.Tk()
    root.title("To-Do List")
    todo_list_gui = TodoListGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()