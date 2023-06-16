#!/usr/bin/env python3
# Password Manager

# Database = wordman.db
# Table name = words
# Password = skynet

import tkinter as tk
import sqlite3
import csv

root = tk.Tk()
root.title("Wordman")
root.geometry("510x660")
root.config(padx=4, pady=4)


# TopFrame
topframe = tk.Frame(root)
topframe.grid(sticky='w')

# Create database or connect to one
conn = sqlite3.connect('wordman.db')
c = conn.cursor()

# Create table
c.execute("""CREATE TABLE IF NOT EXISTS words (
        Account text,
        Username text,
        Password text
        )""")


# Update Entry
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
    update_label = tk.Label(editor, text="Update complete.", fg='#800000')
    update_label.grid(column=1, row=5, padx=0, pady=(10,4), sticky='w')
    conn.commit()
    conn.close()


# close emptyID window
def closeid():
    emp.destroy()

# EmptyID window
def empty_idwin():
    global emp 
    emp = tk.Tk()
    emp.title("Empty ID#")
    emp.geometry("200x120")
    emp.config(padx=4, pady=4)

# Empty ID# message
    emp_label = tk.Label(emp, text="\nMust Provide ID#")
    emp_label.grid(column=0, row=0, padx=34, pady=6)
    emp_btn = tk.Button(emp, text="Ok", command=closeid)
    emp_btn.grid(column=0, row=1, padx=34, pady=6)


# show/hide asterisks for mp
def show():
    if mp_ent.cget('show') == '':
        mp_ent.config(show='*')
    else:
        mp_ent.config(show='')

# Master password def
password = tk.StringVar()
def check(event=None):
    if password.get() == 'skynet':
        add_btn.config(state='normal')
        view_btn.config(state='normal')
        edit_btn.config(state='normal')
        select_box.config(state='normal')
        delete_btn.config(state='normal')
        clear_btn.config(state='normal')
        top.destroy()
    else:
        pw_lbl = tk.Label(top, text="Incorrect Password", fg='#800000')
        pw_lbl.grid(column=0, row=2, padx=34, pady=(10,0))
        top.after(1200, pw_lbl.destroy)


# Master password window
top = tk.Toplevel(root)
top.title("Master")
top.geometry('323x160+633+362')#size+position

mp_lab = tk.Label(top, text="Master Password:")
mp_lab.grid(column=0, row=0, padx=34, pady=(18,0), sticky='w')

mp_ent = tk.Entry(top, textvariable=password, show="*", width=30)
mp_ent.bind('<Return>', check)
mp_ent.focus_set()
mp_ent.grid(column=0, row=1, padx='36', pady=2)


ph_lbl = tk.Label(top, text=" ")
ph_lbl.grid(column=0, row=2, padx=34, pady=(10,0))

mp_btn = tk.Button(top, text="Enter", command=check)
mp_btn.bind('<Return>', check)
mp_btn.grid(column=0, row=3, padx=36, pady=(8,0))

show_chk = tk.Checkbutton(top, text='Show/Hide', command=show)
show_chk.grid(column=0, row=0, padx=34, pady=(18,0), sticky='e')
top.wm_transient(root)


# close editor window
def closedit():
    editor.destroy()
    view_label.destroy()

# Editor Window
def edit():
    # for empty ID# field
    if select_box.index("end") == 0:
        #print("Must provide ID#")
        select_box.focus_set()
        empty_idwin()
    else:
        global editor 
        editor = tk.Tk()
        editor.title("Editor")
        editor.geometry("510x214+544+118")
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

    # Editor id# label
    id_label = tk.Label(editor, text="Entry #" + (entry_id), fg='#800000')
    id_label.grid(column=1, row=0, padx=0, pady=(10,4), sticky='w')

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

    # Update edited entry button
    update_btn = tk.Button(editor, text="Update", command=lambda:[update()])
    update_btn.grid(column=1, row=4, padx=0, pady=4, ipadx=2, sticky='w')

    # Close editor button
    close_btn = tk.Button(editor, text="Close", command=lambda:[closedit(), view()])
    close_btn.grid(column=1, row=4, padx=0, pady=4, ipadx=6, sticky='e')


# Delete entry by id#
def delete():
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()

    # for empty ID# field
    if select_box.index("end") == 0:
        #print("Must provide ID#")
        select_box.focus_set()
        empty_idwin()
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
    view_label.config(text=print_entries)
    view_label.grid(column=0, row=7, padx=(82,0), pady=(15,0), sticky='nw')

    conn.commit()
    conn.close()

#help menu/about
def about_win(event=None):
    win = tk.Toplevel()
    win.title("About")
    about = tk.Label(win, text="""\nWordman\nPassword Manager
    \nCreated with Python/Tkinter and SQLite\n\n
    Saves account names, usernames,\nand passwords to database.
    List of entries can also be saved\nas a .csv file.""")
    about.pack()
    clo = tk.Button(win, text="Close", width=4, command=lambda: win.destroy())
    clo.pack(padx=8, pady=(16,0))
    win.transient(root)
    win.geometry('340x270+638+298')
    win.wait_window()

# Save as .csv file
def save_csv():
    csvWriter = csv.writer(open("words.csv", "w"))
    csvWriter.writerow(['Account', 'Username', 'Password'])
    conn = sqlite3.connect('wordman.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM words")
    entries = c.fetchall()
    csvWriter.writerows(entries)


# Top/Side labels
a_title = tk.Label(topframe, text="Password Manager", font="Arial 10 bold")
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
select_box = tk.Entry(topframe, width=9, font=("arial", 14), state='disabled')
select_box.grid(column=1, row=5, pady=2, sticky='e', ipadx=2)


# Add button
add_btn = tk.Button(topframe, text="Add Entry", width='9', state='disabled', command=lambda:[add(), view()])
add_btn.grid(column=1, row=4, pady=4, sticky='w')

# Clear button
clear_btn = tk.Button(topframe, text="Clear Fields", command=clear, width='9', state='disabled')
clear_btn.grid(column=1, row=4, pady=4, sticky='e')

# View button
view_btn = tk.Button(topframe, text="View List", command=view, width='9', state='disabled')
view_btn.grid(column=1, row=5, pady=4, sticky='w')

# Delete button
delete_btn = tk.Button(topframe, text="Delete Entry", width='9', state='disabled', command=lambda:[delete(), view()])
delete_btn.grid(column=1, row=6, pady=4, sticky='e')

# Edit button
edit_btn = tk.Button(topframe, text="Edit Entry", command=edit, width='9', state='disabled')
edit_btn.grid(column=1, row=6, pady=4, sticky='w')


# Menu Items
menu = tk.Menu(root, bd=1, relief='flat')
root.config(menu=menu, bd=2)

# File
filemenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File ", menu=filemenu)
filemenu.add_command(label="View List", command=view)
filemenu.add_command(label="Save as .csv", command=save_csv)
filemenu.add_command(label="Exit", command=lambda: root.destroy())

# Edit
editmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit ", menu=editmenu)
editmenu.add_command(label="Edit Entry", command=edit)
editmenu.add_command(label="Delete Entry", command=delete)

# Help
editmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help ", menu=editmenu)
editmenu.add_command(label="About", command=about_win)

conn.commit()
conn.close()

root.mainloop()
