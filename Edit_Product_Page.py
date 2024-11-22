import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from sql_connection import getsqlconnection
from User_Setting import UserSetting

class EditProductPage():
    def __init__(self, seller_id, sellerhome, product_dict):
        self.root = tk.Tk()
        self.root.title("Edit Product Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        self.connection =getsqlconnection()
        self.seller_id = seller_id
        self.seller_home_root = sellerhome
        self.product_dict = product_dict

        yourShopText = tk.Label(self.root, text="EDIT PRODUCT", font='Lato 24 bold', bg='#C4DAD2')
        yourShopText.place(x=32, y=33)

        self.image4 = tk.PhotoImage(file='icons/settingIcon.png')
        self.settingButton = tk.Button(self.root, image=self.image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton.place(x=1193, y=29, width=48, height=48)

        self.backButton = tk.Button(self.root, command=self.goBack, bg="#5B8676", fg="white", text='Back', font='Lato 20 bold')
        self.backButton.place(x=40, y=629, width=136, height=60)
        
        self.productframe = tk.Frame(self.root, bg='#C4DAD2')
        self.productframe.place(x=512, y=101, width=690, height=490)

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
        self.dict_title = ['product_name','product_price','product_description','remaining_stock','category']
        self.query_title = ['productName','productPrice','productDescription','remainingStock','categoryID']
        self.product_dict['category'] = self.get_categoryName(self.product_dict['category_id'])

        for i in range(len(self.entry_title)):
            e = self.entry_title[i]
            d = self.dict_title[i]

            label_frame = tk.Frame(scrollableFrame, bg='#C4DAD2')
            label_frame.pack(pady=(5, 5), anchor='w')

            label = tk.Label(label_frame, text=e, font='Lato 16 bold', bg='#C4DAD2')
            label.pack(side='left')

            changelabel = tk.Label(label_frame, text="Change", font='Lato 12 bold', bg="#C4DAD2", fg="#0000EE", cursor="hand2")
            changelabel.pack(side='left', padx=10)
            changelabel.bind("<Button-1>", lambda event, i=i: self.change(i))

            if e == 'Product Description':
                text_area = tk.Text(scrollableFrame, height=10, width=50, font=('Lato', 14), wrap='word', bg='white', fg='black')
                text_area.pack(pady=(0, 20), anchor='w')
                text_area.insert('1.0', self.product_dict[d])
                text_area.config(state='disabled')
                self.entries.append(text_area)
            else:
                entry = tk.Entry(scrollableFrame, background='white', foreground='black', font=('Lato', 16), width=50)
                entry.pack(pady=(0, 20), anchor='w')
                entry.insert(0, self.product_dict[d])
                entry.config(state='readonly')
                self.entries.append(entry)

        imageProductTitle = tk.Label(self.root, text='Product Image', font='Lato 16 bold', bg='#C4DAD2', fg='black')
        imageProductTitle.place(x=120, y=170, anchor='w')
        
        img = Image.open(f"images/{self.product_dict['product_image']}")
        img = img.resize((300,200))
        photoImg =  ImageTk.PhotoImage(img)
        self.imageCut = tk.Label(self.root, image=photoImg)
        self.imageCut.place(x=52, y=300, anchor='w')

        self.editImgButton = tk.Button(self.root, command=self.editImage, bg="#5B8676", fg="white", text='Edit', font='Lato 14 bold')
        self.editImgButton.place(x=152, y=411, width=70, height=40)

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
            self.imageCut.place(x=52, y=300, anchor='w')

            cursor =self.connection.cursor()
            cursor.execute(f"UPDATE product SET productImage='{basefilename}' WHERE productID={self.product_dict['product_id']}")
            self.connection.commit()

    def goBack(self):
        self.root.destroy()
        self.seller_home_root.__class__(self.seller_id)

    def goToSetting(self):
        self.root.destroy()
        UserSetting(self.seller_id, self.seller_home_root)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def change(self, num):
        # self.entry_title = ['Product Name', 'Price', 'Product Description', 'Remaining Stock', 'Category']
        if num==1:
            newnum = simpledialog.askfloat('Input', 'Enter the new price:')
            if newnum:
                self.entries[num].delete(0, tk.END)
                self.entries[num].insert(0, str(newnum))
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE product SET productPrice={newnum} WHERE productID={self.product_dict['product_id']};")
            self.connection.commit()
            cursor.close()
        
        elif num==3:
            newnum = simpledialog.askinteger('Input', 'Enter the remaining stock:')
            if newnum:
                self.entries[num].delete(0, tk.END)
                self.entries[num].insert(0, str(newnum))
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE product SET remainingStock={newnum} WHERE productID={self.product_dict['product_id']};")
            self.connection.commit()
            cursor.close()
        
        else:
            titlequery = self.query_title[num] 
            print(titlequery)
            s = 'Enter the new '+ self.entry_title[num].lower()
            newinput = simpledialog.askstring('Input', s)
            if newinput:
                if num==2:
                    self.entries[num].delete("1.0", tk.END)
                    self.entries[num].insert("1.0", str(newinput))
                    cursor = self.connection.cursor()
                    cursor.execute(f"UPDATE product SET {titlequery}='{newinput}' WHERE productID={self.product_dict['product_id']};")
                    self.connection.commit()
                    cursor.close()
                else:
                    self.entries[num].delete(0, tk.END)
                    self.entries[num].insert(0, str(newinput))

                    if(num==4):
                        category_id = self.get_categoryID(newinput)
                        cursor = self.connection.cursor()
                        cursor.execute(f"UPDATE product SET {titlequery}={category_id} WHERE productID={self.product_dict['product_id']};")
                        self.connection.commit()
                    else:
                        cursor = self.connection.cursor()
                        cursor.execute(f"UPDATE product SET {titlequery}='{newinput}' WHERE productID={self.product_dict['product_id']};")
                        self.connection.commit()
                    cursor.close()


    def get_categoryName(self,categoryID):
        categoryName = ""
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT (`categoryName`) FROM `onlinestore`.`category` WHERE categoryID = {categoryID}")
        products = cursor.fetchone()
        categoryName = products[0]
        cursor.close()
        return categoryName
    
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


