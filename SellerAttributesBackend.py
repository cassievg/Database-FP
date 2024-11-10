import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import mysql.connector

def get_connection():
    global connection
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"
    )
    return connection

cursor = get_connection().cursor()

# Ensuring a new clean database
cursor.execute("DROP DATABASE IF EXISTS `onlinestore`")
cursor.execute("CREATE DATABASE `onlinestore`")

cursor.execute("""
CREATE TABLE IF NOT EXISTS`onlinestore`.`user` (
    `userID` INT NOT NULL AUTO_INCREMENT,
    `userType` VARCHAR(10) NOT NULL,
    `fName` VARCHAR(50) NOT NULL,
    `lName` VARCHAR(50) NOT NULL,
    `address` VARCHAR(255) NOT NULL,
    `phoneNumber` VARCHAR(15) NOT NULL,
    `password` VARCHAR(45) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`userID`)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS `onlinestore`.`category` (
    `categoryID` INT NOT NULL AUTO_INCREMENT,
    `categoryName` VARCHAR(60) NOT NULL,
    PRIMARY KEY (`categoryID`)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS `onlinestore`.`product` (
    `productID` INT NOT NULL AUTO_INCREMENT,
    `productName` VARCHAR(255) NOT NULL,
    `productPrice` FLOAT NOT NULL,
    `productImage` VARCHAR(255) NOT NULL,
    `productDescription` VARCHAR(500) NOT NULL,
    `remainingStock` INT NOT NULL,
    `categoryID` INT NOT NULL,
    `sellerID` INT NOT NULL,
    PRIMARY KEY (`productID`),
    INDEX `fk_categoryID_idx` (`categoryID` ASC) VISIBLE,
    INDEX `fk_sellerID_idx` (`sellerID` ASC) VISIBLE,
    CONSTRAINT `fk_categoryID`
        FOREIGN KEY (`categoryID`)
        REFERENCES `onlinestore`.`category` (`categoryID`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `fk_sellerID`
        FOREIGN KEY (`sellerID`)
        REFERENCES `onlinestore`.`user` (`userID`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
""")

class SellerAttributes():
    def __init__(self):
        self.root1 = tk.Tk()
        self.root1.title("Seller Home Page")
        self.root1.configure(bg="#C4DAD2")
        self.root1.geometry('1280x720')
        self.root1.protocol("WM_END_WINDOW", self.end)

        yourShopText1 = tk.Label(self.root1, text="YOUR SHOP", font='Lato 24 bold', bg='#C4DAD2')
        yourShopText1.place(x=32, y=33)

        image4 = tk.PhotoImage(file="icons\settingIcon.png")
        self.settingButton1 = tk.Button(self.root1, image=image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton1.place(x=1193, y=29, width=48, height=48)

        self.addButton1 = tk.Button(self.root1, command=self.addProduct, bg="#5B8676", fg="white", text='Add Product', font='Lato 16 bold')
        self.addButton1.place(x=561, y=641, width=180, height=50)

        self.shopFrame1 = tk.Frame(self.root1, bg='#C4DAD2')
        self.shopFrame1.place(x=52, y=101, width=1190, height=121)

        self.canvas1 = tk.Canvas(self.shopFrame1, bg="#C4DAD2", highlightthickness=1, highlightbackground='black')
        self.canvas1.pack(side="left", fill="both", expand=True)

        sellerName1 = tk.Label(self.shopFrame1, text="Seller Name", font='Lato 20 bold', bg='#C4DAD2')
        sellerName1.place(x=508, y=20)

        sellerAddress1 = tk.Label(self.shopFrame1, text="Seller Address", font='Lato 16', bg='#C4DAD2')
        sellerAddress1.place(x=518, y=70)

        self.searchbarField1 = tk.Entry(self.root1, background='white', foreground='black', font=('Lato', 14), width=15)
        self.searchbarField1.place(x=310, y=240, width=600, height=40)

        image2 = tk.PhotoImage(file="icons\searchIcon.png")
        self.searchButton1 = tk.Button(self.root1, image=image2, command=self.search, bg="#C4DAD2", fg="white")
        self.searchButton1.place(x=925, y=240, width=40, height=40)

        self.productframe1 = tk.Frame(self.root1, bg='#C4DAD2')
        self.productframe1.place(x=52, y=310, width=1190, height=300)

        self.canvas1 = tk.Canvas(self.productframe1, bg="#C4DAD2", highlightthickness=0)
        self.scrollableFrame1 = tk.Frame(self.canvas1, bg="#C4DAD2")

        self.scrollbar1 = tk.Scrollbar(self.productframe1, orient="vertical", command=self.canvas1.yview)
        self.canvas1.configure(yscrollcommand=self.scrollbar1.set)

        self.canvas1.pack(side="left", fill="both", expand=True)
        self.scrollbar1.pack(side="right", fill="y")

        self.canvas1.create_window((0, 0), window=self.scrollableFrame1, anchor="nw")
        self.scrollableFrame1.bind("<Configure>", self.on_frame_configure)
        self.canvas1.bind_all("<MouseWheel>", self._on_mouse_wheel)

        cursor.execute("SELECT * FROM `onlinestore`.`product`")
        products = cursor.fetchall()
        
        self.product_images = []
        self.names = []
        self.prices = []
        self.image_paths = []
        self.descriptions = []
        for product in products:
            self.names.append(product[1])
            self.prices.append(product[2])
            image_path = product[3]
            self.image_paths.append(image_path)
            self.descriptions.append(product[4])

        self.display_product(self.names)

        self.root2 = tk.Toplevel()
        self.root2.withdraw()
        self.root2.title("Add Product Page")
        self.root2.configure(bg="#C4DAD2")
        self.root2.geometry('1280x720')
        self.root2.protocol("WM_END_WINDOW", self.end)

        yourShopText2 = tk.Label(self.root2, text="ADD PRODUCT", font='Lato 24 bold', bg='#C4DAD2')
        yourShopText2.place(x=32, y=33)

        self.image4 = tk.PhotoImage(file="icons\settingIcon.png")
        self.settingButton2 = tk.Button(self.root2, image=self.image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton2.place(x=1193, y=29, width=48, height=48)

        self.backButton2 = tk.Button(self.root2, command=self.goBack, bg="#5B8676", fg="white", text='Back', font='Lato 20 bold')
        self.backButton2.place(x=40, y=629, width=136, height=60)

        self.okButton2 = tk.Button(self.root2, command=self.okClicked, bg="#5B8676", fg="white", text='OK', font='Lato 20 bold')
        self.okButton2.place(x=1141, y=621, width=100, height=60)
        
        self.productframe2 = tk.Frame(self.root2, bg='#C4DAD2')
        self.productframe2.place(x=52, y=101, width=690, height=490)

        self.canvas2 = tk.Canvas(self.productframe2, bg="#C4DAD2", highlightthickness=0)
        scrollableFrame2 = tk.Frame(self.canvas2, bg="#C4DAD2")

        scrollbar2 = tk.Scrollbar(self.productframe2, orient="vertical", command=self.canvas2.yview)
        self.canvas2.configure(yscrollcommand=scrollbar2.set)

        self.canvas2.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")

        self.canvas2.create_window((0, 0), window=scrollableFrame2, anchor="nw")
        scrollableFrame2.bind("<Configure>", self.on_frame_configure1)
        self.canvas2.bind_all("<MouseWheel>", self._on_mouse_wheel1)

        self.entries2 = []
        self.entry_title2 = ['Product Name', 'Price', 'Product Description', 'Remaining Stock', 'Category']

        for e in self.entry_title2:
            label = tk.Label(scrollableFrame2, text=e, font='Lato 16 bold', bg='#C4DAD2')
            label.pack(pady=(5, 5), anchor='w')  

            if e == 'Product Description':
                text_area = tk.Text(scrollableFrame2, height=10, width=50, font=('Lato', 14), wrap='word', bg='white', fg='black')
                text_area.pack(pady=(0, 20), anchor='w')
                text_area.insert('1.0', "Enter your text here...")
                self.entries2.append(text_area)
            else:
                entry = tk.Entry(scrollableFrame2, background='white', foreground='black', font=('Lato', 16), width=50)
                entry.pack(pady=(0, 20), anchor='w')  
                self.entries2.append(entry)


        imageProductTitle2 = tk.Label(self.root2, text='Product Image', font='Lato 16 bold', bg='#C4DAD2', fg='black')
        imageProductTitle2.place(x=935, y=170, anchor='w')
        
        img2 = Image.open("icons\placeholder.png")
        img2 = img2.resize((300,200))
        self.placeholder2 =  ImageTk.PhotoImage(img2) 
        self.imageCut2 = tk.Label(self.root2, image=self.placeholder2)
        self.imageCut2.place(x=860, y=300, anchor='w')

        self.editImgButton = tk.Button(self.root2, command= lambda: self.editImage1(), bg="#5B8676", fg="white", text='Edit', font='Lato 14 bold')
        self.editImgButton.place(x=980, y=411, width=70, height=40)

        self.root3 = tk.Toplevel()
        self.root3.withdraw()
        self.root3.title("Edit Product Page")
        self.root3.configure(bg="#C4DAD2")
        self.root3.geometry('1280x720')
        self.root3.protocol("WM_END_WINDOW", self.end)

        yourShopText3 = tk.Label(self.root3, text="EDIT PRODUCT", font='Lato 24 bold', bg='#C4DAD2')
        yourShopText3.place(x=32, y=33)

        self.image4 = tk.PhotoImage(file="icons\settingIcon.png")
        self.settingButton3 = tk.Button(self.root3, image=self.image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton3.place(x=1193, y=29, width=48, height=48)

        self.backButton3 = tk.Button(self.root3, command=self.goBack, bg="#5B8676", fg="white", text='Back', font='Lato 20 bold')
        self.backButton3.place(x=40, y=629, width=136, height=60)
        
        self.productframe3 = tk.Frame(self.root3, bg='#C4DAD2')
        self.productframe3.place(x=512, y=101, width=690, height=490)

        self.canvas3 = tk.Canvas(self.productframe3, bg="#C4DAD2", highlightthickness=0)
        scrollableFrame3 = tk.Frame(self.canvas3, bg="#C4DAD2")

        scrollbar3 = tk.Scrollbar(self.productframe3, orient="vertical", command=self.canvas3.yview)
        self.canvas3.configure(yscrollcommand=scrollbar3.set)

        self.canvas3.pack(side="left", fill="both", expand=True)
        scrollbar3.pack(side="right", fill="y")

        self.canvas3.create_window((0, 0), window=scrollableFrame3, anchor="nw")
        scrollableFrame3.bind("<Configure>", self.on_frame_configure2)
        self.canvas3.bind_all("<MouseWheel>", self._on_mouse_wheel2)

        self.entries3 = []
        self.entry_title3 = ['Product Name', 'Price', 'Product Description', 'Remaining Stock', 'Category']

        for i in range(len(self.entry_title3)):
            e = self.entry_title3[i]

            label_frame3 = tk.Frame(scrollableFrame3, bg='#C4DAD2')
            label_frame3.pack(pady=(5, 5), anchor='w')

            label3 = tk.Label(label_frame3, text=e, font='Lato 16 bold', bg='#C4DAD2')
            label3.pack(side='left')

            changelabel3 = tk.Label(label_frame3, text="Change", font='Lato 12 bold', bg="#C4DAD2", fg="#0000EE", cursor="hand2")
            changelabel3.pack(side='left', padx=10)
            changelabel3.bind("<Button-1>", lambda event, i=i: self.change(i))

            if e == 'Product Description':
                text_area3 = tk.Text(scrollableFrame3, height=10, width=50, font=('Lato', 14), wrap='word', bg='white', fg='black')
                text_area3.pack(pady=(0, 20), anchor='w')
                self.entries3.append(text_area3)
            else:
                entry3 = tk.Entry(scrollableFrame3, background='white', foreground='black', font=('Lato', 16), width=50)
                entry3.pack(pady=(0, 20), anchor='w')
                self.entries3.append(entry3)

        imageProductTitle3 = tk.Label(self.root3, text='Product Image', font='Lato 16 bold', bg='#C4DAD2', fg='black')
        imageProductTitle3.place(x=120, y=170, anchor='w')
        
        self.editImgButton3 = tk.Button(self.root3, command= lambda: self.editImage2(), bg="#5B8676", fg="white", text='Edit', font='Lato 14 bold')
        self.editImgButton3.place(x=152, y=411, width=70, height=40)

        self.root1.mainloop()

    def editImage1(self):
        self.file_name = filedialog.askopenfilename()
        if not self.file_name.lower().endswith(('.jpg', '.png')):
            messagebox.showerror("Error","File types must be of the jpg or png type")
        else:
            product_image = Image.open(self.file_name)
            self.product_image = product_image.resize((300,200))
            self.product_image = ImageTk.PhotoImage(self.product_image)

            self.imageCut = tk.Label(self.root2, image=self.product_image)
            self.imageCut.place(x=860, y=300, anchor='w')

    def editImage2(self):
        self.file_name = filedialog.askopenfilename()
        if not self.file_name.lower().endswith(('.jpg', '.png')):
            messagebox.showerror("Error","File types must be of the jpg or png type")
        else:
            product_image = Image.open(self.file_name)
            self.product_image = product_image.resize((300,200))
            self.product_image = ImageTk.PhotoImage(self.product_image)

            self.imageCut = tk.Label(self.root3, image=self.product_image)
            self.imageCut.place(x=52, y=300, anchor='w')
            cursor.execute("UPDATE `onlinestore`.`product` SET `productImage` = %s WHERE `productName` = %s", (self.file_name, self.current_editing_product))


    def clear_entries(self):    
        for entry in self.entries2:
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.Text):
                entry.delete("1.0", tk.END)
                entry.insert('1.0', "Enter your text here...")
            self.imageCut = tk.Label(self.root2, image=self.placeholder2)
            self.imageCut.place(x=860, y=300, anchor='w')
        
    def okClicked(self):
        try:
            productName = self.entries2[0].get()
            price = float(self.entries2[1].get())
            productDescription = self.entries2[2].get("1.0", "end-1c")
            stock = int(self.entries2[3].get())
            category = self.entries2[4].get()
            sellerID = 1

            add_product(productName, price, self.file_name, productDescription, stock, category, sellerID)
            messagebox.showinfo("Updated!", "Product added successfully!")
        except:
            messagebox.showerror("Error", "Please make sure you filled all fields, and validate each input")
        finally:
            self.clear_entries()

        
    def edit_product(self, name):
        
        # Name [1] Price [2] Image [3] Description [4] Stock [5] categoryID [6]
        cursor.execute("SELECT * FROM `onlinestore`.`product` WHERE `productName` = %s", (name,))
        products = cursor.fetchone()
        self.entries3[0].insert(0, products[1])
        self.entries3[1].insert(0, products[2])
        self.entries3[2].insert("1.0", products[4])
        self.entries3[3].insert(0, products[5])
        categoryID = products[6]
        categoryName = get_categoryName(categoryID)
        self.entries3[4].insert(0, categoryName)

        self.current_editing_product = products[1]

        self.productEdit_image_path = os.path.abspath(products[3])
        self.productEdit_image = Image.open(self.productEdit_image_path)
        self.productEdit_image = self.productEdit_image.resize((300,200))
        self.productEdit_image = ImageTk.PhotoImage(self.productEdit_image)
        self.imageCut3 = tk.Label(self.root3, image=self.productEdit_image)
        self.imageCut3.place(x=52, y=300, anchor='w')

        self.root1.withdraw()
        self.root3.deiconify()

    def delete_product(self, name):
        cursor.execute("DELETE FROM `onlinestore`.`product` WHERE `productName` = %s", (name,))
        self.root1.destroy()
        SellerAttributes()

    def display_product(self, names):

        for widget in self.scrollableFrame1.winfo_children():
            widget.destroy()

        if names[0] == "":
            names = self.names
        
        for name1 in names:
            count = 0
            for name2 in self.names:
                if name1.lower() == name2.lower():
                    product_canvas = tk.Canvas(self.scrollableFrame1, width=1130, height=150, bg="white", highlightthickness=0)
                    product_canvas.grid(padx=25, pady=20)

                    images = Image.open(self.image_paths[count])
                    images = images.resize((130,100))
                    product_image = ImageTk.PhotoImage(images)
                    self.product_images.append(product_image)
                    product_canvas.create_image(130, 70, image=product_image)

                    product_canvas.create_text(230, 35, text=self.names[count], font='Lato 16 bold', fill='black', anchor='w')
                    product_canvas.create_text(230, 70, text=self.prices[count], font='Lato 14', fill='grey', anchor='w')

                    delete_button = tk.Button(self.scrollableFrame1, text="X", command=lambda name = self.names[count]: self.delete_product(name), width=3, bg='lightcoral', font='Lato 14 bold')
                    product_canvas.create_window(1100, 25, window=delete_button)

                    edit_button = tk.Button(self.scrollableFrame1, text="Edit", command=lambda namess = self.names[count]: self.edit_product(namess), width=3, bg='lightgray', font='Lato 14 bold')
                    product_canvas.create_window(1070, 110, window=edit_button, width=100)
                count += 1


    def goToSetting(self):
        print("Going to settings...")

    def addProduct(self):
        self.root1.withdraw()
        self.root2.deiconify()

    def change(self, num):
        if num == 0:
            new_name = self.entries3[0].get()
            cursor.execute("UPDATE `onlinestore`.`product` SET `productName` = %s WHERE `productName` = %s", (new_name, self.current_editing_product))
            self.current_editing_product = new_name
            messagebox.showinfo("Name Change", f"Product name has been changed from {self.current_editing_product} to {new_name}")

        if num == 1:
            new_price = self.entries3[1].get()
            cursor.execute("UPDATE `onlinestore`.`product` SET `productPrice` = %s WHERE `productName` = %s", (new_price, self.current_editing_product))
            messagebox.showinfo("Price Change", f"Product name has been changed to {new_price}")

        if num == 2:
            new_description = self.entries3[2].get("1.0", "end-1c")
            cursor.execute("UPDATE `onlinestore`.`product` SET `productDescription` = %s WHERE `productName` = %s", (new_description, self.current_editing_product))
            messagebox.showinfo("Description Change", f"Product description has been changed to {new_description}")

        if num == 3:
            new_stock = self.entries3[3].get()
            cursor.execute("UPDATE `onlinestore`.`product` SET `remainingStock` = %s WHERE `productName` = %s", (new_stock, self.current_editing_product))
            messagebox.showinfo("Stock Change", f"Stock has been changed to {new_stock}")

        if num == 4:
            new_category = self.entries3[4].get()
            new_categoryID = get_categoryID(new_category)
            cursor.execute("UPDATE `onlinestore`.`product` SET `categoryID` = %s WHERE `productName` = %s", (new_categoryID, self.current_editing_product))
            messagebox.showinfo("Category Change", f"Category has been updated!")

    def search(self):
        product_searched = self.searchbarField1.get()
        self.display_product([product_searched])

    def on_frame_configure(self, event):
            self.canvas1.configure(scrollregion=self.canvas1.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas1.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_frame_configure1(self, event):
        self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))

    def _on_mouse_wheel1(self, event):
        self.canvas2.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_frame_configure2(self, event):
        self.canvas3.configure(scrollregion=self.canvas2.bbox("all"))

    def _on_mouse_wheel2(self, event):
        self.canvas3.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def goBack(self):
        self.root2.withdraw()
        self.root3.withdraw()
        self.root1.destroy()
        SellerAttributes()

    def end(self):
        self.root1.destroy()
        self.root2.destroy()
        self.root3.destroy()

def display_table(tableName):
    cursor.execute(f"SELECT * FROM `onlinestore`.`{tableName}`")
    products = cursor.fetchall()

    for product in products:
        print(product)

def get_categoryID(categoryName):
    categoryID = 0
    cursor.execute("SELECT (`categoryID`) FROM `onlinestore`.`category` WHERE categoryName = %s", (categoryName,))
    products = cursor.fetchone()
    try:
        for product in products:
            categoryID = product
    except:
            cursor.execute("INSERT INTO `onlinestore`.`category` (`categoryName`) VALUES (%s);", (categoryName,))
            cursor.execute("SELECT (`categoryID`) FROM `onlinestore`.`category` WHERE categoryName = %s", (categoryName,))
            products = cursor.fetchone()
            categoryID = products[0]

    return categoryID

def get_categoryName(categoryID):
    categoryName = ""
    cursor.execute("SELECT (`categoryName`) FROM `onlinestore`.`category` WHERE categoryID = %s", (categoryID,))
    products = cursor.fetchone()
    categoryName = products[0]
    return categoryName

def add_product(productName, productPrice, productImage, productDescription, remainingStock, categoryName, sellerID):
    category_ID = get_categoryID(categoryName)

    cursor.execute("""
        INSERT INTO `onlinestore`.`product` (`productName`, `productPrice`, `productImage`, `productDescription`, `remainingStock`, `categoryID`, `sellerID`)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s);
    """, (productName, productPrice, productImage, productDescription, remainingStock, category_ID, sellerID))


# Adding Default User
cursor.execute("""
    INSERT INTO `onlinestore`.`user` (`userType`, `fName`, `lName`, `address`, `phoneNumber`, `password`, `email`)
    VALUES ("Seller", "Rafael", "Anderson", "FX Sudirman", "0812971409132", "password", "email@gmail.com");
""")

# Default Products
add_product("Table", 50.000, "icons\placeholder.png", "None", 1, "Furniture", 1)
add_product("Chair", 52.000, "icons\placeholder.png", "None", 1, "Furniture", 1)
add_product("T-Shirt", 43.000, "icons\placeholder.png", "None", 1, "Clothing", 1)
add_product("Paper", 14.000, "icons\placeholder.png", "None", 1, "Stationery", 1)
add_product("Bracelet", 50.000, "icons\placeholder.png", "None", 1, "Accessories", 1)
add_product("Necklace", 50.000, "icons\placeholder.png", "None", 1, "Accessories", 1)
add_product("Wallet", 50.000, "icons\placeholder.png", "None", 1, "Accessories", 1)
add_product("Mug", 50.000, "icons\placeholder.png", "None", 1, "Kitchenware", 1)

SellerAttributes()
