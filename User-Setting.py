import tkinter as tk
from tkinter import font, simpledialog, messagebox
from sql_connection import getsqlconnection

class UserSetting:
    def __init__(self):
        self.connection = getsqlconnection()
        self.cursor = self.connection.cursor(dictionary=True)

        # Set to the user ID of the current user
        self.user_id = 1

        self.root = tk.Tk()
        self.root.title("User Setting")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry("1280x720")
        self.root.protocol("WM_DELETE_WINDOW", self.end)

        title_font = font.Font(size=30, weight="bold")
        normal_text = font.Font(size=15)
        change_font = font.Font(size=8)

        # Title
        self.user_setting = tk.Label(self.root, text="USER SETTING", font=title_font, bg="#C4DAD2")
        self.user_setting.place(x=100, y=50)

        # User details section
        self.full_name = tk.Label(self.root, text="Name: ", font=normal_text, bg="#C4DAD2")
        self.full_name.place(x=400, y=150)
        self.full_name_value = tk.Label(self.root, text="-", font=normal_text, bg="#C4DAD2")
        self.full_name_value.place(x=600, y=150)

        self.email_label = tk.Label(self.root, text="Email: ", font=normal_text, bg="#C4DAD2")
        self.email_label.place(x=400, y=200)
        self.email_value = tk.Label(self.root, text="-", font=normal_text, bg="#C4DAD2")
        self.email_value.place(x=600, y=200)

        self.change_email = tk.Button(self.root, text="Change", font=change_font, bg="#C4DAD2", command=lambda: self.change("email"))
        self.change_email.place(x=800, y=200)

        self.phone_label = tk.Label(self.root, text="Phone Number: ", font=normal_text, bg="#C4DAD2")
        self.phone_label.place(x=400, y=250)
        self.phone_value = tk.Label(self.root, text="-", font=normal_text, bg="#C4DAD2")
        self.phone_value.place(x=600, y=250)

        self.change_phone = tk.Button(self.root, text="Change", font=change_font, bg="#C4DAD2", command=lambda: self.change("phoneNumber"))
        self.change_phone.place(x=800, y=250)

        self.password_label = tk.Label(self.root, text="Password: ", font=normal_text, bg="#C4DAD2")
        self.password_label.place(x=400, y=300)
        self.password_value = tk.Label(self.root, text="********", font=normal_text, bg="#C4DAD2")
        self.password_value.place(x=600, y=300)

        self.change_password = tk.Button(self.root, text="Change", font=change_font, bg="#C4DAD2", command=lambda: self.change("password"))
        self.change_password.place(x=800, y=300)

        # Fetch user data
        self.fetch_user_data()

        self.root.mainloop()

    def fetch_user_data(self):
        try:
            query = "SELECT * FROM user WHERE userID = %s"
            self.cursor.execute(query, (self.user_id,))
            user_data = self.cursor.fetchone()

            if user_data:
                self.full_name_value.configure(text=f"{user_data['fName']} {user_data['lName']}")
                self.email_value.configure(text=user_data['email'])
                self.phone_value.configure(text=user_data['phoneNumber'])
            else:
                messagebox.showerror("Error", "User not found.")

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def change(self, field):
        try:
            if field == "email":
                new_value = simpledialog.askstring("Input", "Enter the new email:")
            elif field == "phoneNumber":
                new_value = simpledialog.askstring("Input", "Enter the new phone number:")
                if not new_value.isdigit():
                    messagebox.showerror("Error", "Phone number must contain only digits.")
                    return
            elif field == "password":
                new_value = simpledialog.askstring("Input", "Enter the new password:")
            else:
                return

            if new_value:
                query = f"UPDATE user SET {field} = %s WHERE userID = %s"
                self.cursor.execute(query, (new_value, self.user_id))
                self.connection.commit()
                messagebox.showinfo("Success", f"{field} updated successfully!")
                self.fetch_user_data()
                
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def end(self):
        self.cursor.close()
        self.connection.close()
        self.root.destroy()

if __name__ == "__main__":
    UserSetting()
