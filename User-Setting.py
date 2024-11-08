import tkinter as tk
from tkinter import font
from tkinter import simpledialog, messagebox

class userSetting:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("User Setting")

        self.root.configure(bg="#C4DAD2")
        self.root.geometry("1280x720")
        self.root.protocol("WM_DELETE_WINDOW", self.end)

        title_font = font.Font(size=30, weight="bold")

        self.user_setting = tk.Label(self.root, text="USER SETTING", font=title_font, bg="#C4DAD2")
        self.user_setting.place(x=100, y=50)

        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="#C4DAD2", highlightthickness=0)
        self.canvas.place(x=545, y=183)

        self.canvas.create_oval(0, 20, 40, 60, fill="#FFFFFF")

        normal_text = font.Font(size=15)

        self.full_name = tk.Label(self.root, text="Newbie Martinez", font=normal_text, bg="#C4DAD2")
        self.full_name.place(x=600, y=210)

        self.ID = tk.Label(self.root, text="ID", font=normal_text, bg="#C4DAD2")
        self.ID.place(x=550, y=270)

        self.ID_frame = tk.Frame(self.root, width=220, height=25, bg="#FFFFFF")
        self.ID_frame.place(x=600, y=270)

        self.ID_label = tk.Label(self.ID_frame, text="CUS-019721679", bg="#FFFFFF")
        self.ID_label.place(x=5, y=3)

        self.email = tk.Label(self.root, text="Email", font=normal_text, bg="#C4DAD2")
        self.email.place(x=521, y=322)

        self.email_frame = tk.Frame(self.root, width=220, height=25, bg="#FFFFFF")
        self.email_frame.place(x=600, y=322)

        change_font = font.Font(size=8)

        self.email_label = tk.Label(self.email_frame, text="-", bg="#FFFFFF")
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

        self.phone_label = tk.Label(self.phoneNumber_frame, text="-", bg="#FFFFFF")
        self.phone_label.place(x=5, y=3)

        self.password = tk.Label(self.root, text="Password", font=normal_text, bg="#C4DAD2")
        self.password.place(x=483, y=426)

        self.password_frame = tk.Frame(self.root, width=220, height=25, bg="#FFFFFF")
        self.password_frame.place(x=600, y=425)

        self.password_label = tk.Label(self.password_frame, text="-", bg="#FFFFFF")
        self.password_label.place(x=5, y=3)
        self.hidden_password = tk.Label(self.root, text="-")
        self.hidden_password.place(x=-1000, y= 199)

        self.change3 = tk.Label(self.root, text="Change", font=change_font, bg="#C4DAD2", fg="#0000EE")
        self.change3.place(x=830, y=428)
        self.change3.bind("<Button-1>", lambda event: self.change(3))

        self.backButton = tk.Button(self.root, width=15, height=3, text="Back", fg="#FFFFFF", bg="#5B8676")
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

        self.BCA = tk.Label(self.root2, text="BCA", font=normal_text, bg="#C4DAD2")
        self.BCA.place(x=523, y=270)

        self.BCA_frame = tk.Frame(self.root2, width=220, height=25, bg="#FFFFFF")
        self.BCA_frame.place(x=600, y=270)

        self.BCA_label = tk.Label(self.BCA_frame, text="-", bg="#FFFFFF")
        self.BCA_label.place(x=5, y=3)

        self.OVO = tk.Label(self.root2, text="OVO", font=normal_text, bg="#C4DAD2")
        self.OVO.place(x=521, y=322)

        self.OVO_frame = tk.Frame(self.root2, width=220, height=25, bg="#FFFFFF")
        self.OVO_frame.place(x=600, y=322)

        self.OVO_label = tk.Label(self.OVO_frame, text="-", bg="#FFFFFF")
        self.OVO_label.place(x=5, y=3)

        self.GOPAY = tk.Label(self.root2, text="GOPAY", font=normal_text, bg="#C4DAD2")
        self.GOPAY.place(x=495, y=374)

        self.GOPAY_frame = tk.Frame(self.root2, width=220, height=25, bg="#FFFFFF")
        self.GOPAY_frame.place(x=600, y=374)

        self.GOPAY_label = tk.Label(self.GOPAY_frame, text="-", bg="#FFFFFF")
        self.GOPAY_label.place(x=5, y=3)

        self.BNI = tk.Label(self.root2, text="BNI", font=normal_text, bg="#C4DAD2")
        self.BNI.place(x=531, y=426)

        self.BNI_frame = tk.Frame(self.root2, width=220, height=25, bg="#FFFFFF")
        self.BNI_frame.place(x=600, y=425)

        self.BNI_label = tk.Label(self.BNI_frame, text="-", bg="#FFFFFF")
        self.BNI_label.place(x=5, y=3)

        link_font = font.Font(size=10)

        self.link1 = tk.Label(self.root2, text="Link", font=link_font, bg="#C4DAD2", fg="#0000EE")
        self.link1.place(x=830, y=325)

        self.link2 = tk.Label(self.root2, text="Link", font=link_font, bg="#C4DAD2", fg="#0000EE")
        self.link2.place(x=830, y=377)

        self.link3 = tk.Label(self.root2, text="Link", font=link_font, bg="#C4DAD2", fg="#0000EE")
        self.link3.place(x=830, y=428)

        self.backButton = tk.Button(self.root2, width=15, height=3, text="Back", fg="#FFFFFF", bg="#5B8676")
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

    def end(self):
        self.root.destroy()
        self.root2.destroy()

    def change(self, num):

        if num == 1:
            new_email = simpledialog.askstring("Input", "Enter the new email:")
            if new_email:
                self.email_label.configure(text=new_email)
            self.root.deiconify()

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

        elif num == 3:
            current_password = self.hidden_password.cget("text")

            if current_password == "-":
                new_password = simpledialog.askstring("Input", "Enter your new password:")
                self.password_label.configure(text=("*" * len(new_password)))
                self.hidden_password.configure(text=new_password)
                current_password = new_password

            else:
                confirm_password = simpledialog.askstring("Input", "Enter your previous password:")
                if confirm_password == current_password:
                    new_password = simpledialog.askstring("Input", "Enter your new password:")
                    if new_password == current_password:
                        messagebox.showerror("Error", "New password must be different from previous password")
                    else:
                        current_password = new_password
                        self.password_label.configure(text=("*" * len(current_password)))
                        self.hidden_password.configure(text=new_password)
                else:
                    messagebox.showerror("Error", "Password is Incorrect")

userSetting()
