from cgitb import text
from email import charset
from operator import length_hint
import sqlite3
import hashlib
import random
from tkinter import *
from tkinter import simpledialog
from functools import partial
from turtle import window_width

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


# Create Password Generator
def passwordGenerator():
    """This Function allows user to generate a password of 20 character length.  The text will then be displayed next to the button."""
    
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+1234567890"
    
    newPassword = ""
    
    for c in range(20):
        newPassword += random.choice(chars)
    
    passLabel = Label(window, text=newPassword)
    passLabel.grid(column=4, row=1)
    return newPassword


    

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
        """This function allows the user to add an entry into the vault by providing information through the popUp window function. Entries are then saved to the vault database."""
        
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
        
    def removeEntry(input):
        """This function allows the user to remove an entry in their vault."""
        
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()
        
        passwordVault()
    
    # Create New window
    window.geometry('850x425')
    lbl = Label(window, text="Password Vault")
    lbl.grid(column=1)
    
    
    # Create button to generate password
    passbutton = Button(window, text="Generate New Password", command=passwordGenerator)
    passbutton.grid(column=3, row=1, pady=10)
    # getnewPass = passwordGenerator()
    # newPass= Label(window, text=passwordGenerator())
    # newPass.grid(column=4, row=1, padx=80)
    
    # Create button to add entries to database
    btn = Button(window, text="Add Entry", command=addEntry)
    btn.grid(column=1, row=1, pady=10)
    
    # Display labels for entries
    lbl = Label(window, text="Website")
    lbl.grid(row=2, column=0, padx = 80)
    lbl = Label(window, text="Username")
    lbl.grid(row=2, column=1, padx = 80)
    lbl = Label(window, text="E-Mail")
    lbl.grid(row=2, column=2, padx = 80)
    lbl = Label(window, text="Password")
    lbl.grid(row=2, column=3, padx = 80)
    
    
    # Display entries from database
    cursor.execute("SELECT * FROM vault")
    if (cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()
            
            lbl1 = Label(window, text=(array[i][1]), font=("Calibri", 12))
            lbl1.grid(column=0, row=i+3)
            lbl1 = Label(window, text=(array[i][2]), font=("Calibri", 12))
            lbl1.grid(column=1, row=i+3)
            lbl1 = Label(window, text=(array[i][3]), font=("Calibri", 12))
            lbl1.grid(column=2, row=i+3)
            lbl1 = Label(window, text=(array[i][4]), font=("Calibri", 12))
            lbl1.grid(column=3, row=i+3)

            # Create the delete button
            btn = Button(window, text="Delete", command= partial(removeEntry, array[i][0]))
            btn.grid(column=4, row=i+3, pady=10)
            
            i = i+1
            
            cursor.execute("SELECT * FROM vault")
            if (len(cursor.fetchall()) <= i):
                break
        
cursor.execute("SELECT * FROM vaultkey")
if cursor.fetchall():
    loginScreen()
else:
    firstLogin()              
window.mainloop()