import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser
from sql_connection import getsqlconnection

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
roleVar = tk.IntVar()

# Function for submit
def submit():

    email = emailVar.get()
    password = pwVar.get()
    role = roleVar.get()

    # Convert role integer input to string
    if role == 1:
        role_str = "customer"
    else:
        role_str = "seller"
    
    try:
        # Connect to the database
        connection = getsqlconnection()
        cursor = connection.cursor()

        # SQL query to check if user exists
        query = "SELECT * FROM users WHERE email = %s AND password = %s AND role = %s"
        cursor.execute(query, (email, password, role_str))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Success", f"Welcome {email}!")
        else:
            messagebox.showerror("Login Failed", "Incorrect or Invalid credentials. Please try again.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        if 'connection' in locals():
            connection.close()

    # Clear fields
    emailVar.set("")
    pwVar.set("")

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
cust = tk.Radiobutton(loginFormFrame, text="Customer", bg="#C4DAD2", font=('Lato', 16, 'normal'), variable=roleVar, value=1)
cust.pack(anchor="w")
sell = tk.Radiobutton(loginFormFrame, text="Seller", bg="#C4DAD2", font=('Lato', 16, 'normal'), variable=roleVar, value=2)
sell.pack(anchor="w")

# Create a button for login/submit
submitButton = tk.Button(loginFormFrame, text = 'Login', bg="#5B8676", fg='white', font = ('Lato', 12, 'normal'), command = submit)
submitButton.pack(side="right", pady=10)

# Create a hyperlink for sign up
signup = tk.Label(loginFormFrame, text="Sign Up Instead", bg="#C4DAD2", fg="black", cursor="hand2", font = ('Lato', 12, 'underline'))
signup.pack(side="left")
signup.bind("<Button-1>", lambda e: callback("https://www.figma.com/design/4RUsaw0PlEYKsbcCDe9EGG/Database-(Online-Store)?node-id=0-1&node-type=canvas&t=YM2GzmleMybZS2GS-0"))

root.mainloop()

