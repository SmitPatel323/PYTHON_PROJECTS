import tkinter as tk
from tkinter import messagebox, simpledialog
import database
import scanner
import billing
import analysis
from datetime import datetime
from PIL import Image, ImageTk

cart = {}
is_logged_in = False 

def exit_application():
    root.destroy()


def main_screen():
    welcome.destroy() 
    root.deiconify()  


welcome = tk.Tk()
welcome.title("Welcome")
welcome.geometry("400x300")
welcome.configure(bg="lightgreen")


img = Image.open("supermart_img.jpg")
bg_image = ImageTk.PhotoImage(img)


bg_label = tk.Label(welcome, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

wel = tk.Label(welcome, text="Welcome to Supermart Billing and Analysis", font=("Arial", 14, "bold"), bg="lightgreen")
wel.place(x=0, y=0)

def register_user_ui():
    register_window = tk.Toplevel(welcome)
    register_window.title("Register User")
    register_window.geometry("300x200")
    
    tk.Label(register_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack(pady=5)
    
    tk.Label(register_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack(pady=5)
    
    def register():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            database.register_user(username, password)
            messagebox.showinfo("Success", "User Registered Successfully!")
            register_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields")
    
    tk.Button(register_window, text="Register", command=register).pack(pady=10)

def login_user_ui():
    global is_logged_in  
    login_window = tk.Toplevel(welcome)
    login_window.title("Login")
    login_window.geometry("300x200")
    
    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)
    
    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    
    def login():
        global is_logged_in  
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            if database.authenticate_user(username, password):
                is_logged_in = True 
                messagebox.showinfo("Success", "Login Successful!")
                login_window.destroy()
                main_screen() 
            else:
                messagebox.showerror("Error", "Invalid Username or Password")
        else:
            messagebox.showerror("Error", "Please fill in all fields")
    
    tk.Button(login_window, text="Login", command=login).pack(pady=10)

button_frame = tk.Frame(welcome, bg="lightgreen")
button_frame.pack(side=tk.BOTTOM, pady=10)

tk.Button(button_frame, text="Register", command=register_user_ui, bg="blue", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Login", command=login_user_ui, bg="blue", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)


root = tk.Tk()
root.withdraw()  

root.title("Supermart Billing System")
root.geometry("1000x700")
root.configure(bg="#f0f0f0")  


def show_frame(frame):
    frame.tkraise()

navbar = tk.Frame(root, bg="#007bff", height=50)
navbar.pack(fill=tk.X, pady=10)

scan_bill_frame = tk.Frame(root, bg="white")
add_product_frame = tk.Frame(root, bg="white")
analysis_frame = tk.Frame(root, bg="white")
product_list_frame = tk.Frame(root, bg="white")

for frame in (scan_bill_frame, add_product_frame, analysis_frame, product_list_frame):
    frame.place(x=0, y=60, width=1000, height=640)


def create_nav_button(text, frame):
    return tk.Button(navbar, text=text, command=lambda: show_frame(frame), bg="white", fg="#007bff", font=("Arial", 12, "bold"), padx=10, pady=5)

tk.Button(navbar, text="Scan & Bill", command=lambda: show_frame(scan_bill_frame), bg="white", fg="#007bff", font=("Arial", 12, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=10, pady=5)
tk.Button(navbar, text="Add Product", command=lambda: show_frame(add_product_frame), bg="white", fg="#007bff", font=("Arial", 12, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=10, pady=5)
tk.Button(navbar, text="Sales Analysis", command=lambda: show_frame(analysis_frame), bg="white", fg="#007bff", font=("Arial", 12, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=10, pady=5)
tk.Button(navbar, text="Product List", command=lambda: show_frame(product_list_frame), bg="white", fg="#007bff", font=("Arial", 12, "bold"), padx=10, pady=5).pack(side=tk.LEFT, padx=10, pady=5)
tk.Button(navbar, text="Exit", command=exit_application, bg="red", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5).pack(side=tk.RIGHT, padx=10, pady=5)


def add_to_cart():
    global is_logged_in  
    if not is_logged_in:  
        messagebox.showerror("Error", "You must be logged in to add products to the cart.")
        return

    product = scanner.scan_barcode()
    if product:
        barcode = product[0]  
        name = product[1]  
        price = product[2]  
        stock = product[3] 

        if stock == 0:
            messagebox.showerror("Out of Stock", f"{name} is out of stock!")
            return

        if barcode in cart:
            cart[barcode]['quantity'] += 1
        else:
            cart[barcode] = {'name': name, 'price': price, 'quantity': 1}

        
        database.update_stock(barcode, 1)
        update_cart_display()
        add_to_cart()

def update_cart_display():
    cart_list.delete(0, tk.END)
    total_price = 0

    for barcode, details in cart.items():
        cart_list.insert(tk.END, f"{details['name']} - ${details['price']} x {details['quantity']}")
        total_price += details['price'] * details['quantity']

    total_label.config(text=f"Total: ${total_price:.2f}")  


def generate_bill():
    global is_logged_in  
    if not is_logged_in:  
        messagebox.showerror("Error", "You must be logged in to generate a bill.")
        return

    if not cart:
        messagebox.showerror("Error", "Cart is empty!")
        return
    
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_price = sum(details['price'] * details['quantity'] for details in cart.values())
    database.record_sale(date, list(cart.values()), total_price)
    
    billing.generate_bill(cart, total_price)
    messagebox.showinfo("Success", "Bill generated successfully!")
    cart.clear()
    update_cart_display()


def show_sales_analysis():
    global is_logged_in  
    if not is_logged_in:  
        messagebox.showerror("Error", "You must be logged in to view sales analysis.")
        return
    
    analysis.display_sales_chart()

def add_product_ui():
    global is_logged_in  
    if not is_logged_in:  
        messagebox.showerror("Error", "You must be logged in to add products.")
        return

    add_product_window = tk.Toplevel(root)
    add_product_window.title("Add Product")
    add_product_window.geometry("300x400")
    
    tk.Label(add_product_window, text="Barcode:").pack(pady=5)
    barcode_entry = tk.Entry(add_product_window)
    barcode_entry.pack(pady=5)
    
    tk.Label(add_product_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(add_product_window)
    name_entry.pack(pady=5)
    
    tk.Label(add_product_window, text="Price:").pack(pady=5)
    price_entry = tk.Entry(add_product_window)
    price_entry.pack(pady=5)
    
    tk.Label(add_product_window, text="Stock:").pack(pady=5)
    stock_entry = tk.Entry(add_product_window)
    stock_entry.pack(pady=5)
    
    
    def add_product():
        barcode = barcode_entry.get()
        name = name_entry.get()
        price = price_entry.get()
        stock = stock_entry.get()
    
        if not barcode or not name or not price or not stock:
            messagebox.showerror("Error", "Please fill in all fields")
            return
    
        try:
            price = float(price)
            stock = int(stock)
            if price < 0 or stock < 0:
                messagebox.showerror("Error", "Price and stock must be non-negative")
                return
            if len(barcode)!=13:
                messagebox.showerror("Error", "Barcode must be exactly 13 characters long")
                return
            database.insert_product(barcode, name, price, stock)
            messagebox.showinfo("Success", "Product added successfully!")
            add_product_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and stock must be an integer")
    
    tk.Button(add_product_window, text="Add Product", command=add_product).pack(pady=10)

def display_products():
    for widget in product_list_frame.winfo_children():
        widget.destroy()
    
    products = database.get_all_products()
    tk.Label(product_list_frame, text="Product List", font=("Arial", 16, "bold")).pack(pady=10)
    for product in products:
        tk.Label(product_list_frame, text=f"Barcode: {product[0]}, Name: {product[1]}, Price: ${product[2]}, Stock: {product[3]}", font=("Arial", 12)).pack(pady=5)

def show_product_sales_analysis():
    barcode = simpledialog.askstring("Input", "Enter the product barcode:")
    if barcode:
        analysis.product_chart(barcode)

add_button = tk.Button(scan_bill_frame, text="Scan Product", command=add_to_cart, bg="#28a745", fg="white", font=("Arial", 12))
add_button.pack(pady=10)

cart_list = tk.Listbox(scan_bill_frame, width=50, height=10) 
cart_list.pack()

total_label = tk.Label(scan_bill_frame, text="Total: $0.00", font=("Arial", 17), bg="white", fg="#333")
total_label.pack()

bill_button = tk.Button(scan_bill_frame, text="Generate Bill", command=generate_bill, bg="#28a745", fg="white", font=("Arial", 12))
bill_button.pack(pady=10)

add_product_button = tk.Button(add_product_frame, text="Add Product", command=add_product_ui, bg="#28a745", fg="white", font=("Arial", 12))
add_product_button.pack(pady=10)

analysis_button = tk.Button(analysis_frame, text="Show Sales Analysis", command=show_sales_analysis, bg="#28a745", fg="white", font=("Arial", 12))
analysis_button.pack(pady=10)

product_sales_button = tk.Button(analysis_frame, text="Show Product Sales Analysis", command=show_product_sales_analysis, bg="#28a745", fg="white", font=("Arial", 12))
product_sales_button.pack(pady=10)

product_list_button = tk.Button(product_list_frame, text="Display Products", command=display_products, bg="#28a745", fg="white", font=("Arial", 12))
product_list_button.pack(pady=10)

show_frame(scan_bill_frame)

root.mainloop()