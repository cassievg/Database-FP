import tkinter as tk

class SignupPage2():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sign Up Page - Payment Type")
        self.root.configure(bg="#C4DAD2")
        self.root.geometry('1280x720')

        storeLogoFrame = tk.Frame(self.root, bg="#C4DAD2", borderwidth=1, relief='solid')
        storeLogoFrame.pack(side="left", pady=10, padx=70, fill='x')

        storeLogoText = tk.Label(storeLogoFrame, text="ONLINE\nSTORE", font=("Lato", 32, "bold"), bg="#C4DAD2")
        storeLogoText.pack(anchor="w")

        yourShopText = tk.Label(self.root, text="PAYMENT TYPE", font='Lato 32 bold', bg='#C4DAD2')
        yourShopText.place(x=573, y=33)

        contentFrame = tk.Frame(self.root, bg='#C4DAD2')
        contentFrame.place(x=512, y=152, width=690, height=430)

        self.labelName = ['BCA', 'OVO', 'GOPAY', 'BNI', 'BRI']
        self.entries=[]

        for e in self.labelName:
            label_frame = tk.Frame(contentFrame, bg='#C4DAD2')
            label_frame.pack(pady=(15, 15), padx=10, anchor='w')  # Padding around the entire frame

            label = tk.Label(label_frame, text=e, font='Lato 20 bold', bg='#C4DAD2')
            label.pack(side='left', padx=(0, 10))  # Padding to the right of the label

            entry = tk.Entry(label_frame, background='white', foreground='black', font=('Lato', 20), width=25)
            entry.pack(side='left', padx=(10, 0))  # Padding to the left of the entry
            self.entries.append(entry)

        self.backButton = tk.Button(self.root, command=self.goBack, bg="#5B8676", fg="white", text='Back', font='Lato 16 bold')
        self.backButton.place(x=520, y=549, width=100, height=50)

        self.okButton = tk.Button(self.root, command=self.okClicked, bg="#5B8676", fg="white", text='Sign Up', font='Lato 16 bold')
        self.okButton.place(x=890, y=549, width=120, height=50)




        self.root.mainloop()
    
    def okClicked(self):
        print('ok...')

    def goBack(self):
        print("Going back...")












SignupPage2()