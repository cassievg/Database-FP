import tkinter as tk
from tkinter import simpledialog

class RoleDialog(simpledialog.Dialog):
    def body(self, master):
        self.role_var = tk.StringVar(value="customer")
        
        tk.Label(master, text="Select your role:").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Radiobutton(master, text="Customer", variable=self.role_var, value="customer").grid(row=1, column=0, sticky="w")
        tk.Radiobutton(master, text="Seller", variable=self.role_var, value="seller").grid(row=2, column=0, sticky="w")
    
    def apply(self):
        self.result = self.role_var.get()