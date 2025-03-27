import cv2
from pyzbar.pyzbar import decode
import database

def scan_barcode():
    cap = cv2.VideoCapture(0) 

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        barcodes = decode(gray)

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            product = database.get_product(barcode_data)

            if product:
                stock_available = product[3]-1  
                if stock_available == 0:
                    print(f"Out of stock: {product[1]}")
                else:
                    print(f"Scanned: {product[1]} - ${product[2]} - {stock_available} in stock")
                    cap.release()
                    cv2.destroyAllWindows()
                    return product

        cv2.putText(frame, "Align barcode & press 'Q' to exit", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.imshow("Barcode Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
