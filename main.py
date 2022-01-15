import sqlite3
import hashlib
from tkinter import *

# Database Code
with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vaultkey(
    id INTEGER PRIMARY KEY,
    v_key TEXT NOT NULL);             
""")


# Create Window
window = Tk()

window.title("Password Vault")

def hashVaultKey(input):
    """This function will hash the Vault Key that the user enters."""
    hash = hashlib.md5(input)
    hash = hash.hexdigest()
    
    return hash


def firstLogin():
    """This Function will only run when in first use.  This will allow the user to create their master password"""
    # Create the Login Screen
    window.geometry('250x150')
    
    lbl = Label(window, text="Create Vault Key")
    lbl.config(anchor=CENTER)
    lbl.pack()

    # Create Entry Box
    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()
    
    # Create Message for password confirmation
    message =  Label(window, text="Re-Enter Vault Key")
    message.pack()

    # Create second entry box
    txt2 = Entry(window, width=20, show="*")
    txt2.pack()
    txt2.focus()
    
    # Create Status Message
    message = Label(window)
    message.pack()

    def saveKey():
        if txt.get() == txt2.get():
            
            # Create the hashed version of the Vault Key
            hashedKey = hashVaultKey(txt.get().encode('utf-8'))
            
            insert_key = """INSERT INTO vaultkey(v_key)
            VALUES(?) """
            cursor.execute(insert_key, [(hashedKey)])
            db.commit()
            
            passwordVault()
        else:
            message.config(text="Keys do not match")
    
    # Create Submit Button
    btn = Button(window, text='Submit', command=saveKey)
    btn.pack(pady=10)
    
    
    
def loginScreen():
    """This Function will create the login screen of the vault"""
    # Create the Login Screen
    window.geometry('250x100')
    
    lbl = Label(window, text="Enter Vault Key")
    lbl.config(anchor=CENTER)
    lbl.pack()

    # Create Entry Box
    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()
    
    # Create Message for password entry
    message =  Label(window)
    message.pack()
    
    def getVaultKey():
        # Check if hashes match
        checkHashedKey = hashVaultKey(txt.get().encode('utf-8'))
        
        cursor.execute("SELECT * FROM vaultkey WHERE id = 1 AND v_key = ?", [(checkHashedKey)])
        
        # Test if hashing is working. Comment out Later
        print(checkHashedKey)
        
        return cursor.fetchall()
    
    def checkPassword():
        """This function will check if the password is correct"""
        
        match = getVaultKey()
        
        print(match)
        
        
        if match:
            passwordVault()
        else:
            txt.delete(0, 'end')
            message.config(text="Wrong Key")
    
    # Create Login Button
    btn = Button(window, text='Login', command=checkPassword)
    btn.pack(pady=10)
    
def passwordVault():
    """This function will be the actual password vault"""
    # Destroy Previous Window
    for widget in window.winfo_children():
        widget.destroy()
    
    # Create New window
    window.geometry('700x350')
    lbl = Label(window, text="Password Vault")
    lbl.config(anchor=CENTER)
    lbl.pack()
    
    
        
cursor.execute("SELECT * FROM vaultkey")
if cursor.fetchall():
    loginScreen()
else:
    firstLogin()              
window.mainloop()