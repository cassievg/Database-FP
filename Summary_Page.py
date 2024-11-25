import tkinter as tk
from sql_connection import getsqlconnection
import datetime
from tkinter import messagebox
from User_Setting import UserSetting

class SummaryPage():
    def __init__(self, cartpage, products, user_id, homeroot):
        self.root = tk.Tk()
        self.root.title("Summary Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        self.connection = getsqlconnection()
        self.cartpage_root = cartpage
        self.products =products
        self.user_id = user_id
        self.home_root = homeroot

        summaryText = tk.Label(self.root, text="SUMMARY", font='Lato 30 bold', bg='#C4DAD2')
        summaryText.place(x=530, y=33)

        image4 = tk.PhotoImage(file='icons/settingIcon.png')
        self.settingButton = tk.Button(self.root, image=image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton.place(x=1193, y=29, width=48, height=48)

        self.backButton = tk.Button(self.root, command=self.goToCart, bg="#5B8676", fg="white", text='Back', font='Lato 20 bold')
        self.backButton.place(x=40, y=629, width=136, height=60)

        self.checkoutButton = tk.Button(self.root, command=self.checkout, bg="#5B8676", fg="white", text='Checkout', font='Lato 20 bold')
        self.checkoutButton.place(x=1041, y=621, width=200, height=60)


        self.productframe = tk.Frame(self.root, bg='#C4DAD2')
        self.productframe.place(x=246, y=110, width=775, height=405)

        self.canvas = tk.Canvas(self.productframe, bg="white", highlightthickness=0)
        scrollableFrame = tk.Frame(self.canvas, bg="white")

        scrollbar = tk.Scrollbar(self.productframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        scrollableFrame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        productSubtotalText = tk.Label(scrollableFrame, text="Product Subtotal", font='Lato 16 bold', bg='white')
        productSubtotalText.pack(padx=10, pady=10, anchor="w")

        total=0
        for d in self.products:
            name = d['product_name']
            price = d['quantity'] * d['product_price']
            total +=price
            price = "Rp {:,.0f}".format(price).replace(",", ".")
            
            product_frame = tk.Frame(scrollableFrame, bg="white")
            product_frame.pack(fill="x", padx=10, pady=5)

            txtlabel = tk.Label(product_frame, text=name, font='Lato 14', bg='white', anchor="w", wraplength=450, justify='left')
            txtlabel.pack(side="left", padx=10)

            pricelabel = tk.Label(product_frame, text=price, font='Lato 14', bg='white', anchor="e")
            pricelabel.pack(side="right", padx=480)
        
        separatorline = tk.Label(scrollableFrame, text="--------------------------------------------------------------------------------------------------------------", font='Lato 16', bg='white')
        separatorline.pack(padx=10, pady=10, anchor="w")

        total_frame = tk.Frame(scrollableFrame, bg="white")
        total_frame.pack(fill="x", padx=10, pady=5)

        txtlabel = tk.Label(total_frame, text='Total', font='Lato 16 bold', bg='white', anchor="w")
        txtlabel.pack(side="left", padx=10)

        total = "Rp {:,.0f}".format(total).replace(",", ".")
        pricelabel = tk.Label(total_frame, text=total, font='Lato 16 bold', bg='white', anchor="e")
        pricelabel.pack(side="right", padx=480)


        self.root.mainloop()
    

    def goToSetting(self):
        self.root.destroy()
        UserSetting(self.user_id, self.home_root)

    def goToCart(self):
        self.root.destroy()
        self.cartpage_root.__class__(self.user_id, self.home_root)



    def checkout(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT GROUP_CONCAT(paymentType) FROM payment WHERE userID = {self.user_id};")
        customer_payment_types = cursor.fetchone()[0]

        if not customer_payment_types:
            messagebox.showerror("Payment Error", "No payment methods found for the customer.")
            cursor.close()
            return

        customer_payment_types = set(customer_payment_types.split(','))

        # Step 2: Retrieve Seller Payment Types
        seller_payment_types = set()
        non_matching_sellers = []  # List to store sellers with no common payment methods
        for d in self.products:
            seller_id = d['seller_id']
            cursor.execute(f"SELECT GROUP_CONCAT(paymentType) FROM payment WHERE userID = {seller_id};")
            seller_payment_types_for_product = cursor.fetchone()[0]
            
            if seller_payment_types_for_product:
                seller_payment_types |= set(seller_payment_types_for_product.split(','))
            else:
                messagebox.showerror("Payment Error", f"No payment methods found for the seller of {d['product_name']}.")
                cursor.close()
                return

            # Check if the seller has no common payment methods with the customer
            if customer_payment_types.isdisjoint(seller_payment_types_for_product.split(',')):
                non_matching_sellers.append(d['product_name'])  # Add product name to the list

        if not seller_payment_types:
            messagebox.showerror("Payment Error", "No payment methods found for the seller.")
            cursor.close()
            return

        # Step 3: Check if any seller has no common payment methods
        if non_matching_sellers:
            non_matching_sellers_list = ', '.join(non_matching_sellers)
            messagebox.showerror("Payment Error", f"The customer and the following sellers do not share any common payment methods: {non_matching_sellers_list}.")
            cursor.close()
            return


        cursor = self.connection.cursor()
        datenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for d in self.products:
            product_id = d['product_id']
            quantity = d['quantity']
            
            cursor.execute(f"SELECT remainingStock FROM product WHERE productID = {product_id};")
            remaining_stock = cursor.fetchone()[0]
            
            if remaining_stock < quantity:
                messagebox.showerror("Stock Error", f"Insufficient stock for product {d['product_name']}. Available: {remaining_stock}, Required: {quantity}")
                cursor.close()
                return  

        cursor.execute(f"INSERT INTO orders (orderDate, customerID) VALUES ('{datenow}', {self.user_id});")
        self.connection.commit()

        cursor.execute(f"SELECT orderID FROM orders WHERE customerID = {self.user_id} ORDER BY orderID DESC LIMIT 1;")
        order_id = cursor.fetchone()[0]

        values = []
        for d in self.products:
            product_id = d['product_id']
            quantity = d['quantity']
            priceAtOrder = d['product_price']
            values.append(f"({order_id}, {product_id}, {quantity}, {priceAtOrder})")

        query = "INSERT INTO order_items (orderID, productID, quantity, priceAtAddition) VALUES " + ", ".join(values)
        cursor.execute(query)
        self.connection.commit()

        for d in self.products:
            product_id = d['product_id']
            quantity = d['quantity']
            update_stock_query = f"UPDATE product SET remainingStock = remainingStock - {quantity} WHERE productID = {product_id};"
            cursor.execute(update_stock_query)
        
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE ci FROM cart_items ci JOIN cart c ON ci.cartID = c.cartID WHERE c.userID = {self.user_id};")
        self.connection.commit()
        cursor.close()
        messagebox.showinfo("Order Successful", "Your order has been placed successfully!")
        
        self.root.destroy()
        self.home_root.__class__(self.user_id)



    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


