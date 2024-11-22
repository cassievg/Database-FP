import tkinter as tk
from tkinter import font
from tkinter import simpledialog, messagebox
from RoleDialog import RoleDialog
from sql_connection import getsqlconnection

class UserSetting():
    def __init__(self, userid=1, prevroot=None):
        self.root = tk.Tk()
        self.root.title("User Setting")
        self.userID = userid
        self.connection = getsqlconnection()
        self.prevroot = prevroot

        self.root.configure(bg="#C4DAD2")
        self.root.geometry("1280x720")
        self.root.protocol("WM_DELETE_WINDOW", self.end)

        title_font = font.Font(size=30, weight="bold")

        self.user_setting = tk.Label(self.root, text="USER SETTING", font=title_font, bg="#C4DAD2")
        self.user_setting.place(x=100, y=50)

        normal_text = font.Font(size=15)
        change_font = font.Font(size=8)

        cursor =self.connection.cursor()
        cursor.execute(f'SELECT * FROM user WHERE userID={self.userID}')
        result = cursor.fetchone()
        self.userDict = {}

        self.userDict['userType'] = result[1]
        self.userDict['fName'] =result[2]
        self.userDict['lName'] =result[3]
        self.userDict['address'] =result[4]
        self.userDict['phoneNumber'] = result[5]
        self.userDict['password'] = result[6]
        self.userDict['email'] = result[7]

        self.username = tk.Label(self.root, text="User Name", font=normal_text, bg="#C4DAD2")
        self.username.place(x=480, y=185)

        self.username_frame = tk.Frame(self.root, width=300, height=60, bg="#FFFFFF")
        self.username_frame.place(x=600, y=185)

        name = self.userDict['fName'] +" " + self.userDict['lName']
        self.username_label = tk.Label(self.username_frame, text=name, bg="#FFFFFF", wraplength=280, justify='left', anchor='w')
        self.username_label.place(x=5, y=3)

        self.change0 = tk.Label(self.root, text="Change", font=change_font, bg="#C4DAD2", fg="#0000EE")
        self.change0.place(x=910, y=185)
        self.change0.bind("<Button-1>", lambda event: self.change(0))

        self.userType = tk.Label(self.root, text="User Type", font=normal_text, bg="#C4DAD2")
        self.userType.place(x=480, y=270)

        self.usertype_frame = tk.Frame(self.root, width=220, height=25, bg="#FFFFFF")
        self.usertype_frame.place(x=600, y=270)

        self.usertype_label = tk.Label(self.usertype_frame, text=self.userDict['userType'], bg="#FFFFFF")
        self.usertype_label.place(x=5, y=3)

        self.change5 = tk.Label(self.root, text="Change", font=change_font, bg="#C4DAD2", fg="#0000EE")
        self.change5.place(x=830, y=275)
        self.change5.bind("<Button-1>", lambda event: self.change(5))

        self.email = tk.Label(self.root, text="Email", font=normal_text, bg="#C4DAD2")
        self.email.place(x=521, y=322)

        self.email_frame = tk.Frame(self.root, width=220, height=25, bg="#FFFFFF")
        self.email_frame.place(x=600, y=322)

        self.email_label = tk.Label(self.email_frame, text=self.userDict['email'], bg="#FFFFFF")
        self.email_label.place(x=5, y=3)

        self.change1 = tk.Label(self.root, text="Change", font=change_font, bg="#C4DAD2", fg="#0000EE")
        self.change1.place(x=830, y=325)
        self.change1.bind("<Button-1>", lambda event: self.change(1))

        self.phoneNumber = tk.Label(self.root, text="Phone Number", font=normal_text, bg="#C4DAD2")
        self.phoneNumber.place(x=443, y=374)

        self.change2 = tk.Label(self.root, text="Change", font=change_font, bg="#C4DAD2", fg="#0000EE")
        self.change2.place(x=830, y=377)
        self.change2.bind("<Button-1>", lambda event: self.change(2))

        self.phoneNumber_frame = tk.Frame(self.root, width=220, height=25, bg="#FFFFFF")
        self.phoneNumber_frame.place(x=600, y=374)

        self.phone_label = tk.Label(self.phoneNumber_frame, text=self.userDict['phoneNumber'], bg="#FFFFFF")
        self.phone_label.place(x=5, y=3)

        pw = ("*" * len(self.userDict['password']))
        self.password = tk.Label(self.root, text="Password", font=normal_text, bg="#C4DAD2")
        self.password.place(x=483, y=426)

        self.password_frame = tk.Frame(self.root, width=220, height=25, bg="#FFFFFF")
        self.password_frame.place(x=600, y=425)

        self.password_label = tk.Label(self.password_frame, text=pw, bg="#FFFFFF")
        self.password_label.place(x=5, y=3)

        self.hidden_password = tk.Label(self.root, text=self.userDict['password'])
        self.hidden_password.place(x=-1000, y= 199)

        self.change3 = tk.Label(self.root, text="Change", font=change_font, bg="#C4DAD2", fg="#0000EE")
        self.change3.place(x=830, y=428)
        self.change3.bind("<Button-1>", lambda event: self.change(3))

        self.address = tk.Label(self.root, text="Address", font=normal_text, bg="#C4DAD2")
        self.address.place(x=495, y=482)

        self.address_frame = tk.Frame(self.root, width=400, height=140, bg="#FFFFFF")
        self.address_frame.place(x=600, y=482)

        self.address_label = tk.Label(self.address_frame, wraplength=380, anchor='w', justify='left', text=self.userDict['address'], bg="#FFFFFF")
        self.address_label.place(x=5, y=3)

        self.change4 = tk.Label(self.root, text="Change", font=change_font, bg="#C4DAD2", fg="#0000EE")
        self.change4.place(x=1010, y=486)
        self.change4.bind("<Button-1>", lambda event: self.change(4))



        self.backButton = tk.Button(self.root, command=self.goBack, width=15, height=3, text="Back", fg="#FFFFFF", bg="#5B8676")
        self.backButton.place(x=110, y=500)

        self.userBiodata = tk.Button(self.root, width=17, height=2, text="User Biodata", fg="#FFFFFF", bg="#5B8676", command=self.to_root_1)
        self.userBiodata.place(x=110, y=250)

        self.paymentAccounts = tk.Button(self.root, width=17, height=2, text="Payment Accounts", bg="#C4DAD2", command=self.to_root_2)
        self.paymentAccounts.place(x=110, y=290)

        self.root2 = tk.Toplevel()
        self.root2.title("User Setting")
        self.root2.withdraw()

        self.root2.configure(bg="#C4DAD2")
        self.root2.geometry("1280x720")
        self.root2.protocol("WM_DELETE_WINDOW", self.end)

        title_font = font.Font(size=30, weight="bold")

        self.user_setting = tk.Label(self.root2, text="USER SETTING", font=title_font, bg="#C4DAD2")
        self.user_setting.place(x=100, y=50)
        normal_text = font.Font(size=15)

        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM payment WHERE userID={self.userID}")
        self.paymentDict = {}

        for(paymentID, paymentType, paymentDetails, userID) in cursor:
            self.paymentDict[paymentType] = (paymentID, paymentDetails)


        self.BCA = tk.Label(self.root2, text="BCA", font=normal_text, bg="#C4DAD2")
        self.BCA.place(x=523, y=270)

        self.BCA_frame = tk.Frame(self.root2, width=220, height=25, bg="#FFFFFF")
        self.BCA_frame.place(x=600, y=270)

        bcatext = self.paymentDict.get('BCA', ('', ''))[1]
        self.BCA_label = tk.Label(self.BCA_frame, text=bcatext, bg="#FFFFFF")
        self.BCA_label.place(x=5, y=3)

        self.OVO = tk.Label(self.root2, text="OVO", font=normal_text, bg="#C4DAD2")
        self.OVO.place(x=521, y=322)

        self.OVO_frame = tk.Frame(self.root2, width=220, height=25, bg="#FFFFFF")
        self.OVO_frame.place(x=600, y=322)

        ovotext = self.paymentDict.get('OVO', ('', ''))[1]
        self.OVO_label = tk.Label(self.OVO_frame, text=ovotext, bg="#FFFFFF")
        self.OVO_label.place(x=5, y=3)

        self.GOPAY = tk.Label(self.root2, text="GOPAY", font=normal_text, bg="#C4DAD2")
        self.GOPAY.place(x=495, y=374)

        self.GOPAY_frame = tk.Frame(self.root2, width=220, height=25, bg="#FFFFFF")
        self.GOPAY_frame.place(x=600, y=374)

        gopaytext = self.paymentDict.get('GOPAY', ('', ''))[1]
        self.GOPAY_label = tk.Label(self.GOPAY_frame, text=gopaytext, bg="#FFFFFF")
        self.GOPAY_label.place(x=5, y=3)

        self.BNI = tk.Label(self.root2, text="BNI", font=normal_text, bg="#C4DAD2")
        self.BNI.place(x=531, y=426)

        self.BNI_frame = tk.Frame(self.root2, width=220, height=25, bg="#FFFFFF")
        self.BNI_frame.place(x=600, y=425)

        bnitext=self.paymentDict.get('BNI', ('', ''))[1]
        self.BNI_label = tk.Label(self.BNI_frame, text=bnitext, bg="#FFFFFF")
        self.BNI_label.place(x=5, y=3)

        self.BRI = tk.Label(self.root2, text="BRI", font=normal_text, bg="#C4DAD2")
        self.BRI.place(x=531, y=476)

        self.BRI_frame = tk.Frame(self.root2, width=220, height=25, bg="#FFFFFF")
        self.BRI_frame.place(x=600, y=475)

        britext = self.paymentDict.get('BRI', ('', ''))[1]
        self.BRI_label = tk.Label(self.BRI_frame, text=britext, bg="#FFFFFF")
        self.BRI_label.place(x=5, y=3)

        self.labelpaymentlist = [self.BCA_label, self.OVO_label, self.GOPAY_label, self.BNI_label, self.BRI_label]

        link_font = font.Font(size=10)

        self.link0 = tk.Label(self.root2, text="Change", font=link_font, bg="#C4DAD2", fg="#0000EE")
        self.link0.place(x=830, y=275)
        self.link0.bind("<Button-1>", lambda event: self.link(0))

        self.link1 = tk.Label(self.root2, text="Change", font=link_font, bg="#C4DAD2", fg="#0000EE")
        self.link1.place(x=830, y=325)
        self.link1.bind("<Button-1>", lambda event: self.link(1))

        self.link2 = tk.Label(self.root2, text="Change", font=link_font, bg="#C4DAD2", fg="#0000EE")
        self.link2.place(x=830, y=377)
        self.link2.bind("<Button-1>", lambda event: self.link(2))

        self.link3 = tk.Label(self.root2, text="Change", font=link_font, bg="#C4DAD2", fg="#0000EE")
        self.link3.place(x=830, y=428)
        self.link3.bind("<Button-1>", lambda event: self.link(3))

        self.link4 = tk.Label(self.root2, text="Change", font=link_font, bg="#C4DAD2", fg="#0000EE")
        self.link4.place(x=830, y=478)
        self.link4.bind("<Button-1>", lambda event: self.link(4))


        self.delete0 = tk.Label(self.root2, text="Delete", font=link_font, bg="#C4DAD2", fg="firebrick")
        self.delete0.place(x=890, y=275)
        self.delete0.bind("<Button-1>", lambda event: self.deletepayment(0))

        self.delete1 = tk.Label(self.root2, text="Delete", font=link_font, bg="#C4DAD2", fg="firebrick")
        self.delete1.place(x=890, y=325)
        self.delete1.bind("<Button-1>", lambda event: self.deletepayment(1))

        self.delete2 = tk.Label(self.root2, text="Delete", font=link_font, bg="#C4DAD2", fg="firebrick")
        self.delete2.place(x=890, y=377)
        self.delete2.bind("<Button-1>", lambda event: self.deletepayment(2))

        self.delete3 = tk.Label(self.root2, text="Delete", font=link_font, bg="#C4DAD2", fg="firebrick")
        self.delete3.place(x=890, y=428)
        self.delete3.bind("<Button-1>", lambda event: self.deletepayment(3))

        self.delete4 = tk.Label(self.root2, text="Delete", font=link_font, bg="#C4DAD2", fg="firebrick")
        self.delete4.place(x=890, y=478)
        self.delete4.bind("<Button-1>", lambda event: self.deletepayment(4))


        self.backButton = tk.Button(self.root2, command=self.goBack, width=15, height=3, text="Back", fg="#FFFFFF", bg="#5B8676")
        self.backButton.place(x=110, y=500)

        self.userBiodata = tk.Button(self.root2, width=17, height=2, text="User Biodata", bg ="#C4DAD2", command=self.to_root_1)
        self.userBiodata.place(x=110, y=250)

        self.paymentAccounts = tk.Button(self.root2, width=17, height=2, text="Payment Accounts", fg="#FFFFFF", bg="#5B8676", command=self.to_root_2)
        self.paymentAccounts.place(x=110, y=290)

        self.root.mainloop()

    def to_root_1(self):
        self.root2.withdraw()
        self.root.deiconify()

    def to_root_2(self):
        self.root.withdraw()
        self.root2.deiconify()
    
    def goBack(self):
        self.root.destroy()
        self.prevroot.__class__(self.userID)

    def end(self):
        self.root.destroy()
        self.root2.destroy()


    def change(self, num):
        if num == 0:
            new_name = simpledialog.askstring("Input", "Enter the new name:")
            if new_name:
                names = new_name.split(maxsplit=1)
                fName = names[0]
                lName = names[1] if len(names) > 1 else ""
                self.username_label.configure(text=new_name)
                cursor = self.connection.cursor()
                cursor.execute(f"UPDATE user SET fName='{fName}', lName='{lName}' WHERE userID={self.userID}")
                self.connection.commit()

        if num == 1:
            new_email = simpledialog.askstring("Input", "Enter the new email:")
            if new_email:
                self.email_label.configure(text=new_email)
                cursor =self.connection.cursor()
                cursor.execute(f"UPDATE user SET email='{new_email}' WHERE userID={self.userID}")
                self.connection.commit()

        elif num == 2:
            new_phone_number = simpledialog.askstring("Input", "Enter your new phone number:")
            correct_form = True

            for char in new_phone_number:
                if char.isdigit():
                    continue
                else:
                    correct_form = False
                    messagebox.showinfo("Error", "Please use numeric characters only")
                    break

            if correct_form:
                self.phone_label.configure(text=new_phone_number)
                cursor =self.connection.cursor()
                cursor.execute(f"UPDATE user SET phoneNumber='{new_phone_number}' WHERE userID={self.userID}")
                self.connection.commit()

        elif num == 3:
            current_password = self.hidden_password.cget("text")
            confirm_password = simpledialog.askstring("Input", "Enter your previous password:")
            if confirm_password == current_password:
                new_password = simpledialog.askstring("Input", "Enter your new password:")
                while new_password == current_password:
                    messagebox.showerror("Error", "New password must be different from previous password")
                    new_password = simpledialog.askstring("Input", "Enter your new password:")  # Refocus here
                if new_password:
                    current_password = new_password
                    self.password_label.configure(text=("*" * len(current_password)))
                    self.hidden_password.configure(text=new_password)
                    cursor = self.connection.cursor()
                    cursor.execute("UPDATE user SET password=%s WHERE userID=%s", (new_password, self.userID))
                    self.connection.commit()
            else:
                messagebox.showerror("Error", "Password is Incorrect")

        
        elif num == 4:
            new_address = simpledialog.askstring("Input", "Enter the new address:")
            if new_address:
                self.address_label.configure(text=new_address)
                cursor =self.connection.cursor()
                cursor.execute(f"UPDATE user SET address='{new_address}' WHERE userID={self.userID}")
                self.connection.commit()

        elif num==5:
            dialog = RoleDialog(self.root, title="Choose Role")
            role = dialog.result
            self.usertype_label.configure(text=role.capitalize())
            cursor =self.connection.cursor()
            cursor.execute(f"UPDATE user SET userType='{role}' WHERE userID={self.userID}")
            self.connection.commit()
    

    def link(self,num):
        plist = ['BCA', 'OVO', 'GOPAY', 'BNI', 'BRI']
        new_acc = simpledialog.askstring("Input", f"Enter the new {plist[num]}:")
        if not new_acc: return

        correct_form = True
        for char in new_acc:
            if not char.isdigit():
                correct_form = False
                messagebox.showinfo("Error", "Please use numeric characters only")
                break

        if new_acc and correct_form:
            current = self.labelpaymentlist[num].cget('text')
            self.labelpaymentlist[num].configure(text=new_acc)
            if current =='':
                cursor=self.connection.cursor()
                cursor.execute(f"INSERT INTO payment(paymentType, paymentDetails, userID) VALUES('{plist[num]}', '{new_acc}', {self.userID})")
                self.connection.commit()
                payment_id = cursor.lastrowid
                self.paymentDict[plist[num]] = (payment_id, new_acc)

            else:
                cursor =self.connection.cursor()
                paymentid = self.paymentDict[plist[num]][0]
                cursor.execute(f"UPDATE payment SET paymentDetails='{new_acc}' WHERE paymentID={paymentid}")
                self.paymentDict[plist[num]] = (paymentid, new_acc)
                self.connection.commit()
    

    def deletepayment(self, num):
        plist = ['BCA', 'OVO', 'GOPAY', 'BNI', 'BRI']
        answer = messagebox.askyesno(title='confirmation', message=f'Are you sure that you want to delete account for {plist[num]}?')
        
        if answer:
            current = self.labelpaymentlist[num].cget('text')
            if current =='':
                messagebox.showerror(title='Error', message=f"Sorry, we couldn't find an account registered under your name for {plist[num]}")
            else:
                cursor =self.connection.cursor()
                cursor.execute(f"DELETE FROM payment where paymentID={self.paymentDict[plist[num]][0]}")
                self.connection.commit()
                self.labelpaymentlist[num].configure(text='')



UserSetting()