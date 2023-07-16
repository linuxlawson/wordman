# Wordman
**Password Manager**  
Using Python, tkinter, and SQLite3  
<br>
Master Password: blank

**What it does:**  
Saves/stores your account names, usernames, and passwords to a database  
(in case they are forgotten).
<br>

**To use:**  
1. Fill in the fields provided (account, username, password).  
2. `Add Entry` to add entry to database.  
3. `View List` to view entries.  
4. `Clear Fields` will clear input fields only (will not effect database).  
5. To Delete an entry, enter ID# and click `Delete Entry`.  
6. To Edit an entry, enter ID# and click `Edit Entry`.  

ID#'s are the last number of each entry.  
View List button must be used after adding/deleting entries (to see updates).

<br>  

**Added:**  
- Master password window to prevent unauthorized use  (default password: blank).  
- Option to save as csv file.
- View List button is now toggle-able, and must be used after adding/deleting entries.

<br>

**Notes:**     
**`View List`** will show only a partial list of entries in UI (20+ entries).  
All entries will still be saved/stored in database.  


There is no encryption on this program so shouldn't be used at work, school,   
but should be fine for personal at home use.  

