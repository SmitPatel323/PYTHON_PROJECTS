import sqlite3
import matplotlib.pyplot as plt

def display_sales_chart():
    conn = sqlite3.connect('supermart.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT date, total_price FROM sales ORDER BY date')
    sales_data = cursor.fetchall()

    cursor.execute("""
        SELECT name, SUM(total_sales) AS total_sales
        FROM product_sale
        GROUP BY name
        ORDER BY total_sales DESC limit 10
    """)
    product_data = cursor.fetchall()
    conn.close()

    if not sales_data and not product_data:
        print('No sales data available.')
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(19.2, 10.8),gridspec_kw={'hspace': 0.5 })
    if sales_data:
        dates, totals = zip(*sales_data)   
        ax1.plot(dates, totals, marker='o', linestyle='-', color='b', label='Sales Trend')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Total Sales ($)')
        ax1.set_title('Supermart Sales Analysis')
        ax1.set_xticks(dates)
        ax1.set_xticklabels(dates, rotation=45)
        ax1.legend()

    if product_data:
        names, totals = zip(*product_data)
        ax2.bar(names, totals)
        ax2.set_title("Product Sales")
        ax2.set_xlabel("Products")
        ax2.set_ylabel("Total Sales")
        ax2.set_xticks(names)
        ax2.set_xticklabels(names, rotation=90)
    plt.show()

def product_chart(barcode):
    conn = sqlite3.connect('supermart.db')
    cursor = conn.cursor()
    cursor.execute('SELECT date, total_sales FROM product_sale WHERE barcode=? ORDER BY date', (barcode,))
    product_sales_data = cursor.fetchall()
    conn.close()

    if not product_sales_data:
        print('No sales data available for this product.')
        return

    dates, total_sales = zip(*product_sales_data)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, total_sales, marker='o', linestyle='-', color='g', label='Product Sales Trend')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.title('Sales Analysis for Product Barcode: {}'.format(barcode))
    plt.xticks(dates, rotation=45)
    plt.legend()
    plt.show()
