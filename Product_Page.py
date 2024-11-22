import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from sql_connection import getsqlconnection
from Cart_Page import CartPage
from User_Setting import UserSetting

class ProductPage():
    def __init__(self, product_dict, user_id, homeroot):
        self.root = tk.Tk()
        self.root.title("Product Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')
        self.connection = getsqlconnection()

        self.home_root = homeroot
        self.user_id = user_id
        self.product_dict = product_dict

        cursor = self.connection.cursor()
        cursor.execute(f"SELECT categoryName FROM category WHERE categoryID = {self.product_dict['category_id']}")
        category_name = cursor.fetchone()[0]
        cursor.close()

        content = tk.Frame(self.root, bg="#C4DAD2")
        content.pack(padx=20, pady=20)
        header = tk.Frame(content, bg="#C4DAD2")
        header.pack(padx=20, pady=20)

        image1 = tk.PhotoImage(file="icons/Logo.png")
        self.image_label = tk.Label(self.root, image=image1, bg='#C4DAD2')
        self.image_label.place(x=43, y=22)

        image3 = tk.PhotoImage(file='icons/cartIcon.png')
        self.cartButton = tk.Button(self.root, image=image3, command=self.goToCart, bg="#C4DAD2", fg="white")
        self.cartButton.place(x=1112, y=29, width=48, height=48)

        image4 = tk.PhotoImage(file='icons/settingIcon.png')
        self.settingButton = tk.Button(self.root, image=image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton.place(x=1193, y=29, width=48, height=48)

        img_path = 'images/'+ self.product_dict['product_image']
        img = Image.open(img_path)
        img = img.resize((450,300))
        photoImg =  ImageTk.PhotoImage(img)
        self.imageCut = tk.Label(self.root, image=photoImg)
        self.imageCut.place(x=52, y=300, anchor='w')

        self.productframe = tk.Frame(self.root, bg='#C4DAD2')
        self.productframe.place(x=562, y=101, width=650, height=490)

        self.canvas = tk.Canvas(self.productframe, bg="#C4DAD2", highlightthickness=0)
        scrollableFrame = tk.Frame(self.canvas, bg="#C4DAD2")

        scrollbar = tk.Scrollbar(self.productframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        scrollableFrame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        label1 = tk.Label(scrollableFrame, text=self.product_dict['product_name'], font='Lato 28 bold', bg='#C4DAD2',wraplength=620,anchor='w', justify='left')
        label1.pack(pady=(5, 15), anchor='w')

        price = self.product_dict['product_price']
        price = "Rp {:,.0f}".format(price).replace(",", ".")
        label2 = tk.Label(scrollableFrame, text=price, font='Lato 20', bg='#C4DAD2',wraplength=620,anchor='w', justify='left')
        label2.pack(pady=(5, 25), anchor='w')
            
        label3 = tk.Label(scrollableFrame, text='Product Description:', font='Lato 18 bold', bg='#C4DAD2',wraplength=620,anchor='w', justify='left')
        label3.pack(pady=(5, 5), anchor='w')
        label3_2 = tk.Label(scrollableFrame, text=self.product_dict['product_description'], font='Lato 16', bg='#C4DAD2',wraplength=620,anchor='w', justify='left')
        label3_2.pack(pady=(5,25), anchor='w')

        label4 = tk.Label(scrollableFrame, text='Category:', font='Lato 18 bold', bg='#C4DAD2',wraplength=620,anchor='w', justify='left')
        label4.pack(pady=(5, 5), anchor='w')
        label4_2 = tk.Label(scrollableFrame, text=category_name, font='Lato 16', bg='#C4DAD2',wraplength=620,anchor='w', justify='left')
        label4_2.pack(pady=(5,25), anchor='w')

        labelseller = tk.Label(scrollableFrame, text='Seller:', font='Lato 18 bold', bg='#C4DAD2',wraplength=620,anchor='w', justify='left')
        labelseller.pack(pady=(5, 0), anchor='w')

        sellerDetailCont = tk.Frame(scrollableFrame, bg="#C4DAD2", borderwidth=1, relief='solid')
        sellerDetailCont.pack(side="bottom", pady=10, fill='x')

        cursor = self.connection.cursor()
        query = f"SELECT user.fName, user.lName, user.address, payment.paymentType FROM user JOIN payment ON user.userID = payment.userID WHERE user.userID = {self.product_dict['seller_id']};"
        cursor.execute(query)
        self.sellerDetails = {'seller_name':'', 'seller_address':'', 'seller_payment_type':[]}

        for (fname, lname, seller_address, seller_payment_type) in cursor:
            self.sellerDetails['seller_name'] = fname + ' ' + lname
            self.sellerDetails['seller_address'] = seller_address
            self.sellerDetails['seller_payment_type'].append(seller_payment_type)

        sellerNameText = tk.Label(sellerDetailCont, text=self.sellerDetails['seller_name'], font=("Lato", 18, "bold"), bg="#C4DAD2",wraplength=620,anchor='w', justify='left')
        sellerNameText.pack(anchor="nw")

        sellerAddressText = tk.Label(sellerDetailCont, text='Address: '+self.sellerDetails['seller_address'], font=("Lato", 14), bg="#C4DAD2", wraplength=620,anchor='w', justify='left')
        sellerAddressText.pack(anchor="nw")

        seller_payment = ', '.join(self.sellerDetails['seller_payment_type'])
        sellerPaymentText = tk.Label(sellerDetailCont, text='Accepted payment: '+seller_payment, font=("Lato", 14), bg="#C4DAD2")
        sellerPaymentText.pack(anchor="nw")


        self.backButton = tk.Button(self.root, command=self.goToHome, bg="#5B8676", fg="white", text='Back', font='Lato 20 bold')
        self.backButton.place(x=40, y=629, width=136, height=60)

        self.addToCartButton = tk.Button(self.root, command=self.addToCart, bg="#5B8676", fg="white", text='Add to Cart', font='Lato 20 bold')
        self.addToCartButton.place(x=1041, y=621, width=200, height=60)

        self.root.mainloop()

    def goToCart(self):
        self.root.destroy()
        CartPage(self.user_id, self.home_root)

    def goToSetting(self):
        self.root.destroy()
        UserSetting(self.user_id, self.home_root)

    def goToHome(self):
        self.root.destroy()  
        self.home_root.__class__() 
    
    def addToCart(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM cart WHERE userID = {self.user_id}")
        cart = cursor.fetchone()
        
        if not cart:
            cursor.execute(f"INSERT INTO cart (userID) VALUES ({self.user_id})")
            self.connection.commit()
            cart_id = cursor.lastrowid
        else:
            cart_id = cart[0]
        cursor.close()
        
        product_id = self.product_dict['product_id']
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT quantity FROM cart_items WHERE productID = {product_id} AND cartID={cart_id}")
        result = cursor.fetchone()
        quantity =1
        if result: quantity += result[0]
        cursor.close()

        if(self.product_dict['remaining_stock']<quantity):
            messagebox.showerror("Stock Error", f"Insufficient stock for this product. Available: {self.product_dict['remaining_stock']}, Required: {quantity}")
            return

        cursor = self.connection.cursor()
        cursor.execute(f"SELECT productPrice FROM product WHERE productID = {product_id}")
        product = cursor.fetchone()
        
        if product and quantity==1:
            price_at_addition = product[0]
            cursor.execute(f"INSERT INTO cart_items (cartID, productID, quantity, priceAtAddition) VALUES ({cart_id}, {product_id}, {quantity}, {price_at_addition})")
            self.connection.commit()
        elif product and quantity>1:
            price_at_addition =product[0]
            cursor.execute(f"UPDATE cart_items SET quantity={quantity}, priceAtAddition={price_at_addition} WHERE cartID={cart_id} AND productID={product_id}")
            self.connection.commit()

        cursor.close()


    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# ddddd = {'product_id': 1, 'product_name': 'Toothpaste', 'product_price': 12000.0, 'product_image': 'toothpaste.png', 'product_description': 'mint flavor toothpaste aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'remaining_stock': 12, 'category_id': 2, 'seller_id': 1}
# xxx = {1:'Fashion', 2:'Health'}
# ProductPage(ddddd,xxx)

