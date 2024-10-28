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
root.title("Sign Up Page")

# Setting up background color and size
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
signupFormFrame = tk.Frame(content, bg="#C4DAD2")
signupFormFrame.pack(side="right", pady=50, padx=100, fill='x')

# Put sign up text in container
signupText = tk.Label(signupFormFrame, text="SIGN UP", font=("Lato", 28, "bold"), bg="#C4DAD2")
signupText.pack(anchor="n")

# Create a canvas to hold form content and make it scrollable
canvas = tk.Canvas(signupFormFrame, bg="#C4DAD2", highlightthickness=0)
scrollableFrame = tk.Frame(canvas, bg="#C4DAD2")

# Create scrollbar
scrollbar = tk.Scrollbar(signupFormFrame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Pack canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Place the frame on the canvas
canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

# Update scroll region
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollableFrame.bind("<Configure>", on_frame_configure)

# Declaring string vars to store user inputs
fNameVar = tk.StringVar()
lNameVar = tk.StringVar()
addressVar = tk.StringVar()
phonenumVar = tk.StringVar()
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
   label.config(text=selection)

# Add form labels and entries to the scrollable frame
form_elements = [
    ("First Name", fNameVar), ("Last Name", lNameVar),
    ("Address", addressVar), ("Phone Number", phonenumVar),
    ("Email", emailVar), ("Password", pwVar)
]

for label_text, var in form_elements:
    label = tk.Label(scrollableFrame, text=label_text, bg="#C4DAD2", font=('Lato', 16, 'bold'))
    label.pack(anchor="w", pady=10)
    entry = tk.Entry(scrollableFrame, textvariable=var, font=('Lato', 16, 'normal'))
    if label_text == "Password":
        entry.config(show="*")
    entry.pack(anchor="w", pady=10)

# Role selection (radio buttons)
roleLabel = tk.Label(scrollableFrame, text='Role', bg="#C4DAD2", font=('Lato', 16, 'bold'))
roleLabel.pack(anchor="w", pady=10)

var = tk.IntVar()
cust = tk.Radiobutton(scrollableFrame, text="Customer", bg="#C4DAD2", font=('Lato', 16, 'normal'), variable=var, value=1, command=sel)
cust.pack(anchor="w")
sell = tk.Radiobutton(scrollableFrame, text="Seller", bg="#C4DAD2", font=('Lato', 16, 'normal'), variable=var, value=2, command=sel)
sell.pack(anchor="w")

# Selection label
label = tk.Label(scrollableFrame, bg="#C4DAD2", font=('Lato', 16, 'normal'))
label.pack()

# Create container for buttons
buttonsFrame = tk.Frame(root, bg="#C4DAD2")
buttonsFrame.pack()

# Create a button for signup/submit
submitButton = tk.Button(buttonsFrame, text='Next', bg="#5B8676", fg='white', font=('Lato', 12, 'normal'), command=submit)
submitButton.pack(side="right", pady=10, padx=100)

# Create a hyperlink for sign up
signup = tk.Label(buttonsFrame, text="Login Instead", fg="black", cursor="hand2", font=('Lato', 12, 'underline'))
signup.pack(side="left")
signup.bind("<Button-1>", lambda e: callback("https://www.figma.com/design/4RUsaw0PlEYKsbcCDe9EGG/Database-(Online-Store)?node-id=0-1&node-type=canvas&t=YM2GzmleMybZS2GS-0"))

root.mainloop()
