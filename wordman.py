#!/usr/bin/env python3
# Password Manager

import tkinter as tk
import sqlite3

root = tk.Tk()
root.title("Wordman")
root.geometry("510x660")
root.config(padx=4, pady=4)

# TopFrame
topframe = tk.Frame(root)
topframe.grid(padx=0, pady=0, sticky='w')

# Create database or connect to one
conn = sqlite3.connect('wordman.db')
c = conn.cursor()

# Create table
c.execute("""CREATE TABLE IF NOT EXISTS words (
        Account text,
        Username text,
        Password text
        )""")

# Update Entry Function
def update():
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()

    entry_id = select_box.get()

    c.execute("""UPDATE words SET
        Account = :acc,
        Username = :user,
        Password = :pword

        WHERE oid = :oid""",
        {
        'acc': a_name_ed.get(),
        'user': u_name_ed.get(),
        'pword': p_word_ed.get(),
        'oid': entry_id
        })

    # Message in editor window
    win_label = tk.Label(editor, text="Update complete.", fg="#555555")
    win_label.grid(column=1, row=5, padx=0, pady=(10,4), sticky='w')

    conn.commit()
    conn.close()


# close editor window
def closewin():
    editor.destroy()

# close emptyID window
def closeid():
    emp.destroy()

def empty_idwin():
    global emp 
    emp = tk.Tk()
    emp.title("Empty ID#")
    emp.geometry("200x120")
    emp.config(padx=4, pady=4)

# Empty ID# message
    emp_label = tk.Label(emp, text="\nMust Provide ID#", fg="#555555")
    emp_label.grid(column=0, row=0, padx=34, pady=6)
    emp_btn = tk.Button(emp, text="Ok", command=closeid)
    emp_btn.grid(column=0, row=1, padx=34, pady=6)


def hide():
    view_label.destroy()

# Editor Window
def edit():
    # for empty ID# entry box
    if select_box.index("end") == 0:
        print("Must provide ID#")
        view()
        empty_idwin()
        select_box.focus_set()
    else:
        global editor 
        editor = tk.Tk()
        editor.title("Editor")
        editor.geometry("510x214")
        editor.config(padx=4, pady=4)

    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()
    try:
    # Select oid# from database
        entry_id = select_box.get()
        c.execute("SELECT * FROM words WHERE oid=" + entry_id)
        entries = c.fetchall()
    except sqlite3.OperationalError:
        # escape input error
        return

    # Editor label
    win_label = tk.Label(editor, text="Entry #" + (entry_id), fg="#555555")
    win_label.grid(column=1, row=0, padx=0, pady=(10,4), sticky='w')

    # Entry box labels
    a_name_label = tk.Label(editor, text="Account:")
    a_name_label.grid(column=0, row=1, padx=4, pady=2, sticky='w')
    u_name_label = tk.Label(editor, text="Username:")
    u_name_label.grid(column=0, row=2, padx=4, pady=2, sticky='w')
    p_word_label = tk.Label(editor, text="Password:")
    p_word_label.grid(column=0, row=3, padx=4, pady=2, sticky='w')

    # Global variables for Entry Box names
    global a_name_ed
    global u_name_ed
    global p_word_ed

    # Entry boxes
    a_name_ed = tk.Entry(editor, width=40)
    a_name_ed.grid(column=1, row=1, pady=2)
    u_name_ed = tk.Entry(editor, width=40)
    u_name_ed.grid(column=1, row=2, pady=2)
    p_word_ed = tk.Entry(editor, width=40)
    p_word_ed.grid(column=1, row=3, pady=2)

    #loop thru results
    for entry in entries:
        a_name_ed.insert(0, entry[0])
        u_name_ed.insert(0, entry[1])
        p_word_ed.insert(0, entry[2])

    # Update entry button
    update_btn = tk.Button(editor, text="Update", command=lambda:[update(), hide()])
    update_btn.grid(column=1, row=4, padx=0, pady=4, ipadx=2, sticky='w')

    # Close editor button
    close_btn = tk.Button(editor, text="Close", command=lambda:[closewin(), view()])
    close_btn.grid(column=1, row=4, padx=0, pady=4, ipadx=6, sticky='e')


# Delete entry by id#
def delete():
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()

    # for empty ID# entry box
    if select_box.index("end") == 0:
        print("Must provide ID#")
        empty_idwin()
        select_box.focus_set()
    else:
        c.execute("DELETE FROM words WHERE oid=" + select_box.get()) 

    conn.commit()
    conn.close()


# Add Entry Function
def add():
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()

    # Insert into table
    c.execute("INSERT INTO words VALUES (:a_name, :u_name, :p_word)",
            {
            'a_name': a_name.get(),
            'u_name': u_name.get(),
            'p_word': p_word.get()
            })

    conn.commit()
    conn.close()

# Clear entry fields
def clear():
    a_name.delete(0, 'end')
    u_name.delete(0, 'end')
    p_word.delete(0, 'end')
    a_name.focus_set()


# View function
def view():
    global view_label
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()

    # View database
    c.execute("SELECT *, oid FROM words")
    entries = c.fetchall()

    # Loop thru results
    print_entries = ''
    for entry in entries:
        print_entries += str(entry).replace("'","").replace("(","").replace(")","") + "\n"

    view_label = tk.Label(root, text=print_entries, justify='left')
    view_label.config(text=print_entries, pady=0)
    view_label.grid(column=0, row=7, padx=(82,0), pady=(15,0), sticky='nw')

    conn.commit()
    conn.close()


# GUI
# Top/Side labels
a_title = tk.Label(topframe, text="Password Manager", font="Arial 10 bold", fg="#555555")
a_title.grid(column=1, row=0, padx=2, pady=4)
entries = tk.Label(root, text="Entries:")
entries.grid(column=0, row=7, padx=4, pady=(15,0), sticky='nw')

# Entry box labels
a_name_label = tk.Label(topframe, text="Account:")
a_name_label.grid(column=0, row=1, padx=4, pady=2, sticky='w')
u_name_label = tk.Label(topframe, text="Username:")
u_name_label.grid(column=0, row=2, padx=4, pady=2, sticky='w')
p_word_label = tk.Label(topframe, text="Password:")
p_word_label.grid(column=0, row=3, padx=4, pady=2, sticky='w')
select_box_lab = tk.Label(topframe, text="Select ID#")
select_box_lab.grid(column=1, row=5, padx=(50,0), pady=2)

# Entry boxes
a_name = tk.Entry(topframe, width=40)
a_name.grid(column=1, row=1, pady=2)
u_name = tk.Entry(topframe, width=40)
u_name.grid(column=1, row=2, pady=2)
p_word = tk.Entry(topframe, width=40)
p_word.grid(column=1, row=3, pady=2)
select_box = tk.Entry(topframe, width=9, font=("arial", 14))
select_box.grid(column=1, row=5, pady=2, sticky='e', ipadx=2)


# Add button
add_btn = tk.Button(topframe, text="Add Entry", command=add, width='9')
add_btn.grid(column=1, row=4, pady=4, sticky='w')

# Clear button
clear_btn = tk.Button(topframe, text="Clear Fields", command=clear, width='9')
clear_btn.grid(column=1, row=4, pady=4, sticky='e')

# View button
view_btn = tk.Button(topframe, text="View List", command=view, width='9')
view_btn.grid(column=1, row=5, pady=4, sticky='w')

# Delete button
delete_btn = tk.Button(topframe, text="Delete Entry", command=delete, width='9')
delete_btn.grid(column=1, row=6, pady=4, sticky='e')

# Edit button
edit_btn = tk.Button(topframe, text="Edit Entry", command=edit, width='9')
edit_btn.grid(column=1, row=6, pady=4, sticky='w')


conn.commit()
conn.close()

root.mainloop()
