import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

def callback(url):
    webbrowser.open_new(url)

# Set up root
root = tk.Tk()
root.title("Login Page")

# Setting up background colour and size
root.configure(bg="#C4DAD2")
root.geometry('1280x720')

# Create container for content
content = tk.Frame(root, bg="#C4DAD2")
content.pack(padx=20, pady=20)

# Create container for store logo
storeLogoFrame = tk.Frame(content, bg="#C4DAD2", borderwidth=1, relief='solid')
storeLogoFrame.pack(side="left", pady=10, padx=10, fill='x')

# Put store logo in container
storeLogoText = tk.Label(storeLogoFrame, text="ONLINE\nSTORE", font=("Lato", 32, "bold"), bg="#C4DAD2")
storeLogoText.pack(anchor="w")

# Create container for login form
loginFormFrame = tk.Frame(content, bg="#C4DAD2")
loginFormFrame.pack(side="right", pady=50, padx=100, fill='x')

# Put login text in container
loginText = tk.Label(loginFormFrame, text="LOGIN", font=("Lato", 28, "bold"), bg="#C4DAD2")
loginText.pack(anchor="n")

# Login form email address

# Declaring string vars to store email and password
emailVar = tk.StringVar()
pwVar = tk.StringVar()

# Function for submit
def submit():

    email = emailVar.get()
    password = pwVar.get()
    
    print("Email: " + email)
    print("Password: " + password)
    
    emailVar.set("")
    pwVar.set("")

# Function for radio buttons
def sel():
   selection = "You selected the option " + str(var.get())
   label.config(text = selection)

# Create a label for email
emailLabel = tk.Label(loginFormFrame, text = 'Email', bg="#C4DAD2", font=('Lato', 18, 'bold'))
emailLabel.pack(anchor="w", pady=10)
 
# Create a entry for email
emailEntry = tk.Entry(loginFormFrame, textvariable = emailVar, font=('Lato', 16, 'normal'))
emailEntry.pack(anchor="w", pady=10)
 
# Create a label for password
pwLabel = tk.Label(loginFormFrame, text = 'Password', bg="#C4DAD2", font = ('Lato', 18, 'bold'))
pwLabel.pack(anchor="w", pady=10)
 
# Create a entry for password
pwEntry = tk.Entry(loginFormFrame, textvariable = pwVar, font = ('Lato', 16, 'normal'), show = '*')
pwEntry.pack(anchor="w", pady=10)
 
# Create a label for role
roleLabel = tk.Label(loginFormFrame, text = 'Role', bg="#C4DAD2", font = ('Lato', 18, 'bold'))
roleLabel.pack(anchor="w", pady=10)

# Create radio buttons
var = tk.IntVar()
cust = tk.Radiobutton(loginFormFrame, text="Customer", bg="#C4DAD2", font = ('Lato', 16, 'normal'), variable=var, value=1, command=sel)
cust.pack(anchor="w")
sell = tk.Radiobutton(loginFormFrame, text="Seller", bg="#C4DAD2", font = ('Lato', 16, 'normal'), variable=var, value=2, command=sel)
sell.pack(anchor="w")
label = tk.Label(loginFormFrame, bg="#C4DAD2", font = ('Lato', 16, 'normal'))
label.pack()

# Create a button for login/submit
submitButton = tk.Button(loginFormFrame, text = 'Login', bg="#5B8676", fg='white', font = ('Lato', 12, 'normal'), command = submit)
submitButton.pack(side="right", pady=10)

# Create a hyperlink for sign up
signup = tk.Label(loginFormFrame, text="Sign Up Instead", bg="#C4DAD2", fg="black", cursor="hand2", font = ('Lato', 12, 'underline'))
signup.pack(side="left")
signup.bind("<Button-1>", lambda e: callback("https://www.figma.com/design/4RUsaw0PlEYKsbcCDe9EGG/Database-(Online-Store)?node-id=0-1&node-type=canvas&t=YM2GzmleMybZS2GS-0"))

root.mainloop()