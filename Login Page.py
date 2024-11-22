import tkinter as tk
from tkinter import messagebox
from sql_connection import getsqlconnection
from SignUpPage import SignUpPage
from Home import Homepage
from Seller_HomePage import SellerHomePage

class LoginPage():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        content = tk.Frame(self.root, bg="#C4DAD2")
        content.pack(padx=20, pady=20)

        storeLogoFrame = tk.Frame(content, bg="#C4DAD2", borderwidth=1, relief='solid')
        storeLogoFrame.pack(side="left", pady=10, padx=10, fill='x')

        storeLogoText = tk.Label(storeLogoFrame, text="ONLINE\nSTORE", font=("Lato", 32, "bold"), bg="#C4DAD2")
        storeLogoText.pack(anchor="w")

        self.emailVar = tk.StringVar()
        self.pwVar = tk.StringVar()
        self.roleVar = tk.IntVar()

        loginFormFrame = tk.Frame(content, bg="#C4DAD2")
        loginFormFrame.pack(side="right", pady=50, padx=100, fill='x')

        loginText = tk.Label(loginFormFrame, text="LOGIN", font=("Lato", 28, "bold"), bg="#C4DAD2")
        loginText.pack(anchor="n")

        emailLabel = tk.Label(loginFormFrame, text = 'Email', bg="#C4DAD2", font=('Lato', 18, 'bold'))
        emailLabel.pack(anchor="w", pady=10)
        
        emailEntry = tk.Entry(loginFormFrame, textvariable = self.emailVar, font=('Lato', 16, 'normal'))
        emailEntry.pack(anchor="w", pady=10)
        
        pwLabel = tk.Label(loginFormFrame, text = 'Password', bg="#C4DAD2", font = ('Lato', 18, 'bold'))
        pwLabel.pack(anchor="w", pady=10)
        
        pwEntry = tk.Entry(loginFormFrame, textvariable = self.pwVar, font = ('Lato', 16, 'normal'), show = '*')
        pwEntry.pack(anchor="w", pady=10)
        
        cust = tk.Radiobutton(loginFormFrame, text="Customer", bg="#C4DAD2", font=('Lato', 16, 'normal'), variable=self.roleVar, value=1)
        cust.pack(anchor="w")
        sell = tk.Radiobutton(loginFormFrame, text="Seller", bg="#C4DAD2", font=('Lato', 16, 'normal'), variable=self.roleVar, value=2)
        sell.pack(anchor="w")

        submitButton = tk.Button(loginFormFrame, text = 'Login', bg="#5B8676", fg='white', font = ('Lato', 12, 'normal'), command = self.submit)
        submitButton.pack(side="right", pady=10)

        signup = tk.Label(loginFormFrame, text="Sign Up Instead", bg="#C4DAD2", fg="black", cursor="hand2", font = ('Lato', 12, 'underline'))
        signup.pack(side="left")
        signup.bind("<Button-1>", lambda e: self.goToSignup(e))

        self.root.mainloop()

    
    def goToSignup(self, event=None):  
        self.root.destroy()
        SignUpPage(self, {})

    def submit(self):
        email = self.emailVar.get()
        password = self.pwVar.get()
        role = self.roleVar.get()

        if role == 1:
            role_str = "customer"
        else:
            role_str = "seller"
        
        try:
            connection = getsqlconnection()
            cursor = connection.cursor()

            query = "SELECT * FROM user WHERE email = %s AND password = %s AND userType = %s"
            cursor.execute(query, (email, password, role_str))
            result = cursor.fetchone()

            if result:
                userid = result[0]
                fname = result[2]
                lname = result[3]
                messagebox.showinfo("Login Success", f"Welcome {fname} {lname}!")
                self.root.destroy()  
                if(role_str=='customer'): Homepage(userid)  
                else: SellerHomePage(userid)
            else:
                messagebox.showerror("Login Failed", "Incorrect or Invalid credentials. Please try again.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


        self.emailVar.set("")
        self.pwVar.set("")


LoginPage()
