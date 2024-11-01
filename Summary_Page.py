import tkinter as tk

class SummaryPage():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Summary Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        summaryText = tk.Label(self.root, text="SUMMARY", font='Lato 30 bold', bg='#C4DAD2')
        summaryText.place(x=530, y=33)

        image4 = tk.PhotoImage(file='icons/settingIcon.png')
        self.settingButton = tk.Button(self.root, image=image4, command=self.goToSetting, bg="#C4DAD2", fg="white")
        self.settingButton.place(x=1193, y=29, width=48, height=48)

        self.backButton = tk.Button(self.root, command=self.goToHome, bg="#5B8676", fg="white", text='Back', font='Lato 20 bold')
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

        self.products = [
            {'name': 'Table', 'price': 'Rp 50.000'},
            {'name': 'Chair', 'price': 'Rp 52.000'},
            {'name': 'T-Shirt', 'price': 'Rp 43.000'},
            {'name': 'Paper', 'price': 'Rp 14.000'},
            {'name': 'Bracelet', 'price': 'Rp 100.000'},
            {'name': 'Necklace', 'price': 'Rp 112.000'},
            {'name': 'Wallet', 'price': 'Rp 45.000'},
            {'name': 'Mug', 'price': 'Rp 23.000'}
        ]

        for d in self.products:
            name = d['name']
            price = d['price']
            
            product_frame = tk.Frame(scrollableFrame, bg="white")
            product_frame.pack(fill="x", padx=10, pady=5)

            txtlabel = tk.Label(product_frame, text=name, font='Lato 14', bg='white', anchor="w")
            txtlabel.pack(side="left", padx=10)

            pricelabel = tk.Label(product_frame, text=price, font='Lato 14', bg='white', anchor="e")
            pricelabel.pack(side="right", padx=480)
        
        separatorline = tk.Label(scrollableFrame, text="--------------------------------------------------------------------------------------------------------------", font='Lato 16', bg='white')
        separatorline.pack(padx=10, pady=10, anchor="w")

        total_frame = tk.Frame(scrollableFrame, bg="white")
        total_frame.pack(fill="x", padx=10, pady=5)

        txtlabel = tk.Label(total_frame, text='Total', font='Lato 16 bold', bg='white', anchor="w")
        txtlabel.pack(side="left", padx=10)

        pricelabel = tk.Label(total_frame, text=price, font='Lato 16 bold', bg='white', anchor="e")
        pricelabel.pack(side="right", padx=480)


        self.root.mainloop()
    

    def delete_product(self, product_canvas):
        product_canvas.destroy()

    def goToSetting(self):
        print("Going to settings...")

    def goToHome(self):
        print("Going home...")

    def checkout(self):
        print("Checking out...")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

SummaryPage()
