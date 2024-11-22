import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from sql_connection import getsqlconnection
from User_Setting import UserSetting

class AddProductPage():
    def __init__(self, seller_id, homepageroot):
        self.root = tk.Tk()
        self.root.title("Add Product Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        self.seller_id = seller_id
        self.homepage_root = homepageroot
        self.connection = getsqlconnection()

        yourShopText = tk.Label(self.root, text="ADD PRODUCT", font='Lato 24 bold', bg='#C4DAD2')
        yourShopText.place(x=32, y=33)

        self.image4 = tk.PhotoImage(file='icons/settingIcon.png')
        self.settingButton = tk.Button(self.root, image=self.image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton.place(x=1193, y=29, width=48, height=48)

        self.backButton = tk.Button(self.root, command=self.goBack, bg="#5B8676", fg="white", text='Back', font='Lato 20 bold')
        self.backButton.place(x=40, y=629, width=136, height=60)

        self.okButton = tk.Button(self.root, command=self.okClicked, bg="#5B8676", fg="white", text='OK', font='Lato 20 bold')
        self.okButton.place(x=1141, y=621, width=100, height=60)

        self.productframe = tk.Frame(self.root, bg='#C4DAD2')
        self.productframe.place(x=52, y=101, width=690, height=490)

        self.canvas = tk.Canvas(self.productframe, bg="#C4DAD2", highlightthickness=0)
        scrollableFrame = tk.Frame(self.canvas, bg="#C4DAD2")

        scrollbar = tk.Scrollbar(self.productframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        scrollableFrame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.entries = []
        self.entry_title = ['Product Name', 'Price', 'Product Description', 'Remaining Stock', 'Category']
        self.keys = ['productName','productPrice','productDescription','remainingStock','category','productImage']
        self.product_dict = dict.fromkeys(self.keys)
        self.product_dict['productImage'] ='placeholder.png'

        for e in self.entry_title:
            label = tk.Label(scrollableFrame, text=e, font='Lato 16 bold', bg='#C4DAD2')
            label.pack(pady=(5, 5), anchor='w')  

            if e == 'Product Description':
                text_area = tk.Text(scrollableFrame, height=10, width=50, font=('Lato', 14), wrap='word', bg='white', fg='black')
                text_area.pack(pady=(0, 20), anchor='w')
                self.entries.append(text_area)
            else:
                entry = tk.Entry(scrollableFrame, background='white', foreground='black', font=('Lato', 16), width=50)
                entry.pack(pady=(0, 20), anchor='w')  
                self.entries.append(entry)


        imageProductTitle = tk.Label(self.root, text='Product Image', font='Lato 16 bold', bg='#C4DAD2', fg='black')
        imageProductTitle.place(x=935, y=170, anchor='w')

        img = Image.open("images/placeholder.png")
        img = img.resize((300,200))
        photoImg =  ImageTk.PhotoImage(img)
        self.imageCut = tk.Label(self.root, image=photoImg)
        self.imageCut.place(x=860, y=300, anchor='w')

        self.editImgButton = tk.Button(self.root, command=self.editImage, bg="#5B8676", fg="white", text='Edit', font='Lato 14 bold')
        self.editImgButton.place(x=980, y=411, width=70, height=40)

        self.root.mainloop()


    def editImage(self):
        self.file_name = filedialog.askopenfilename()
        if not self.file_name.lower().endswith(('.jpeg', '.jpg', '.png')):
            messagebox.showerror("Error", "File types must be of the jpg or png type")
        else:
            images_folder = "images"
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)
            
            basefilename = os.path.basename(self.file_name)
            dest_path = os.path.join(images_folder, basefilename)
            shutil.copy(self.file_name, dest_path)

            product_image = Image.open(dest_path)
            self.product_image = product_image.resize((300, 200))
            self.product_image = ImageTk.PhotoImage(self.product_image)
            self.imageCut = tk.Label(self.root, image=self.product_image)
            self.imageCut.place(x=860, y=300, anchor='w')

            self.product_dict['productImage'] = basefilename

    def okClicked(self):
        for i, entry in enumerate(self.entries):
            if isinstance(entry, tk.Text):
                self.product_dict[self.keys[i]] = entry.get("1.0", tk.END).strip()
            else:
                self.product_dict[self.keys[i]] = entry.get().strip()

        for i, (key, val) in enumerate(self.product_dict.items()):
            if not val:  # Empty value
                messagebox.showerror('Error', f'{self.entry_title[i]} cannot be empty.')
                return  # Exit if any field is empty
        
        try:
            if self.product_dict['productPrice']:
                self.product_dict['productPrice'] = float(self.product_dict['productPrice'])
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number.")
            return

        try:
            if self.product_dict['remainingStock']:
                self.product_dict['remainingStock'] = int(self.product_dict['remainingStock'])
        except ValueError:
            messagebox.showerror("Error", "Remaining stock must be an integer.")
            return

        category_id = self.get_categoryID(self.product_dict['category'])
        del self.product_dict['category']
        self.product_dict['categoryID'] = category_id

        self.product_dict['sellerID'] =self.seller_id
        columns = ', '.join(self.product_dict.keys())
        placeholders = ', '.join(['%s'] * len(self.product_dict))
        query = f"INSERT INTO product ({columns}) VALUES ({placeholders})"

        cursor = self.connection.cursor()
        cursor.execute(query, tuple(self.product_dict.values()))
        self.connection.commit()

        messagebox.showinfo("Success", "Product added successfully.")
        self.root.destroy()
        self.homepage_root.__class__(self.seller_id)



    def goBack(self):
        self.root.destroy()
        self.homepage_root.__class__(self.seller_id)

    def goToSetting(self):
        self.root.destroy()
        UserSetting(self.seller_id, self.homepage_root)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def get_categoryID(self, categoryName):
        cursor =self.connection.cursor()
        cursor.execute("SELECT categoryID FROM category WHERE categoryName = %s", (categoryName,))
        category_id_result = cursor.fetchone()
        
        if category_id_result:
            category_id = category_id_result[0]
            return category_id
        else:
            cursor.execute("INSERT INTO category (categoryName) VALUES (%s)", (categoryName,))
            self.connection.commit()
            cursor.execute("SELECT categoryID FROM category WHERE categoryName = %s", (categoryName,))
            category_id = cursor.fetchone()[0]
            return category_id

