import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Functions to handle button actions
def backButtonAction():
    messagebox.showinfo("Back Button", "Back")

def addCartAction():
    messagebox.showinfo("Add to Cart", "Add to cart")

# Set up root
root = tk.Tk()
root.title("Product Page")

# Setting up background colour and size
root.configure(bg="#C4DAD2")
root.geometry('1280x720')

# Create container for content
content = tk.Frame(root, bg="#C4DAD2")
content.pack(padx=20, pady=20)

# Create container for Shop Title
header = tk.Frame(content, bg="#C4DAD2")
header.pack(padx=20, pady=20)

# Create text for Shop Title
shopTitleText = tk.Label(header, text="ONLINE STORE", font=("Lato", 20, "bold"), bg="#C4DAD2")
shopTitleText.pack(side="left", padx=10)

icons_frame = tk.Frame(header, bg="#C4DAD2")
icons_frame.pack(side="right")

cart_icon = tk.Label(icons_frame, text="🛒", font=("Lato", 20), bg="#C4DAD2")
cart_icon.pack(side="left", padx=10)

settings_icon = tk.Label(icons_frame, text="⚙️", font=("Lato", 20), bg="#C4DAD2")
settings_icon.pack(side="left", padx=10)

# Create container for Product Details
productDetailCont = tk.Frame(content, bg="#C4DAD2")
productDetailCont.pack(padx=20, pady=20)

# Create image for Product Details
image_url = "https://storage.googleapis.com/a1aa/image/6Lhf7bkG5H0zKS6vqJs4XwBZeond46sVTDTHn1JQPgpCHQqTA.jpg"
response = requests.get(image_url)
img_data = Image.open(BytesIO(response.content)).resize((459, 342))
product_image = ImageTk.PhotoImage(img_data)

image_label = tk.Label(productDetailCont, image=product_image, bg="#C4DAD2")
image_label.pack(side='left')

# Create text for the Product Details
productNameText = tk.Label(productDetailCont, text="Product Name", font=("Lato", 16, "bold"), bg="#C4DAD2")
productNameText.pack(anchor="w")

productPriceText = tk.Label(productDetailCont, text="Product Price", font=("Lato", 14), bg="#C4DAD2")
productPriceText.pack(anchor="w")

productDetailsText = tk.Label(productDetailCont, text="Product Description:\naaaaaaaaaaaa", font=("Lato", 14), bg="#C4DAD2")
productDetailsText.pack(anchor="w")

# Create container for Seller Details
sellerDetailCont = tk.Frame(productDetailCont, bg="#C4DAD2", borderwidth=1, relief='solid')
sellerDetailCont.pack(side="bottom", pady=10, fill='x')

# Create text for the Seller Details
sellerNameText = tk.Label(sellerDetailCont, text="Seller Name", font=("Lato", 16, "bold"), bg="#C4DAD2")
sellerNameText.pack(anchor="nw")

sellerAddressText = tk.Label(sellerDetailCont, text="Seller Address", font=("Lato", 14), bg="#C4DAD2")
sellerAddressText.pack(anchor="nw")

sellerPaymentText = tk.Label(sellerDetailCont, text="Seller Accepted Payment", font=("Lato", 14), bg="#C4DAD2")
sellerPaymentText.pack(anchor="nw")

# Create container for Buttons
buttonsFrame = tk.Frame(content, bg="#c8d6d4")
buttonsFrame.pack(side="bottom")

# Create Buttons
back_button = tk.Button(buttonsFrame, text="Back", command=backButtonAction, bg="#6b8f8e", fg="white")
back_button.pack(side="left", padx=10)

# Add to Cart Button
add_to_cart_button = tk.Button(buttonsFrame, text="Add to Cart", command=addCartAction, bg="#6b8f8e", fg="white")
add_to_cart_button.pack(side="left", padx=10)

root.mainloop()