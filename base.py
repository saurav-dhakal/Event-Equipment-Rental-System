
from datetime import datetime

class Equipment:
    def __init__(self, name, brand, price, qty):
        self.name = name
        self.brand = brand
        self.price = price
        self.qty = qty

class RentalShop:
    def __init__(self, equipment_file):
        self.equipment_list = []
        self.load_equipment(equipment_file)
    
    def load_equipment(self, equipment_file):
        with open(equipment_file, 'r') as file:
            for line in file:
                data = line.strip().split(', ')
                name, brand, price, qty = data
                equipment = Equipment(name, brand, float(price), int(qty))
                self.equipment_list.append(equipment)
    
    def display_equipment(self):
        for idx, equipment in enumerate(self.equipment_list, start=1):
            print(f"{idx}. {equipment.name} ({equipment.brand}) - ${equipment.price:.2f} per 5 days, qty: {equipment.qty}")
    
    def generate_invoice(self, customer_name, rented_items):
        total_amount = 0
        invoice_text = f"Invoice for {customer_name}\n"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        for item in rented_items:
            equipment = self.equipment_list[item - 1]
            invoice_text += f"Item: {equipment.name} ({equipment.brand}) - ${equipment.price:.2f}\n"
            total_amount += equipment.price
        
        invoice_text += f"Total amount: ${total_amount:.2f}\n"
        invoice_text += f"Date and Time: {timestamp}\n"
        
        return invoice_text, total_amount
    
    def rent_equipment(self, customer_name, items):
        invoice_text, total_amount = self.generate_invoice(customer_name, items)
        invoice_filename = f"invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        
        with open(invoice_filename, 'w') as file:
            file.write(invoice_text)
        
        for item in items:
            self.equipment_list[item - 1].qty -= 1
        
        return total_amount, invoice_filename
    
    def return_equipment(self, customer_name, item):
        equipment = self.equipment_list[item - 1]
        rental_duration = 5  
        rental_fee = equipment.price
        
        return_date = datetime.now()
        return_date_str = return_date.strftime("%Y-%m-%d %H:%M:%S")
        
        if rental_duration < (return_date - datetime.strptime(return_date_str, "%Y-%m-%d %H:%M:%S")).days:
            late_days = (return_date - datetime.strptime(return_date_str, "%Y-%m-%d %H:%M:%S")).days - rental_duration
            fine = late_days * (rental_fee * 0.2) 
            invoice_text = f"Late return by {late_days} days.\nFine: ${fine:.2f}\n"
            invoice_text += f"Total amount due: ${rental_fee + fine:.2f}\n"
        else:
            invoice_text = f"Equipment returned on time.\nTotal amount due: ${rental_fee:.2f}\n"
        
        invoice_text += f"Date and Time of Return: {return_date_str}\n"
        invoice_filename = f"return_invoice_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        
        with open(invoice_filename, 'w') as file:
            file.write(invoice_text)
        
        equipment.qty += 1
        
        return invoice_filename

def main():
    equipment_file = "equipment.txt"
    rental_system = RentalShop(equipment_file)
    
    while True:
        print("\nWelcome to Upama's Rental Shop!")
        print("1. Display Available Equipment")
        print("2. Rent Equipment")
        print("3. Return Equipment")
        print("4. Exit")
        choice = int(input("Please select an option: "))
        
        if choice == 1:
            print("\nAvailable Equipment:")
            rental_system.display_equipment()
        
        elif choice == 2:
            customer_name = input("Enter customer name: ")
            rental_system.display_equipment()
            items = [int(x) for x in input("Enter the items number to rent (separated by spaces): ").split()]
            total_amount, invoice_filename = rental_system.rent_equipment(customer_name, items)
            print(f"\nTotal amount to be paid: ${total_amount:.2f}")
            print(f"Invoice saved as '{invoice_filename}'")
        
        elif choice == 3:
            customer_name = input("Enter customer name: ")
            rental_system.display_equipment()
            item = int(input("Enter the number of the item being returned: "))
            invoice_filename = rental_system.return_equipment(customer_name, item)
            print(f"\nReturn transaction completed.")
            print(f"Invoice saved as '{invoice_filename}'")
        
        elif choice == 4:
            print("Thank you for using the Event Equipment Rental Shop!")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
