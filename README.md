# wordman
Password Manager


To create and use this program  
I have installed on my system:
- Python 3  
- tkinter  
- DB Browser for SQLite (SQLite3)  

  

What it does:  
Saves username and passwords to a database.

database = wordman.db  

To use:  
1. Fill in the fields provided (account, username, password).  
2. `Add Entry` to add entry to database.  
3. `View List` to view entries.  
4. `Clear` to clear fields (will not effect database).  
5. To Delete an entry, enter ID# and click `Delete`.  
6. To Edit an entry, enter ID# and click `Edit Entry`.  

ID#'s are the last number of each entry.  

After every Added, Edited, or Deleted entry,  
the View List button must be clicked to see updates.  
Think of it as a Refresh button.  


Notes:   
View List will only show 20+ entries in app itself.  
All entries will still be saved/visible in database.  

There is a glitch in program where long entries (i.e.-passwords)  
when shortened, will leave left-over text in window.  
This will go away after closing/re-opening program.  

There is no encryption on this program so shouldn't be used at work, school,   
but should be fine for personal at home use.  

