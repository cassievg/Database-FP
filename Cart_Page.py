import tkinter as tk

class CartPage():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cart Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        yourCartText = tk.Label(self.root, text="YOUR CART", font='Lato 30 bold', bg='#C4DAD2')
        yourCartText.place(x=32,y=33)

        image4 = tk.PhotoImage(file='settingIcon.png')
        self.settingButton = tk.Button(self.root, image=image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton.place(x=1193, y=29, width=48, height=48)

        self.backButton = tk.Button(self.root, command=self.goToHome, bg="#5B8676", fg="white", text='Back', font='Lato 20 bold')
        self.backButton.place(x=40, y=629, width=136, height=60)

        self.checkoutButton = tk.Button(self.root, command=self.checkout, bg="#5B8676", fg="white", text='Checkout', font='Lato 20 bold')
        self.checkoutButton.place(x=1041, y=621, width=200, height=60)


        self.productframe = tk.Frame(self.root, bg='#C4DAD2')
        self.productframe.place(x=52, y=101, width=1190, height=490)

        self.canvas = tk.Canvas(self.productframe, bg="green", highlightthickness=0)
        scrollableFrame = tk.Frame(self.canvas, bg="green")

        scrollbar = tk.Scrollbar(self.productframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

        scrollableFrame.bind("<Configure>", self.on_frame_configure)

        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.products = [
            {'name': 'Table', 'price': 'Rp 50.000', 'image': 'placeholder.png', 'payment':'BCA'},
            {'name': 'Chair', 'price': 'Rp 52.000', 'image': 'placeholder.png','payment':'BCA'},
            {'name': 'T-Shirt', 'price': 'Rp 43.000', 'image': 'placeholder.png','payment':'BCA'},
            {'name': 'Paper', 'price': 'Rp 14.000', 'image': 'placeholder.png','payment':'BCA'},
            {'name': 'Bracelet', 'price': 'Rp 100.000', 'image': 'placeholder.png','payment':'BCA'},
            {'name': 'Necklace', 'price': 'Rp 112.000', 'image': 'placeholder.png','payment':'BCA'},
            {'name': 'Wallet', 'price': 'Rp 45.000', 'image': 'placeholder.png','payment':'BCA'},
            {'name': 'Mug', 'price': 'Rp 23.000', 'image': 'placeholder.png','payment':'BCA'}
        ]

        self.product_images = []

        for d in self.products:
            name = d['name']
            price = d['price']
            image_path = d['image']  
            payment = d['payment']

            product_canvas = tk.Canvas(scrollableFrame, width=1130, height=150, bg="white", highlightthickness=0)
            product_canvas.grid(padx=25, pady=20)

            product_image = tk.PhotoImage(file=image_path)  
            self.product_images.append(product_image)  
            product_canvas.create_image(330, 70, image=product_image)

            product_canvas.create_text(440, 35, text=name, font='Lato 16 bold', fill='black', anchor='w')
            product_canvas.create_text(440, 70, text=price, font='Lato 14', fill='grey', anchor='w')
            product_canvas.create_text(440, 105, text=payment, font='Lato 14', fill='grey', anchor='w')

        self.root.mainloop()


    def goToSetting(self):
        print("Going to settings...")

    def goToHome(self):
        print("going home...")

    def checkout(self):
        print("check out...")

    def on_frame_configure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

CartPage()