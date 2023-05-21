#!/usr/bin/env python3
# Password Manager

import tkinter as tk
import sqlite3

root = tk.Tk()
root.title("Wordman")
root.geometry("520x660")
root.config(padx=4, pady=4)

# TopFrame
topframe = tk.Frame(root)
topframe.grid(padx=0, pady=0, sticky='w')

# Create database or connect to one
conn = sqlite3.connect('wordman.db')

# cursor
c = conn.cursor()

# Create table
c.execute("""CREATE TABLE IF NOT EXISTS words (
        Account text,
        Username text,
        Password text
        )""")

# Update Entry Function
def update():
    # Create database or connect to one
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
    win_label = tk.Label(editor, text="Update complete.", anchor='w', fg='#555555')
    win_label.grid(column=1, row=5, padx=0, pady=(10,4), sticky='w')

    # Commit/close changes
    conn.commit()
    conn.close()

# For close window button in editor
def closewin():
    editor.destroy()


# Editor Window
def edit():
    global editor 
    editor = tk.Tk()
    editor.title("Editor")
    editor.geometry("520x214")
    editor.config(padx=4, pady=4)

    # Create database or connect to one
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()

    # Select oid# from database
    entry_id = select_box.get()
    c.execute("SELECT * FROM words WHERE oid = " + entry_id)
    entries = c.fetchall()

    # Editor window label
    win_label = tk.Label(editor, text="Entry #" + (entry_id), anchor='w', fg='#555555')
    win_label.grid(column=1, row=0, padx=0, pady=(10,4), sticky='w')

    # Entry box labels
    a_name_label = tk.Label(editor, text="Account:", anchor='w')
    a_name_label.grid(column=0, row=1, padx=4, pady=2, sticky='w')
    u_name_label = tk.Label(editor, text="Username:", anchor='w')
    u_name_label.grid(column=0, row=2, padx=4, pady=2, sticky='w')
    p_word_label = tk.Label(editor, text="Password:", anchor='w')
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
    update_btn = tk.Button(editor, text="Update", command=update)
    update_btn.grid(column=1, row=4, padx=0, pady=4, ipadx=2, sticky='w')

    # Close editor window button
    close_btn = tk.Button(editor, text="Close", command=lambda:[view(), closewin()])
    close_btn.grid(column=1, row=4, padx=0, pady=4, ipadx=6, sticky='e')


# Delete entry by oid#
def delete():
    # Create database or connect to one
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()
    
    # Delete entry*
    c.execute("DELETE from words WHERE oid=" + select_box.get())
      
    # Commit/close
    conn.commit()
    conn.close()

# Add Entry Function
def add():
    # Create database or connect to one
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()

    # Insert into table
    c.execute("INSERT INTO words VALUES (:a_name, :u_name, :p_word)",
            {
                'a_name': a_name.get(),
                'u_name': u_name.get(),
                'p_word': p_word.get()
            })

    # Commit/close
    conn.commit()
    conn.close()

# Clear entry boxes
def clear():
    a_name.delete(0, 'end')
    u_name.delete(0, 'end')
    p_word.delete(0, 'end')
    a_name.focus_set()


# View function
def view():
    # Create database or connect to one
    global view_label
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()

    # View the database, oid = id#
    c.execute("SELECT *, oid FROM words")
    entries = c.fetchall()
    #print(entries)

    # Loop thru results
    print_entries = ''
    for entry in entries:
        print_entries += str(entry).replace("'", "").replace("(", "").replace(")", "") + "\n"

    view_label = tk.Label(root, text=print_entries, justify='left')
    view_label.config(text=print_entries, pady=0)
    view_label.grid(column=0, row=7, padx=(82,0), pady=(15,0), sticky='nw')
        
    # Commit/close
    conn.commit()
    conn.close()

def hide():
    view_label.destroy()
    #print_entries = []


# GUI    
# Title/Side label
a_title = tk.Label(topframe, text="Password Manager", font='Arial 10 bold', fg='#555555')
a_title.grid(column=1, row=0, padx=2, pady=4)
entries = tk.Label(root, text="Entries:", anchor='w')
entries.grid(column=0, row=7, padx=4, pady=(15,0), sticky='nw')

# Entry box labels
a_name_label = tk.Label(topframe, text="Account:", anchor='w')
a_name_label.grid(column=0, row=1, padx=4, pady=2, sticky='w')
u_name_label = tk.Label(topframe, text="Username:", anchor='w')
u_name_label.grid(column=0, row=2, padx=4, pady=2, sticky='w')
p_word_label = tk.Label(topframe, text="Password:", anchor='w')
p_word_label.grid(column=0, row=3, padx=4, pady=2, sticky='w')
select_box_lab = tk.Label(topframe, text="Select ID#", anchor='e')
select_box_lab.grid(column=1, row=5, padx=(50,0), pady=2)

# Entry boxes
a_name = tk.Entry(topframe, width=40)
a_name.grid(column=1, row=1, pady=2, sticky='w')
u_name = tk.Entry(topframe, width=40)
u_name.grid(column=1, row=2, pady=2, sticky='w')
p_word = tk.Entry(topframe, width=40)
p_word.grid(column=1, row=3, pady=2, sticky='w')
select_box = tk.Entry(topframe, width=9, font=("arial", 14))
select_box.grid(column=1, row=5, pady=2, sticky='e', ipadx=2)


# Add button
add_btn = tk.Button(topframe, text="Add Entry", command=add, width='9')
add_btn.grid(column=1, row=4, padx=0, pady=4, sticky='w')

# Clear button
clear_btn = tk.Button(topframe, text="Clear", command=clear, width='9')
clear_btn.grid(column=1, row=4, padx=0, pady=4, sticky='e')

# View button
view_btn = tk.Button(topframe, text="View List", command=view, width='9')
view_btn.grid(column=1, row=5, padx=0, pady=4, sticky='w')

# Delete button
delete_btn = tk.Button(topframe, text="Delete", command=delete, width='9')
delete_btn.grid(column=1, row=6, padx=0, pady=4, sticky='e')

# Edit button
edit_btn = tk.Button(topframe, text="Edit Entry", command=lambda:[hide(), edit()], width='9')
edit_btn.grid(column=1, row=6, padx=0, pady=4, sticky='w')


conn.commit()
conn.close()

root.mainloop()
