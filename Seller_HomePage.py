import tkinter as tk

class SellerHomePage():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Seller Home Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

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

        sellerName = tk.Label(self.shopFrame, text="Seller Name", font='Lato 20 bold', bg='#C4DAD2')
        sellerName.place(x=508, y=20)

        sellerAddress = tk.Label(self.shopFrame, text="Seller Address", font='Lato 16', bg='#C4DAD2')
        sellerAddress.place(x=518, y=70)


        self.searchbarField = tk.Entry(self.root, background='white', foreground='black', font=('Lato', 14), width=15)
        self.searchbarField.place(x=310, y=240, width=600, height=40)

        image2 = tk.PhotoImage(file='icons/searchIcon.png')
        self.searchButton = tk.Button(self.root, image=image2, command=self.search, bg="#C4DAD2", fg="white")
        self.searchButton.place(x=925, y=240, width=40, height=40)


        self.productframe = tk.Frame(self.root, bg='#C4DAD2')
        self.productframe.place(x=52, y=310, width=1190, height=300)

        self.canvas = tk.Canvas(self.productframe, bg="#C4DAD2", highlightthickness=0)
        scrollableFrame = tk.Frame(self.canvas, bg="#C4DAD2")

        scrollbar = tk.Scrollbar(self.productframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        scrollableFrame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.products = [
            {'name': 'Table', 'price': 'Rp 50.000', 'image': 'placeholder.png'},
            {'name': 'Chair', 'price': 'Rp 52.000', 'image': 'placeholder.png'},
            {'name': 'T-Shirt', 'price': 'Rp 43.000', 'image': 'placeholder.png'},
            {'name': 'Paper', 'price': 'Rp 14.000', 'image': 'placeholder.png'},
            {'name': 'Bracelet', 'price': 'Rp 100.000', 'image': 'placeholder.png'},
            {'name': 'Necklace', 'price': 'Rp 112.000', 'image': 'placeholder.png'},
            {'name': 'Wallet', 'price': 'Rp 45.000', 'image': 'placeholder.png'},
            {'name': 'Mug', 'price': 'Rp 23.000', 'image': 'placeholder.png'}
        ]

        self.product_images = []

        for d in self.products:
            name = d['name']
            price = d['price']
            image_path = 'icons/' + d['image']

            product_canvas = tk.Canvas(scrollableFrame, width=1130, height=150, bg="white", highlightthickness=0)
            product_canvas.grid(padx=25, pady=20)

            product_image = tk.PhotoImage(file=image_path)
            self.product_images.append(product_image)
            product_canvas.create_image(130, 70, image=product_image)

            product_canvas.create_text(230, 35, text=name, font='Lato 16 bold', fill='black', anchor='w')
            product_canvas.create_text(230, 70, text=price, font='Lato 14', fill='grey', anchor='w')

            delete_button = tk.Button(scrollableFrame, text="X", command=lambda pc=product_canvas: self.delete_product(pc), width=3, bg='lightcoral', font='Lato 14 bold')
            product_canvas.create_window(1100, 25, window=delete_button)

            edit_button = tk.Button(scrollableFrame, text="Edit", command=lambda pc=d: self.edit_product(pc), width=3, bg='lightgray', font='Lato 14 bold')
            product_canvas.create_window(1070, 110, window=edit_button, width=100)

        self.root.mainloop()
    

    def edit_product(self, dict):
        print(dict)

    def delete_product(self, product_canvas):
        product_canvas.destroy()

    def goToSetting(self):
        print("Going to settings...")

    def addProduct(self):
        print("Adding product...")

    def editProduct(self):
        print("Editing product...")

    def search(self):
        print('Searching...')

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

SellerHomePage()
