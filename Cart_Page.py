import tkinter as tk
from sql_connection import getsqlconnection
from PIL import Image, ImageTk
from Summary_Page import SummaryPage
from tkinter import messagebox
from User_Setting import UserSetting

class CartPage():
    def __init__(self, user_id, homeroot):
        self.root = tk.Tk()
        self.root.title("Cart Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        self.connection = getsqlconnection()
        self.user_id = user_id
        self.home_root = homeroot

        yourCartText = tk.Label(self.root, text="YOUR CART", font='Lato 30 bold', bg='#C4DAD2')
        yourCartText.place(x=32, y=33)

        image4 = tk.PhotoImage(file='icons/settingIcon.png')
        self.settingButton = tk.Button(self.root, image=image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton.place(x=1193, y=29, width=48, height=48)

        self.backButton = tk.Button(self.root, command=self.goToHome, bg="#5B8676", fg="white", text='Back', font='Lato 20 bold')
        self.backButton.place(x=40, y=629, width=136, height=60)

        self.checkoutButton = tk.Button(self.root, command=self.checkout, bg="#5B8676", fg="white", text='Checkout', font='Lato 20 bold')
        self.checkoutButton.place(x=1041, y=621, width=200, height=60)

        self.productframe = tk.Frame(self.root, bg='#C4DAD2')
        self.productframe.place(x=52, y=101, width=1190, height=490)

        self.canvas = tk.Canvas(self.productframe, bg="#C4DAD2", highlightthickness=0)
        scrollableFrame = tk.Frame(self.canvas, bg="#C4DAD2")

        scrollbar = tk.Scrollbar(self.productframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        scrollableFrame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        cart_cursor = self.connection.cursor()
        cart_query = f"""
            SELECT cart_items.productID, cart_items.quantity, cart_items.priceAtAddition 
            FROM cart_items 
            JOIN cart ON cart.cartID = cart_items.cartID 
            WHERE cart.userID = {self.user_id};
        """
        cart_cursor.execute(cart_query)

        self.cartDetails = [] 
        self.products = []

        product_ids = []
        for c in cart_cursor:
            self.cartDetails.append({
                'productID': c[0],
                'quantity': c[1],
                'priceAtAddition': c[2]
            })
            product_ids.append(c[0])

        cart_cursor.close()

        if product_ids:
            product_cursor = self.connection.cursor()
            product_query = f"""
                SELECT product.productID, product.productName, product.productPrice, product.productImage, 
                    product.productDescription, product.remainingStock, product.categoryID, product.sellerID, 
                    GROUP_CONCAT(payment.paymentType) AS payment_types
                FROM product 
                JOIN user ON product.sellerID = user.userID 
                LEFT JOIN payment ON user.userID = payment.userID 
                WHERE product.productID IN ({','.join(map(str, product_ids))})
                GROUP BY product.productID;
            """
            product_cursor.execute(product_query)

            product_map = {p[0]: {
                'product_id': p[0],
                'product_name': p[1],
                'product_price': p[2],  
                'product_image': p[3],
                'product_description': p[4],
                'remaining_stock': p[5],
                'category_id': p[6],
                'seller_id': p[7],
                'payment_types': p[8].split(',') if p[8] else [],  
                'quantity':0
            } for p in product_cursor}

            # Update products with prices from cartDetails
            for item in self.cartDetails:
                product = product_map.get(item['productID'])
                if product:
                    product['product_price'] = item['priceAtAddition'] 
                    product['quantity'] = item['quantity']
                    self.products.append(product)

            product_cursor.close()

            

        self.product_images = []

        for d in self.products:
            name = d['product_name']
            price = d['product_price']
            price = "Rp {:,.0f}".format(price).replace(",", ".")
            image_path = 'images/' + d['product_image']
            payment = ', '.join(map(str, d['payment_types']))
            quantity = tk.IntVar(value=d['quantity'])

            product_canvas = tk.Canvas(scrollableFrame, width=1130, height=150, bg="white", highlightthickness=0)
            product_canvas.grid(padx=25, pady=20)

            img = Image.open(image_path)
            img = img.resize((150,100))
            photoImg =  ImageTk.PhotoImage(img)
            self.product_images.append(photoImg)  
            product_canvas.create_image(330, 70, image=photoImg)

            product_canvas.create_text(440, 35, text=name, font='Lato 16 bold', fill='black', anchor='w')
            product_canvas.create_text(440, 70, text=price, font='Lato 14', fill='grey', anchor='w')
            product_canvas.create_text(440, 105, text=payment, font='Lato 14', fill='grey', anchor='w')

            quantity_label = tk.Label(scrollableFrame, textvariable=quantity, font='Lato 16',bg='white')
            product_canvas.create_window(110, 70, window=quantity_label, anchor='w')

            add_button = tk.Button(
                scrollableFrame, text="+", font='Lato 10 bold', bg='lightgray', width=3,
                command=lambda q=quantity, product_id=d['product_id'], current_quantity=quantity.get(): (
                    self.check_and_update_quantity(q, product_id, current_quantity + 1)
                )
            )

            minus_button = tk.Button(
                scrollableFrame, text="-", font='Lato 10 bold', bg='lightgray', width=3,
                command=lambda q=quantity, product_id=d['product_id'], current_quantity=quantity.get(): (
                    self.check_and_update_quantity(q, product_id, max(1, current_quantity - 1))
                )
            )

            product_canvas.create_window(170, 70, window=add_button)
            product_canvas.create_window(75, 70, window=minus_button)

            delete_button = tk.Button(scrollableFrame, text="X", command=lambda pc=product_canvas, pid=d['product_id']: self.delete_product(pc,pid), width=3, bg='lightcoral', font='Lato 14 bold')
            product_canvas.create_window(1100, 25, window=delete_button)

        self.root.mainloop()
    
    def check_and_update_quantity(self, quantity_var, product_id, new_quantity):
        # Check if stock is sufficient
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT remainingStock FROM product WHERE productID = {product_id};")
        remaining_stock = cursor.fetchone()[0]
        
        if remaining_stock < new_quantity:
            # Display error if stock is insufficient
            messagebox.showerror("Stock Error", f"Insufficient stock. Available: {remaining_stock}, Required: {new_quantity}")
            return  # Don't update the UI if stock is insufficient

        # If sufficient stock, update the quantity
        quantity_var.set(new_quantity)  # Update the UI quantity
        self.update_quantity(product_id, new_quantity)  # Update the database

    def update_quantity(self, product_id, new_quantity):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT cartID FROM cart WHERE userID = {self.user_id};")
        cart_id = cursor.fetchone()

        if cart_id:
            query = f"UPDATE cart_items SET quantity = {new_quantity} WHERE productID = {product_id} AND cartID = {cart_id[0]};"
            cursor.execute(query)
            self.connection.commit()
        
        for product in self.products:
            if product['product_id'] == product_id:
                product['quantity'] = new_quantity
                break
        cursor.close()


    def delete_product(self, product_canvas, product_id):
        answer = messagebox.askyesno(title='confirmation', message='Are you sure that you want to delete?')
        if answer:
            product_canvas.destroy()
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM cart_items WHERE productID = {product_id};")
            self.connection.commit()
        self.products = [product for product in self.products if product['product_id'] != product_id]



    def goToSetting(self):
        self.root.destroy()
        UserSetting(self.user_id, self.home_root)

    def goToHome(self):
        self.root.destroy()
        self.home_root.__class__(self.user_id)

    def checkout(self):
        self.root.destroy()
        SummaryPage(self, self.products, self.user_id, self.home_root)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


