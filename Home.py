import tkinter as tk
from sql_connection import getsqlconnection
from PIL import Image, ImageTk

class Homepage():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Home Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')
        self.connection = getsqlconnection()

        image1 = tk.PhotoImage(file="icons/Logo.png")
        self.image_label = tk.Label(self.root, image=image1, bg='#C4DAD2')
        self.image_label.place(x=43, y=22)

        self.searchbarField = tk.Entry(self.root, background='white', foreground='black', font=('Lato', 14), width=15)
        self.searchbarField.place(x=328, y=34, width=600, height=40)

        image2 = tk.PhotoImage(file='icons/searchIcon.png')
        self.searchButton = tk.Button(self.root, image=image2, command=self.search, bg="#C4DAD2", fg="white")
        self.searchButton.place(x=945, y=29, width=47, height=47)

        image3 = tk.PhotoImage(file='icons/cartIcon.png')
        self.cartButton = tk.Button(self.root, image=image3, command=self.goToCart, bg="#C4DAD2", fg="white")
        self.cartButton.place(x=1112, y=29, width=48, height=48)

        image4 = tk.PhotoImage(file='icons/settingIcon.png')
        self.settingButton = tk.Button(self.root, image=image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton.place(x=1193, y=29, width=48, height=48)


        self.filterframe = tk.Frame(self.root, bg='white')
        self.filterframe.place(x=18, y=148, width=316, height=537)

        self.canvas = tk.Canvas(self.filterframe, bg="white", highlightthickness=0)
        scrollableFrame = tk.Frame(self.canvas, bg="white")

        scrollbar = tk.Scrollbar(self.filterframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")

        scrollableFrame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        filtertext = tk.Label(scrollableFrame, text="Filter", font='Lato 20 bold', bg='white')
        filtertext.pack(padx=10, pady=10, anchor="w")

        categorytext = tk.Label(scrollableFrame, text="By Category:", font='Lato 16 bold', bg='white')
        categorytext.pack(padx=10,pady=10, anchor="w")

        
        cursor = self.connection.cursor()
        query = "SELECT category.categoryID, category.categoryName FROM product JOIN category ON product.categoryID=category.categoryID;"
        cursor.execute(query)
        self.categoryDict = []
        self.categoryList =[]

        for category in cursor:
            self.categoryDict.append({'categoryID':category[0], 'categoryName':category[1]})
            self.categoryList.append(category[1])

        self.categoryList = list(set(self.categoryList))
        self.categoryButtonClicked = []
        for category in self.categoryList:
            check = tk.IntVar()
            self.categoryButtonClicked.append(check)
            button = tk.Checkbutton(scrollableFrame, text=category, variable=check, 
                                    onvalue=1, offvalue=0, font='Lato 12', bg='white', 
                                    command=self.togglecheckbox)
            button.pack(anchor="w", padx=20)



        priceText = tk.Label(scrollableFrame, text="By Price:", font='Lato 16 bold', bg='white')
        priceText.pack(padx=10,pady=15, anchor="w")

        self.priceList = ['<Rp 20.000', 'Rp 20.000-100.000', 'Rp 100.000-500.000', 'Rp 500.000-1.000.000', '>Rp 1.000.000']
        self.priceButtonClicked = []
        for p in self.priceList:
            check = tk.IntVar()
            self.priceButtonClicked.append(check)
            button = tk.Checkbutton(scrollableFrame, text=p, variable=check, 
                                    onvalue=1, offvalue=0, font='Lato 12', bg='white', 
                                    command=self.togglecheckbox2)
            button.pack(anchor="w", padx=20)    



        self.productframe = tk.Frame(self.root, bg='#C4DAD2')
        self.productframe.place(x=370, y=148, width=872, height=537)

        self.canvas2 = tk.Canvas(self.productframe, bg="#C4DAD2", highlightthickness=0)
        self.scrollableFrame2 = tk.Frame(self.canvas2, bg="#C4DAD2")

        scrollbar2 = tk.Scrollbar(self.productframe, orient="vertical", command=self.canvas2.yview)
        self.canvas2.configure(yscrollcommand=scrollbar2.set)

        self.canvas2.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")

        self.canvas2.create_window((0, 0), window=self.scrollableFrame2, anchor="nw")
        self.scrollableFrame2.bind("<Configure>", self.on_frame_configure2)
        self.canvas2.bind_all("<MouseWheel>", self._on_mouse_wheel2)

        
        cursor = self.connection.cursor()
        query = "SELECT * FROM product;"
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

        self.product_images = []

        columns = 3
        for index, d in enumerate(self.products):
            row = index // columns
            col = index % columns
            
            name = d['product_name']
            price = d['product_price']
            price = "Rp {:,.0f}".format(price).replace(",", ".")
            image_path = 'images/'+ d['product_image']  

            product_canvas = tk.Canvas(self.scrollableFrame2, width=230, height=230, bg="white", highlightthickness=0)
            product_canvas.grid(row=row, column=col, padx=25, pady=20)

            img = Image.open(image_path)
            img = img.resize((150,100))
            photoImg =  ImageTk.PhotoImage(img)
            self.product_images.append(photoImg)  
            product_canvas.create_image(110, 70, image=photoImg)

            product_canvas.create_text(110, 150, text=name, font='Lato 16 bold', fill='black')
            product_canvas.create_text(110, 180, text=price, font='Lato 14', fill='grey')
            

        self.current_search_query = ""
        self.selected_category_ids = []
        self.selected_price_ranges = []
        self.root.mainloop()


    def search(self):
        self.current_search_query = self.searchbarField.get().strip().lower()
        self.updateProductDisplay()

    def togglecheckbox(self):
        selected_category_names = [
            self.categoryList[idx] for idx, val in enumerate(self.categoryButtonClicked) if val.get() == 1
        ]
        self.selected_category_ids = [
            category['categoryID'] for category in self.categoryDict if category['categoryName'] in selected_category_names
        ]
        self.updateProductDisplay()

    def togglecheckbox2(self):
        self.selected_price_ranges = [
            self.priceList[idx] for idx, val in enumerate(self.priceButtonClicked) if val.get() == 1
        ]
        self.updateProductDisplay()

    def updateProductDisplay(self):
        filtered_products = self.products

        if self.current_search_query:
            filtered_products = [
                product for product in filtered_products
                if self.current_search_query in product['product_name'].lower()
            ]

        if self.selected_category_ids:
            filtered_products = [
                product for product in filtered_products
                if product['category_id'] in self.selected_category_ids
            ]

        if self.selected_price_ranges:
            price_ranges = {
                '<Rp 20.000': (0, 20000),
                'Rp 20.000-100.000': (20000, 100000),
                'Rp 100.000-500.000': (100000, 500000),
                'Rp 500.000-1.000.000': (500000, 1000000),
                '>Rp 1.000.000': (1000000, float('inf'))
            }
            temp_filtered = []
            for price_range in self.selected_price_ranges:
                min_price, max_price = price_ranges[price_range]
                temp_filtered.extend(
                    product for product in filtered_products
                    if min_price <= product['product_price'] <= max_price
                )
            filtered_products = temp_filtered

        self.displayProducts = filtered_products

        for widget in self.scrollableFrame2.winfo_children():
            widget.destroy()

        columns = 3
        for index, product in enumerate(self.displayProducts):
            row = index // columns
            col = index % columns

            name = product['product_name']
            price = product['product_price']
            price = "Rp {:,.0f}".format(price).replace(",", ".")
            image_path = 'images/' + product['product_image']

            product_canvas = tk.Canvas(self.scrollableFrame2, width=230, height=230, bg="white", highlightthickness=0)
            product_canvas.grid(row=row, column=col, padx=25, pady=20)

            img = Image.open(image_path)
            img = img.resize((150, 100))
            photoImg = ImageTk.PhotoImage(img)
            self.product_images.append(photoImg)  
            product_canvas.create_image(110, 70, image=photoImg)

            product_canvas.create_text(110, 150, text=name, font='Lato 16 bold', fill='black')
            product_canvas.create_text(110, 180, text=price, font='Lato 14', fill='grey')


    
    def on_frame_configure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_frame_configure2(self,event):
        self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))
    
    def _on_mouse_wheel2(self, event):
        self.canvas2.yview_scroll(int(-1*(event.delta/120)), "units")

    def goToCart(self):
        print("Going to cart...")

    def goToSetting(self):
        print("Going to settings...")

Homepage()
