import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ---------------- DATABASE CONNECTION ----------------

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="campus_lost_found"
    )
    


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Campus Lost & Found Management System")
root.geometry("1100x700")
root.configure(bg="#edf2f7")

# ---------------- HEADING ----------------

heading = tk.Label(
    root,
    text="CAMPUS LOST & FOUND",
    font=("Arial", 25, "bold"),
    bg="#17365d",
    fg="white",
    pady=20
)
heading.pack(fill="x")

tk.Label(
    root,
    text="Campus Item Management Dashboard",
    font=("Arial", 13),
    bg="#edf2f7"
).pack(pady=10)

# ---------------- INPUT FORM ----------------

form = tk.Frame(root, bg="#edf2f7")
form.pack(pady=10)

tk.Label(form, text="Item Name", bg="#edf2f7").grid(
    row=0, column=0, padx=10, pady=8
)

name_entry = tk.Entry(form, width=25)
name_entry.grid(row=0, column=1, padx=10)

tk.Label(form, text="Type", bg="#edf2f7").grid(
    row=0, column=2, padx=10
)

type_box = ttk.Combobox(
    form,
    values=["Lost", "Found"],
    width=22,
    state="readonly"
)
type_box.grid(row=0, column=3, padx=10)
type_box.set("Lost")

tk.Label(form, text="Category", bg="#edf2f7").grid(
    row=1, column=0, padx=10, pady=8
)

category_entry = tk.Entry(form, width=25)
category_entry.grid(row=1, column=1, padx=10)

tk.Label(form, text="Location", bg="#edf2f7").grid(
    row=1, column=2, padx=10
)

location_entry = tk.Entry(form, width=25)
location_entry.grid(row=1, column=3, padx=10)

tk.Label(form, text="Reporter Name", bg="#edf2f7").grid(
    row=2, column=0, padx=10, pady=8
)

reporter_entry = tk.Entry(form, width=25)
reporter_entry.grid(row=2, column=1, padx=10)

tk.Label(form, text="Description", bg="#edf2f7").grid(
    row=2, column=2, padx=10
)

description_entry = tk.Entry(form, width=25)
description_entry.grid(row=2, column=3, padx=10)


# ---------------- DATABASE OPERATIONS ----------------

def report_item():
    name = name_entry.get().strip()
    item_type = type_box.get()
    category = category_entry.get().strip()
    location = location_entry.get().strip()
    reporter = reporter_entry.get().strip()
    description = description_entry.get().strip()

    if not name or not reporter:
        messagebox.showwarning(
            "Warning", "Enter item name and reporter name"
        )
        return

    con = None
    try:
        con = connect_db()
        cur = con.cursor()

        query = """
        INSERT INTO items
        (item_name, item_type, category, description,
         location, reporter)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            name, item_type, category,
            description, location, reporter
        )

        cur.execute(query, values)
        con.commit()

        messagebox.showinfo(
            "Success", "Item reported successfully!"
        )

        for entry in [
            name_entry, category_entry,
            location_entry, reporter_entry,
            description_entry
        ]:
            entry.delete(0, tk.END)

        refresh_items()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if con and con.is_connected():
            con.close()


def refresh_items():
    con = None
    try:
        con = connect_db()
        cur = con.cursor()

        cur.execute("SELECT * FROM items ORDER BY item_id DESC")
        rows = cur.fetchall()

        for row in table.get_children():
            table.delete(row)

        for row in rows:
            table.insert("", tk.END, values=row)

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if con and con.is_connected():
            con.close()


def search_items():
    keyword = search_entry.get().strip()

    con = None
    try:
        con = connect_db()
        cur = con.cursor()

        query = """
        SELECT * FROM items
        WHERE item_name LIKE %s
        OR category LIKE %s
        OR location LIKE %s
        ORDER BY item_id DESC
        """

        value = "%" + keyword + "%"
        cur.execute(query, (value, value, value))
        rows = cur.fetchall()

        for row in table.get_children():
            table.delete(row)

        for row in rows:
            table.insert("", tk.END, values=row)

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if con and con.is_connected():
            con.close()


def claim_item():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning", "Select an item first"
        )
        return

    item_id = table.item(selected[0])["values"][0]

    con = None
    try:
        con = connect_db()
        cur = con.cursor()

        cur.execute(
            "UPDATE items SET status='Claimed' WHERE item_id=%s",
            (item_id,)
        )

        con.commit()

        messagebox.showinfo(
            "Success", "Item marked as Claimed"
        )

        refresh_items()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if con and con.is_connected():
            con.close()


def delete_item():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning", "Select an item first"
        )
        return

    item_id = table.item(selected[0])["values"][0]

    if not messagebox.askyesno(
        "Confirm", "Delete this item?"
    ):
        return

    con = None
    try:
        con = connect_db()
        cur = con.cursor()

        cur.execute(
            "DELETE FROM items WHERE item_id=%s",
            (item_id,)
        )

        con.commit()

        messagebox.showinfo(
            "Success", "Item deleted successfully"
        )

        refresh_items()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if con and con.is_connected():
            con.close()


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(root, bg="#edf2f7")
button_frame.pack(pady=15)

def make_button(text, command, column):
    tk.Button(
        button_frame,
        text=text,
        command=command,
        width=17,
        height=2,
        bg="#2563a6",
        fg="white",
        font=("Arial", 10, "bold")
    ).grid(row=0, column=column, padx=6)


make_button("Report Item", report_item, 0)
make_button("View All Items", refresh_items, 1)
make_button("Claim Item", claim_item, 2)
make_button("Delete Item", delete_item, 3)


# ---------------- SEARCH ----------------

search_frame = tk.Frame(root, bg="#edf2f7")
search_frame.pack(pady=10)

tk.Label(
    search_frame,
    text="Search Item:",
    font=("Arial", 11, "bold"),
    bg="#edf2f7"
).pack(side="left", padx=5)

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_items,
    bg="#198754",
    fg="white",
    width=12
).pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="Show All",
    command=refresh_items,
    width=12
).pack(side="left", padx=5)


# ---------------- ITEMS TABLE ----------------

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=15, pady=10)

columns = (
    "ID", "Name", "Type", "Category",
    "Description", "Location", "Reporter",
    "Status", "Date"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=115, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

table.configure(yscrollcommand=scrollbar.set)

table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# ---------------- FOOTER ----------------

tk.Label(
    root,
    text="Developed using Python | Tkinter | MySQL",
    font=("Arial", 10),
    bg="#edf2f7",
    fg="#555555"
).pack(pady=8)


root.mainloop()