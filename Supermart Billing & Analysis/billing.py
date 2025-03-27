from datetime import datetime
import database
def generate_bill(cart, total_price):
    with open("bill.txt", "w") as f:
        f.write("----- Supermart Bill -----\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-------------------------\n")
        
        for barcode, details in cart.items():
            f.write(f"{details['name']} x{details['quantity']} - ${details['price']} each\n")
            database.product_sales(barcode,details['name'],details['quantity']*details['price'])
        f.write("-------------------------\n")
        f.write(f"Total: ${total_price:.2f}\n")
        f.write("-------------------------\n")
        f.write("Thank you for shopping with us!\n")

def apply_discount(total_price, discount_code):
    discount_percentage = 0
    if discount_code == "SUPER10":
        discount_percentage = 10
    elif discount_code == "SUMMER15":
        discount_percentage = 15

    discount_amount = (total_price * discount_percentage) / 100
    return total_price - discount_amount
