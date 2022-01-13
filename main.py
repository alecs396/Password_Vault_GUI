import sqlite3
import hashlib
from tkinter import *

window = Tk()

window.title("Password Vault")

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
            pass
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
    
    def checkPassword():
        """This function will check if the password is correct"""
        
        password = "test"
        
        if password == txt.get():
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
    
    
        
firstLogin()
window.mainloop()