# Wordman
**Password Manager**  
Using Python, tkinter, and SQLite3  
<br>

**Update:** Included master password feature to prevent unauthorized use.  
        Current Password = skynet  
        Note: Actual database is still accessible to those who know where it is.  
<br>  

**What it does:**  
Saves usernames and passwords to a database.  
<br>

**To use:**  
1. Fill in the fields provided (account, username, password).  
2. `Add Entry` to add entry to database.  
3. `View List` to view entries.  
4. `Clear Fields` will clear input fields only (will not effect database).  
5. To Delete an entry, enter ID# and click `Delete Entry`.  
6. To Edit an entry, enter ID# and click `Edit Entry`.  

ID#'s are the last number of each entry.  

After an `Added` or `Deleted` entry,  
the View List button must be clicked to see changes.  
Think of it as a Refresh button.  
<br>

Notes:   
`View List` will show a partial list in UI itself (20+ entries).  
All entries will still be saved/stored in database.  


There is no encryption on this program so shouldn't be used at work, school,   
but should be fine for personal at home use.  

