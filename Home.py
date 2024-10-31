import tkinter as tk

class Homepage():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Home Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

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

        self.categoryList = ['Fashion', 'Healthcare', 'School', 'Technology', 'Education']
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

        self.priceList = ['Rp 50.000-100.000', 'Rp 50.000-100.000', 'Rp 50.000-100.000', 'Rp 50.000-100.000', 'Rp 50.000-100.000']
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
        scrollableFrame2 = tk.Frame(self.canvas2, bg="#C4DAD2")

        scrollbar2 = tk.Scrollbar(self.productframe, orient="vertical", command=self.canvas2.yview)
        self.canvas2.configure(yscrollcommand=scrollbar2.set)

        self.canvas2.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")

        self.canvas2.create_window((0, 0), window=scrollableFrame2, anchor="nw")

        scrollableFrame2.bind("<Configure>", self.on_frame_configure2)

        self.canvas2.bind_all("<MouseWheel>", self._on_mouse_wheel2)

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

        columns = 3
        for index, d in enumerate(self.products):
            row = index // columns
            col = index % columns
            
            name = d['name']
            price = d['price']
            image_path = 'icons/'+ d['image']  

            product_canvas = tk.Canvas(scrollableFrame2, width=230, height=230, bg="white", highlightthickness=0)
            product_canvas.grid(row=row, column=col, padx=25, pady=20)

            product_image = tk.PhotoImage(file=image_path)  
            self.product_images.append(product_image)  
            product_canvas.create_image(110, 70, image=product_image)

            product_canvas.create_text(110, 150, text=name, font='Lato 16 bold', fill='black')
            product_canvas.create_text(110, 180, text=price, font='Lato 14', fill='grey')
            
    



        self.root.mainloop()




    def search(self):
        print("Searching...")

    def goToCart(self):
        print("Going to cart...")

    def goToSetting(self):
        print("Going to settings...")

    def togglecheckbox(self):
        for idx, val in enumerate(self.categoryButtonClicked):
            print(f"{self.categoryList[idx]} selected: {bool(val.get())}")
    
    def togglecheckbox2(self):
        for idx, val in enumerate(self.priceButtonClicked):
            print(f"{self.priceList[idx]} selected: {bool(val.get())}")
    
    def on_frame_configure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_frame_configure2(self,event):
        self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))
    
    def _on_mouse_wheel2(self, event):
        self.canvas2.yview_scroll(int(-1*(event.delta/120)), "units")



Homepage()
