import sqlite3
import hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial

# Database Code
with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

# Create database to manage the vault key
cursor.execute("""
CREATE TABLE IF NOT EXISTS vaultkey(
    id INTEGER PRIMARY KEY,
    v_key TEXT NOT NULL);             
""")

# Create the vault database
cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
    id INTEGER PRIMARY KEY,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL);             
""")

# Create popup
def popUp(text):
    answer = simpledialog.askstring("input string", text)
    
    return answer

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
        
        # Test if hashing is working. Comment out
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
    
    def addEntry():
        text1 = "Website"
        text2 = "Username"
        text3 =  "E-Mail"
        text4 = "Password"
        
        website = popUp(text1)
        username = popUp(text2)
        email = popUp(text3)
        password = popUp(text4)
        
        insert_fields = """INSERT INTO vault(website, username, email, password)
        VALUES(?,?,?,?)"""
        
        cursor.execute(insert_fields, (website, username, email, password))
        db.commit()
        
        passwordVault()
        
    
    
    # Create New window
    window.geometry('700x350')
    
    lbl = Label(window, text="Password Vault")
    lbl.grid(column=1)
    
    btn = Button(window, text="+", command=addEntry)
    btn.grid(column=1, pady=10)
        
cursor.execute("SELECT * FROM vaultkey")
if cursor.fetchall():
    loginScreen()
else:
    firstLogin()              
window.mainloop()