import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

# Function to add a new expense
def add_expense():
    date = date_entry.get()
    description = description_entry.get()
    category = category_combobox.get()
    price = price_entry.get()

    if date and description and category and price:
        try:
            cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)",
                        (date, description, category, price))
            conn.commit()
            messagebox.showinfo("Success", "Expense added successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

# Function to view expenses summary
def view_summary():
    view_choice = view_combobox.get()
    if view_choice == "View all expenses":
        cur.execute("SELECT * FROM expenses")
        expenses = cur.fetchall()
        for expense in expenses:
            print(expense)
    elif view_choice == "View monthly expenses by category":
        month = month_entry.get()
        year = year_entry.get()
        if month and year:
            try:
                cur.execute("""SELECT category, SUM(price) FROM expenses
                               WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                               GROUP BY category""", (month, year))
                expenses = cur.fetchall()
                for expense in expenses:
                    print(f"Category: {expense[0]}, Total: {expense[1]}")
            except sqlite3.Error as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please enter both month and year.")

# Connects to database
conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

# Create GUI
root = tk.Tk()
root.title("Expense Manager")

# Add expense frame
add_frame = ttk.LabelFrame(root, text="Add Expense")
add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

ttk.Label(add_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
date_entry = ttk.Entry(add_frame)
date_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(add_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
description_entry = ttk.Entry(add_frame)
description_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(add_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5)
category_combobox = ttk.Combobox(add_frame, values=["Food", "Transportation", "Shopping", "Bills", "Others"])
category_combobox.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(add_frame, text="Price:").grid(row=3, column=0, padx=5, pady=5)
price_entry = ttk.Entry(add_frame)
price_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = ttk.Button(add_frame, text="Add Expense", command=add_expense)
add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# View summary frame
view_frame = ttk.LabelFrame(root, text="View Expenses Summary")
view_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

ttk.Label(view_frame, text="View Option:").grid(row=0, column=0, padx=5, pady=5)
view_combobox = ttk.Combobox(view_frame, values=["View all expenses", "View monthly expenses by category"])
view_combobox.grid(row=0, column=1, padx=5, pady=5)

view_button = ttk.Button(view_frame, text="View Summary", command=view_summary)
view_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# If you want to add functionality to view monthly expenses by category, you can add entry fields for month and year in the view_frame

root.mainloop()

