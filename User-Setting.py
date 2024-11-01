import tkinter as tk
from tkinter import font
from tkinter import simpledialog, messagebox

def to_root_1():
    root2.withdraw()
    root.deiconify()

def to_root_2():
    root.withdraw()
    root2.deiconify()

def end():
    root.destroy()
    root2.destroy()

def change(num):

    if num == 1:
        new_email = simpledialog.askstring("Input", "Enter the new email:")
        if new_email:
            email_label.configure(text=new_email)
        root.deiconify()

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
            phone_label.configure(text=new_phone_number)

    elif num == 3:
        current_password = hidden_password.cget("text")

        if current_password == "-":
            new_password = simpledialog.askstring("Input", "Enter your new password:")
            password_label.configure(text=("*" * len(new_password)))
            hidden_password.configure(text=new_password)
            current_password = new_password

        else:
            confirm_password = simpledialog.askstring("Input", "Enter your previous password:")
            if confirm_password == current_password:
                new_password = simpledialog.askstring("Input", "Enter your new password:")
                if new_password == current_password:
                    messagebox.showerror("Error", "New password must be different from previous password")
                else:
                    current_password = new_password
                    password_label.configure(text=("*" * len(current_password)))
                    hidden_password.configure(text=new_password)
            else:
                messagebox.showerror("Error", "Password is Incorrect")


root = tk.Tk()
root.title("User Setting")

root.configure(bg="#C4DAD2")
root.geometry("1280x720")
root.protocol("WM_DELETE_WINDOW", end)

title_font = font.Font(size=30, weight="bold")

user_setting = tk.Label(root, text="USER SETTING", font=title_font, bg="#C4DAD2")
user_setting.place(x=100, y=50)

canvas = tk.Canvas(root, width=200, height=200, bg="#C4DAD2", highlightthickness=0)
canvas.place(x=545, y=183)

canvas.create_oval(0, 20, 40, 60, fill="#FFFFFF")

normal_text = font.Font(size=15)

full_name = tk.Label(root, text="Newbie Martinez", font=normal_text, bg="#C4DAD2")
full_name.place(x=600, y=210)

ID = tk.Label(root, text="ID", font=normal_text, bg="#C4DAD2")
ID.place(x=550, y=270)

ID_frame = tk.Frame(root, width=220, height=25, bg="#FFFFFF")
ID_frame.place(x=600, y=270)

ID_label = tk.Label(ID_frame, text="CUS-019721679", bg="#FFFFFF")
ID_label.place(x=5, y=3)

email = tk.Label(root, text="Email", font=normal_text, bg="#C4DAD2")
email.place(x=521, y=322)

email_frame = tk.Frame(root, width=220, height=25, bg="#FFFFFF")
email_frame.place(x=600, y=322)

change_font = font.Font(size=8)

email_label = tk.Label(email_frame, text="-", bg="#FFFFFF")
email_label.place(x=5, y=3)

change1 = tk.Label(root, text="Change", font=change_font, bg="#C4DAD2", fg="#0000EE")
change1.place(x=830, y=325)
change1.bind("<Button-1>", lambda event: change(1))

phoneNumber = tk.Label(root, text="Phone Number", font=normal_text, bg="#C4DAD2")
phoneNumber.place(x=443, y=374)

change2 = tk.Label(root, text="Change", font=change_font, bg="#C4DAD2", fg="#0000EE")
change2.place(x=830, y=377)
change2.bind("<Button-1>", lambda event: change(2))

phoneNumber_frame = tk.Frame(root, width=220, height=25, bg="#FFFFFF")
phoneNumber_frame.place(x=600, y=374)

phone_label = tk.Label(phoneNumber_frame, text="-", bg="#FFFFFF")
phone_label.place(x=5, y=3)

password = tk.Label(root, text="Password", font=normal_text, bg="#C4DAD2")
password.place(x=483, y=426)

password_frame = tk.Frame(root, width=220, height=25, bg="#FFFFFF")
password_frame.place(x=600, y=425)

password_label = tk.Label(password_frame, text="-", bg="#FFFFFF")
password_label.place(x=5, y=3)
hidden_password = tk.Label(root, text="-")
hidden_password.place(x=-1000, y= 199)

change3 = tk.Label(root, text="Change", font=change_font, bg="#C4DAD2", fg="#0000EE")
change3.place(x=830, y=428)
change3.bind("<Button-1>", lambda event: change(3))

backButton = tk.Button(root, width=15, height=3, text="Back", fg="#FFFFFF", bg="#5B8676")
backButton.place(x=110, y=500)

userBiodata = tk.Button(root, width=17, height=2, text="User Biodata", fg="#FFFFFF", bg="#5B8676", command=to_root_1)
userBiodata.place(x=110, y=250)

paymentAccounts = tk.Button(root, width=17, height=2, text="Payment Accounts", bg="#C4DAD2", command=to_root_2)
paymentAccounts.place(x=110, y=290)

root2 = tk.Toplevel()
root2.title("User Setting")
root2.withdraw()

root2.configure(bg="#C4DAD2")
root2.geometry("1280x720")
root2.protocol("WM_DELETE_WINDOW", end)

title_font = font.Font(size=30, weight="bold")

user_setting = tk.Label(root2, text="USER SETTING", font=title_font, bg="#C4DAD2")
user_setting.place(x=100, y=50)

normal_text = font.Font(size=15)

BCA = tk.Label(root2, text="BCA", font=normal_text, bg="#C4DAD2")
BCA.place(x=523, y=270)

BCA_frame = tk.Frame(root2, width=220, height=25, bg="#FFFFFF")
BCA_frame.place(x=600, y=270)

BCA_label = tk.Label(BCA_frame, text="-", bg="#FFFFFF")
BCA_label.place(x=5, y=3)

OVO = tk.Label(root2, text="OVO", font=normal_text, bg="#C4DAD2")
OVO.place(x=521, y=322)

OVO_frame = tk.Frame(root2, width=220, height=25, bg="#FFFFFF")
OVO_frame.place(x=600, y=322)

OVO_label = tk.Label(OVO_frame, text="-", bg="#FFFFFF")
OVO_label.place(x=5, y=3)

GOPAY = tk.Label(root2, text="GOPAY", font=normal_text, bg="#C4DAD2")
GOPAY.place(x=495, y=374)

GOPAY_frame = tk.Frame(root2, width=220, height=25, bg="#FFFFFF")
GOPAY_frame.place(x=600, y=374)

GOPAY_label = tk.Label(GOPAY_frame, text="-", bg="#FFFFFF")
GOPAY_label.place(x=5, y=3)

BNI = tk.Label(root2, text="BNI", font=normal_text, bg="#C4DAD2")
BNI.place(x=531, y=426)

BNI_frame = tk.Frame(root2, width=220, height=25, bg="#FFFFFF")
BNI_frame.place(x=600, y=425)

BNI_label = tk.Label(BNI_frame, text="-", bg="#FFFFFF")
BNI_label.place(x=5, y=3)

link_font = font.Font(size=10)

link1 = tk.Label(root2, text="Link", font=link_font, bg="#C4DAD2", fg="#0000EE")
link1.place(x=830, y=325)

link2 = tk.Label(root2, text="Link", font=link_font, bg="#C4DAD2", fg="#0000EE")
link2.place(x=830, y=377)

link3 = tk.Label(root2, text="Link", font=link_font, bg="#C4DAD2", fg="#0000EE")
link3.place(x=830, y=428)

backButton = tk.Button(root2, width=15, height=3, text="Back", fg="#FFFFFF", bg="#5B8676")
backButton.place(x=110, y=500)

userBiodata = tk.Button(root2, width=17, height=2, text="User Biodata", bg ="#C4DAD2", command=to_root_1)
userBiodata.place(x=110, y=250)

paymentAccounts = tk.Button(root2, width=17, height=2, text="Payment Accounts", fg="#FFFFFF", bg="#5B8676", command=to_root_2)
paymentAccounts.place(x=110, y=290)

root.mainloop()