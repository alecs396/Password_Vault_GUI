import random
# This program will randomly generate a password based on how many charachters the user wants it to be.

def generate_pass():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+1234567890"

    length = input('Length of Password:')
    length = int(length)

    password = ""

    for c in range(length):
        password += random.choice(chars)


    print("Your new password: " + password)