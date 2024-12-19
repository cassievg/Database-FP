import tkinter as tk
from tkinter import messagebox
from sql_connection import getsqlconnection
from Home import Homepage
from Seller_HomePage import SellerHomePage

class SignupPage2():
    def __init__(self, userDict, signuproot):
        self.userDict = userDict
        self.signupRoot = signuproot
        self.root = tk.Tk()
        self.root.title("Sign Up Page - Payment Type")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        storeLogoFrame = tk.Frame(self.root, bg="#C4DAD2", borderwidth=1, relief='solid')
        storeLogoFrame.pack(side="left", pady=10, padx=70, fill='x')

        storeLogoText = tk.Label(storeLogoFrame, text="ONLINE\nSTORE", font=("Lato", 32, "bold"), bg="#C4DAD2")
        storeLogoText.pack(anchor="w")

        yourShopText = tk.Label(self.root, text="PAYMENT TYPE", font='Lato 32 bold', bg='#C4DAD2')
        yourShopText.place(x=573, y=33)

        contentFrame = tk.Frame(self.root, bg='#C4DAD2')
        contentFrame.place(x=512, y=152, width=690, height=430)

        self.labelName = ['BCA', 'OVO', 'GOPAY', 'BNI', 'BRI']
        self.entries = []

        for e in self.labelName:
            label_frame = tk.Frame(contentFrame, bg='#C4DAD2')
            label_frame.pack(pady=(15, 15), padx=10, anchor='w')  # Padding around the entire frame

            label = tk.Label(label_frame, text=e, font='Lato 20 bold', bg='#C4DAD2')
            label.pack(side='left', padx=(0, 10))  # Padding to the right of the label

            entry = tk.Entry(label_frame, background='white', foreground='black', font=('Lato', 20), width=25)
            entry.pack(side='left', padx=(10, 0))  # Padding to the left of the entry
            self.entries.append((e, entry))  # Keep the payment type with the corresponding entry

        self.backButton = tk.Button(self.root, command=self.goBack, bg="#5B8676", fg="white", text='Back', font='Lato 16 bold')
        self.backButton.place(x=520, y=549, width=100, height=50)

        self.okButton = tk.Button(self.root, command=self.okClicked, bg="#5B8676", fg="white", text='Sign Up', font='Lato 16 bold')
        self.okButton.place(x=890, y=549, width=120, height=50)

        self.root.mainloop()
    

    def checkPaymentDetails(self, p):
        for char in p:
            if not char.isdigit():
                messagebox.showinfo("Error", "Please use numeric characters only for payment details")
                return False
        return True

    def okClicked(self):
        try:
            connection = getsqlconnection()
            cursor = connection.cursor()
            paymentDict = {}

            for paymentType, entry in self.entries:
                paymentDetails = entry.get()
                if not paymentDetails.strip():
                    continue
                
                if len(paymentDetails)>45:
                    messagebox.showerror("Error", f"Payment number cannot exceed 45 characters")
                    return
                if not self.checkPaymentDetails(paymentDetails):
                    return
                paymentDict[paymentType]= paymentDetails
            
            if not paymentDict:
                messagebox.showerror("Error", f"At least one payment type have to be filled.")
                return

            role_str = self.userDict['userType']
            fName = self.userDict['fName']
            lName= self.userDict['lName']
            address= self.userDict['address']
            phoneNo=self.userDict['phoneNumber']
            password =self.userDict['password']
            email =self.userDict['email']

            query1 = "SELECT userID FROM user ORDER BY userID DESC LIMIT 1;"
            cursor.execute(query1)
            result = cursor.fetchone()  # Fetch the first row

            # Check if a row is returned
            if result is not None:
                last_userid = result[0]  # Extract the first element (userID)
                user_id = last_userid + 1
            else:
                user_id = 1  # Default to 1 if no rows are returned

            cursor = connection.cursor()
            query_insert = """
            INSERT INTO user (userID, userType, fName, lName, address, phoneNumber, password, email, cartID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert, (user_id, role_str, fName, lName, address, phoneNo, password, email, user_id))
            connection.commit()

            for key, val in paymentDict.items():
                query = """
                INSERT INTO payment (paymentType, paymentDetails, userID)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (key, val, user_id))

            connection.commit()
            messagebox.showinfo("Success", "Account created successfully!")


            self.root.destroy()
            if(role_str.lower()=='customer'): Homepage(user_id)
            else: SellerHomePage(user_id)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


    def goBack(self):
        self.root.destroy()
        self.signupRoot.__class__(self.signupRoot, self.userDict)




