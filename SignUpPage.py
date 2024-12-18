import re
import tkinter as tk
from tkinter import messagebox
from sql_connection import getsqlconnection
from SignUpPage2 import SignupPage2

class SignUpPage():
    def __init__(self, loginpageroot, userDict):
        self.root = tk.Tk()
        self.root.title("Sign Up Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')
        self.loginPageRoot = loginpageroot
        self.userDict = userDict

        content = tk.Frame(self.root, bg="#C4DAD2")
        content.pack(padx=20, pady=20)

        storeLogoFrame = tk.Frame(content, bg="#C4DAD2", borderwidth=1, relief='solid')
        storeLogoFrame.pack(side="left", pady=10, padx=10, fill='x')

        storeLogoText = tk.Label(storeLogoFrame, text="ONLINE\nSTORE", font=("Lato", 32, "bold"), bg="#C4DAD2")
        storeLogoText.pack(anchor="w")

        signupFormFrame = tk.Frame(content, bg="#C4DAD2")
        signupFormFrame.pack(side="right", pady=50, padx=100, fill='x')

        signupText = tk.Label(signupFormFrame, text="SIGN UP", font=("Lato", 28, "bold"), bg="#C4DAD2")
        signupText.pack(anchor="n")

        self.canvas = tk.Canvas(signupFormFrame, bg="#C4DAD2", highlightthickness=0)
        scrollableFrame = tk.Frame(self.canvas, bg="#C4DAD2")

        scrollbar = tk.Scrollbar(signupFormFrame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

        scrollableFrame.bind("<Configure>", lambda e: self.on_frame_configure(e))
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.fNameVar = tk.StringVar()
        self.lNameVar = tk.StringVar()
        self.addressVar = tk.StringVar()
        self.phonenumVar = tk.StringVar()
        self.emailVar = tk.StringVar()
        self.pwVar = tk.StringVar()
        self.roleVar = tk.IntVar()

        form_elements = [
            ("First Name", self.fNameVar, 'fName'), ("Last Name", self.lNameVar, 'lName'),
            ("Address", self.addressVar, 'address'), ("Phone Number", self.phonenumVar, 'phoneNumber'),
            ("Email", self.emailVar,'email'), ("Password", self.pwVar, 'password')
        ]

        for label_text, var, dict_label in form_elements:
            label = tk.Label(scrollableFrame, text=label_text, bg="#C4DAD2", font=('Lato', 16, 'bold'))
            label.pack(anchor="w", pady=10)
            entry = tk.Entry(scrollableFrame, textvariable=var, font=('Lato', 16, 'normal'))

            if self.userDict : entry.insert(0, self.userDict[dict_label])
            if label_text == "Password":
                entry.config(show="*")
            entry.pack(anchor="w", pady=10)

        cust = tk.Radiobutton(scrollableFrame, text="Customer", bg="#C4DAD2", font=('Lato', 16, 'normal'), variable=self.roleVar, value=1)
        cust.pack(anchor="w")
        sell = tk.Radiobutton(scrollableFrame, text="Seller", bg="#C4DAD2", font=('Lato', 16, 'normal'), variable=self.roleVar, value=2)
        sell.pack(anchor="w")

        if self.userDict:
            if self.userDict['userType'].lower()=='customer': cust.select()
            else: sell.select()

        label = tk.Label(scrollableFrame, bg="#C4DAD2", font=('Lato', 16, 'normal'))
        label.pack()

        buttonsFrame = tk.Frame(self.root, bg="#C4DAD2")
        buttonsFrame.pack()

        submitButton = tk.Button(buttonsFrame, text='Next', bg="#5B8676", fg='white', font=('Lato', 12, 'normal'), command=self.submit)
        submitButton.pack(side="right", pady=10, padx=100)

        signup = tk.Label(buttonsFrame, text="Login Instead", fg="black", cursor="hand2", font=('Lato', 12, 'underline'))
        signup.pack(side="left")
        signup.bind("<Button-1>", lambda e: self.goToLogin(e))

        self.root.mainloop()
    
    def on_frame_configure(self,event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def goToLogin(self, event=None):
        self.root.destroy()
        self.loginPageRoot.__class__()


    def submit(self):
        fName = self.fNameVar.get()
        lName = self.lNameVar.get()
        address = self.addressVar.get()
        phoneNo = self.phonenumVar.get()
        email = self.emailVar.get()
        password = self.pwVar.get()
        role = self.roleVar.get()

        if role == 1:
            role_str = "customer"
        else:
            role_str = "seller"

        if not all([fName, lName, address, phoneNo, email, password, role]):
            messagebox.showerror("Input Error", "Missing fields.")
            return
        
        if len(fName)>50 or len(lName)>50: 
            messagebox.showinfo("Error", "Length of first name or last name cannot exceed 50")
            return
        
        if len(address)>500:
            messagebox.showinfo('Error', "Length of address cannot exceed 500")
            return
        
        if len(phoneNo)>15: 
            messagebox.showinfo('Error', "Length of phone number cannot exceed 15")
            return
        
        if len(email)>255:
            messagebox.showinfo('Error', "Length of address cannot exceed 255")
            return
        
        if len(password)>45:
            messagebox.showinfo('Error', "Length of password cannot exceed 45")
            return

        for char in phoneNo:
            if not char.isdigit():
                messagebox.showinfo("Error", "Please use numeric characters only for phone number")
                return
        
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if not valid:
            messagebox.showinfo("Error", "Please use a valid email address")
            return
        
        validpassword = re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password)
        if not validpassword:
            messagebox.showinfo("Error", "Password must have at least has 8 characters with at least one letter and one number")
            return
            

        try:
            connection = getsqlconnection()
            cursor = connection.cursor()

            query_check = "SELECT * FROM user WHERE email = %s"
            cursor.execute(query_check, (email,))
            if cursor.fetchone():
                messagebox.showerror("Signup Error", "This email already exists.")
                return
            
            userdict ={}
            userdict['userType'] = role_str
            userdict['fName'] = fName
            userdict['lName'] =lName
            userdict['address'] =address
            userdict['phoneNumber'] =phoneNo
            userdict['password'] =password
            userdict['email'] =email

            self.root.destroy()
            SignupPage2(userdict, self)

            self.fNameVar.set("")
            self.lNameVar.set("")
            self.addressVar.set("")
            self.phonenumVar.set("")
            self.emailVar.set("")
            self.pwVar.set("")
            self.roleVar.set(0)


        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


