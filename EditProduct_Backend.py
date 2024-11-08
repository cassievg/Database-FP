import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

import mysql.connector

def get_connection():
    global connection
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="puputompoyay"
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

def display_table(tableName):
    cursor.execute(f"SELECT * FROM `onlinestore`.`{tableName}`")
    products = cursor.fetchall()

    for product in products:
        print(product)

def add_product(productName, productPrice, productImage, productDescription, remainingStock, categoryID, sellerID):
    cursor.execute("""
        INSERT INTO `onlinestore`.`product` (`productName`, `productPrice`, `productImage`, `productDescription`, `remainingStock`, `categoryID`, `sellerID`)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s);
    """, (productName, productPrice, productImage, productDescription, remainingStock, categoryID, sellerID))

# Adding Default User
cursor.execute("""
    INSERT INTO `onlinestore`.`user` (`userType`, `fName`, `lName`, `address`, `phoneNumber`, `password`, `email`)
    VALUES ("Seller", "Rafael", "Anderson", "FX Sudirman", "0812971409132", "password", "email@gmail.com");
""")

class AddProductPage():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Add Product Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        yourShopText = tk.Label(self.root, text="ADD PRODUCT", font='Lato 24 bold', bg='#C4DAD2')
        yourShopText.place(x=32, y=33)

        self.image4 = tk.PhotoImage(file=r"C:\Users\Rafael\OneDrive\Desktop\Uni\Programming Files\Mini Projects\Database Technology\icons\settingIcon.png")
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

        for e in self.entry_title:
            label = tk.Label(scrollableFrame, text=e, font='Lato 16 bold', bg='#C4DAD2')
            label.pack(pady=(5, 5), anchor='w')  

            if e == 'Product Description':
                text_area = tk.Text(scrollableFrame, height=10, width=50, font=('Lato', 14), wrap='word', bg='white', fg='black')
                text_area.pack(pady=(0, 20), anchor='w')
                text_area.insert('1.0', "Enter your text here...")
                self.entries.append(text_area)
            else:
                entry = tk.Entry(scrollableFrame, background='white', foreground='black', font=('Lato', 16), width=50)
                entry.pack(pady=(0, 20), anchor='w')  
                self.entries.append(entry)


        imageProductTitle = tk.Label(self.root, text='Product Image', font='Lato 16 bold', bg='#C4DAD2', fg='black')
        imageProductTitle.place(x=935, y=170, anchor='w')
        
        img = Image.open(r"C:\Users\Rafael\OneDrive\Desktop\Uni\Programming Files\Mini Projects\Database Technology\icons\placeholder.png")
        img = img.resize((300,200))
        self.placeholder =  ImageTk.PhotoImage(img) 
        self.imageCut = tk.Label(self.root, image=self.placeholder)
        self.imageCut.place(x=860, y=300, anchor='w')

        self.editImgButton = tk.Button(self.root, command=self.editImage, bg="#5B8676", fg="white", text='Edit', font='Lato 14 bold')
        self.editImgButton.place(x=980, y=411, width=70, height=40)

        self.root.mainloop()
    
    def editImage(self):
        self.file_name = filedialog.askopenfilename()
        if not self.file_name.lower().endswith(('.jpg', '.png')):
            messagebox.showerror("Error","File types must be of the jpg or png type")
        else:
            product_image = Image.open(self.file_name)
            self.product_image = product_image.resize((300,200))
            self.product_image = ImageTk.PhotoImage(self.product_image)

            self.imageCut = tk.Label(self.root, image=self.product_image)
            self.imageCut.place(x=860, y=300, anchor='w')

    def clear_entries(self):    
        for entry in self.entries:
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.Text):
                entry.delete("1.0", tk.END)
                entry.insert('1.0', "Enter your text here...")
            self.imageCut = tk.Label(self.root, image=self.placeholder)
            self.imageCut.place(x=860, y=300, anchor='w')
        
    def okClicked(self):
        try:
            productName = self.entries[0].get()
            price = float(self.entries[1].get())
            productDescription = self.entries[2].get("1.0", "end-1c")
            stock = self.entries[3].get()

            category = self.entries[4].get()
            cursor.execute("SELECT `categoryID` FROM `onlinestore`.`category` WHERE `categoryName` = %s;", (category,))
            categoryID_product = cursor.fetchone()

            if categoryID_product is None:
                cursor.execute("INSERT INTO `onlinestore`.`category` (`categoryName`) VALUES (%s);", (category,))
                cursor.execute("SELECT `categoryID` FROM `onlinestore`.`category` WHERE `categoryName` = %s;", (category,))
                categoryID_product = cursor.fetchone()

            for category in categoryID_product:
                categoryID = category

            sellerID = 1

            add_product(productName, price, self.file_name, productDescription, stock, categoryID, sellerID)
            messagebox.showinfo("Updated!", "Product added successfully!")
            self.clear_entries()
        except:
            messagebox.showerror("Error", "Please make sure you filled all fields, and validate each input")


    def goBack(self):
        print("Going back...")

    def goToSetting(self):
        print("Going to settings...")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

AddProductPage()
display_table("product")