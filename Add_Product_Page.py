import tkinter as tk
from PIL import Image, ImageTk

class AddProductPage():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Add Product Page")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        yourShopText = tk.Label(self.root, text="ADD PRODUCT", font='Lato 24 bold', bg='#C4DAD2')
        yourShopText.place(x=32, y=33)

        self.image4 = tk.PhotoImage(file='icons/settingIcon.png')
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

        img = Image.open("icons/placeholder.png")
        img = img.resize((300,200))
        photoImg =  ImageTk.PhotoImage(img)
        self.imageCut = tk.Label(self.root, image=photoImg)
        self.imageCut.place(x=860, y=300, anchor='w')

        self.editImgButton = tk.Button(self.root, command=self.editImage, bg="#5B8676", fg="white", text='Edit', font='Lato 14 bold')
        self.editImgButton.place(x=980, y=411, width=70, height=40)

        self.root.mainloop()

    def editImage(self):
        print('edit image...')
    def okClicked(self):
        print('ok...')

    def goBack(self):
        print("Going back...")

    def goToSetting(self):
        print("Going to settings...")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

AddProductPage()
