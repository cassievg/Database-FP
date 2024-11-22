import tkinter as tk
from sql_connection import getsqlconnection
from PIL import Image, ImageTk
from tkinter import messagebox
from Edit_Product_Page import EditProductPage
from Add_Product_Page import AddProductPage
from User_Setting import UserSetting

class SellerHomePage():
    def __init__(self, sellerID):
        self.root = tk.Tk()
        self.root.title("Seller Home Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        self.connection = getsqlconnection()
        self.sellerID = sellerID

        yourShopText = tk.Label(self.root, text="YOUR SHOP", font='Lato 24 bold', bg='#C4DAD2')
        yourShopText.place(x=32, y=33)

        image4 = tk.PhotoImage(file='icons/settingIcon.png')
        self.settingButton = tk.Button(self.root, image=image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton.place(x=1193, y=29, width=48, height=48)

        self.addButton = tk.Button(self.root, command=self.addProduct, bg="#5B8676", fg="white", text='Add Product', font='Lato 16 bold')
        self.addButton.place(x=561, y=641, width=180, height=50)

        self.shopFrame = tk.Frame(self.root, bg='#C4DAD2')
        self.shopFrame.place(x=52, y=101, width=1190, height=121)

        self.canvas1 = tk.Canvas(self.shopFrame, bg="#C4DAD2", highlightthickness=1, highlightbackground='black')
        self.canvas1.pack(side="left", fill="both", expand=True)

        cursor = self.connection.cursor()
        cursor.execute(f'SELECT fName, lName, address FROM user WHERE userID={self.sellerID}')
        seller_details = cursor.fetchone()

        sellerName = tk.Label(self.shopFrame, text=seller_details[0]+' '+seller_details[1], font='Lato 20 bold', bg='#C4DAD2')
        sellerName.place(x=508, y=20)

        sellerAddress = tk.Label(self.shopFrame, text=seller_details[2], font='Lato 16', bg='#C4DAD2')
        sellerAddress.place(x=518, y=70)


        self.searchbarField = tk.Entry(self.root, background='white', foreground='black', font=('Lato', 14), width=15)
        self.searchbarField.place(x=310, y=240, width=600, height=40)

        image2 = tk.PhotoImage(file='icons/searchIcon.png')
        self.searchButton = tk.Button(self.root, image=image2, command=self.search, bg="#C4DAD2", fg="white")
        self.searchButton.place(x=925, y=240, width=40, height=40)


        self.productframe = tk.Frame(self.root, bg='#C4DAD2')
        self.productframe.place(x=52, y=310, width=1190, height=300)

        self.canvas = tk.Canvas(self.productframe, bg="#C4DAD2", highlightthickness=0)
        self.scrollableFrame = tk.Frame(self.canvas, bg="#C4DAD2")

        scrollbar = tk.Scrollbar(self.productframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw")
        self.scrollableFrame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        cursor = self.connection.cursor()
        query = f"SELECT * FROM product WHERE sellerID={self.sellerID};"
        cursor.execute(query)
        self.products = []

        for (product_id, product_name, product_price, product_image, product_description, remaining_stock, category_id, seller_id) in cursor:
            self.products.append({
                'product_id':product_id,
                'product_name' : product_name,
                'product_price':product_price,
                'product_image':product_image,
                'product_description' : product_description,
                'remaining_stock' : remaining_stock,
                'category_id' :category_id,
                'seller_id' : seller_id
            })
        cursor.close()

        self.product_images = []

        for d in self.products:
            name = d['product_name']
            price = d['product_price']
            price = "Rp {:,.0f}".format(price).replace(",", ".")
            image_path = 'images/' + d['product_image']
            stock = 'Remaining stock: ' + str(d['remaining_stock'])

            product_canvas = tk.Canvas(self.scrollableFrame, width=1130, height=150, bg="white", highlightthickness=0)
            product_canvas.grid(padx=25, pady=20)

            img = Image.open(image_path)
            img = img.resize((150,100))
            photoImg =  ImageTk.PhotoImage(img)
            self.product_images.append(photoImg)  
            product_canvas.create_image(110, 70, image=photoImg)

            product_canvas.create_text(230, 35, text=name, font='Lato 16 bold', fill='black', anchor='w')
            product_canvas.create_text(230, 70, text=price, font='Lato 14', fill='grey', anchor='w')
            product_canvas.create_text(230, 105, text=stock, font='Lato 14', fill='grey', anchor='w')

            delete_button = tk.Button(self.scrollableFrame, text="X", command=lambda pc=product_canvas, pid=d['product_id']: self.delete_product(pc,pid), width=3, bg='lightcoral', font='Lato 14 bold')
            product_canvas.create_window(1100, 25, window=delete_button)

            edit_button = tk.Button(self.scrollableFrame, text="Edit", command=lambda pc=d: self.edit_product(pc), width=3, bg='lightgray', font='Lato 14 bold')
            product_canvas.create_window(1070, 110, window=edit_button, width=100)

        self.root.mainloop()
    

    def edit_product(self, dict):
        self.root.destroy()
        EditProductPage(self.sellerID, self, dict)


    def delete_product(self, product_canvas, product_id):
        answer = messagebox.askyesno(title='confirmation', message='Are you sure that you want to delete?')
        if answer:
            product_canvas.destroy()
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM `onlinestore`.`product` WHERE `productID` = {product_id}")
            self.connection.commit()

    def goToSetting(self):
        self.root.destroy()
        UserSetting(self.sellerID, self)

    def addProduct(self):
        self.root.destroy()
        AddProductPage(self.sellerID, self)

    def search(self):
        self.current_search_query = self.searchbarField.get().strip().lower()
        self.updateProductDisplay()

    def updateProductDisplay(self):
        filtered_products = self.products

        if self.current_search_query:
            filtered_products = [
                product for product in filtered_products
                if self.current_search_query in product['product_name'].lower()
            ]

        self.displayProducts = filtered_products

        for widget in self.scrollableFrame.winfo_children():
            widget.destroy()

        available_products = [product for product in self.displayProducts if product['remaining_stock'] > 0]
        for d in available_products:
            name = d['product_name']
            price = d['product_price']
            price = "Rp {:,.0f}".format(price).replace(",", ".")
            image_path = 'images/' + d['product_image']

            product_canvas = tk.Canvas(self.scrollableFrame, width=1130, height=150, bg="white", highlightthickness=0)
            product_canvas.grid(padx=25, pady=20)

            img = Image.open(image_path)
            img = img.resize((150,100))
            photoImg =  ImageTk.PhotoImage(img)
            self.product_images.append(photoImg)  
            product_canvas.create_image(110, 70, image=photoImg)

            product_canvas.create_text(230, 35, text=name, font='Lato 16 bold', fill='black', anchor='w')
            product_canvas.create_text(230, 70, text=price, font='Lato 14', fill='grey', anchor='w')

            delete_button = tk.Button(self.scrollableFrame, text="X", command=lambda pc=product_canvas, pid=d['product_id']: self.delete_product(pc,pid), width=3, bg='lightcoral', font='Lato 14 bold')
            product_canvas.create_window(1100, 25, window=delete_button)

            edit_button = tk.Button(self.scrollableFrame, text="Edit", command=lambda pc=d: self.edit_product(pc), width=3, bg='lightgray', font='Lato 14 bold')
            product_canvas.create_window(1070, 110, window=edit_button, width=100)



    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

# SellerHomePage(1)
