# Veliswa Boya
# Student Number: 402601157
# BSc: IT, 2026S1PR511AD
# 2026 Semester 1

import math
from datetime import datetime

# Global constants 

USER_FILE = "user.txt"
PARKING_FILE = "parking.txt"
PAYMENTS_FILE = "payments.txt"

# Mall information (global constants)

MALL_IDS = ["MALL001", "MALL002", "MALL003"]
MALL_NAMES = ["Gateway Theatre of Shopping", "Pavilion Shopping Centre", "La Lucia Mall"]
MALL_LOCATIONS = ["Umhlanga, Durban", "Westville, Durban", "La Lucia, Durban"]
MALL_CAPACITIES = [250, 180, 150]
MALL_PRICING_TYPES = ["flat", "hourly", "capped"]
MALL_RATES = [15.00, 10.00, 12.00]
MALL_CAPS = [0, 0, 60.00]

# Global variables

current_username = ""
current_role = ""
current_mall_id = ""
selected_mall_index = -1

def read_user_file():
    """Read all users from file and return as list of lists"""
    users = []
    try:
        with open(USER_FILE, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    users.append(parts)
    except FileNotFoundError:
        pass
    return users

# whether use is a driver, admin, or owner/stakeholder, they will all be written here,
# with their corresponding role type.

def write_user_to_file(username, password, role, mall_id):
    """Add a new user to the user file"""
    with open(USER_FILE, 'a') as file:
        file.write(username + '|' + password + '|' + role + '|' + mall_id + '\n')

# read this file to check status of parked car, this file is relevant for all roles, for different uses.

def read_parking_records():
    """Read all parking records from file"""
    records = []
    try:
        with open(PARKING_FILE, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    records.append(parts)
    except FileNotFoundError:
        pass
    return records

# adding a new parking record when driver requests to park at a selected mall.

def write_parking_record(record_id, username, mall_id, car_reg, entry_time, exit_time, fee, paid):
    """Add a new parking record"""
    with open(PARKING_FILE, 'a') as file:
        file.write(record_id + '|' + username + '|' + mall_id + '|' + car_reg + '|' + entry_time + '|' + exit_time + '|' + str(fee) + '|' + str(paid) + '\n')

# the parking file is updated when entry, exit, fee for parking.

def update_parking_record(record_id, exit_time, fee): 
    
    """Update a parking record with exit time and fee"""
    records = read_parking_records()
    for record in records:
        if record[0] == record_id:
            record[5] = exit_time
            record[6] = str(fee)
            break

# Write updated parking records back to file after updating with exit time and fee.
# This info will be used later when user is making payment.

    with open(PARKING_FILE, 'w') as file:
        for record in records:
            file.write('|'.join(record) + '\n')

# mark a parking record as paid as soon as the driver pays it on the Driver activities menu.

def mark_record_as_paid(record_id):
    """Mark a parking record as paid"""
    records = read_parking_records()
    for record in records:
        if record[0] == record_id:
            record[7] = 'yes'
    # Write updated records back to file
    with open(PARKING_FILE, 'w') as file:
        for record in records:
            file.write('|'.join(record) + '\n')

def write_payment_to_file(payment_id, record_id, username, mall_id, amount, payment_time):
    """Append a payment record to file"""
    with open(PAYMENTS_FILE, 'a') as file:
        file.write(payment_id + '|' + record_id + '|' + username + '|' + mall_id + '|' + str(amount) + '|' + payment_time + '\n')

def read_payments():
    """Read all payment records from file"""
    payments = []
    try:
        with open(PAYMENTS_FILE, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    payments.append(parts)
    except FileNotFoundError:
        pass
    return payments


def calculate_parking_fee(mall_index, duration_hours):
    """Calculate parking fee based on mall type and duration"""
    pricing_type = MALL_PRICING_TYPES[mall_index]
    rate = MALL_RATES[mall_index]
      
    if pricing_type == "flat":
        return rate
    elif pricing_type == "hourly":
        hours = math.ceil(duration_hours)
        return hours * rate
    elif pricing_type == "capped":
        cap = MALL_CAPS[mall_index]
        hours = math.ceil(duration_hours)
        uncapped_fee = hours * rate 
        if uncapped_fee > cap: 
            return cap
        else:
            return uncapped_fee
    else:
        return 0.0
    
def calculate_duration_hours(entry_time_str, exit_time_str):
    """Calculate duration in hours between two datetime strings"""
    entry_time = datetime.fromisoformat(entry_time_str)
    exit_time = datetime.fromisoformat(exit_time_str)
    duration_seconds = (exit_time - entry_time).total_seconds()
    duration_hours = duration_seconds / 3600
    return duration_hours

# is the parking full? 
def count_active_cars(mall_id):
    """Count cars currently parked at the mall"""
    records = read_parking_records()
    count = 0

# if the exit time in the parking record (parking.txt file) is empty, then the car is still parked.
    for record in records:
        if record[2] == mall_id and record[5] == "":
            count = count + 1

    return count

def register_user():
    """Register new user"""
    print("User Registration")
    username = input("Enter username: ").strip()

    users = read_user_file()
    for user in users:
        if user[0] == username:
            print("Username already exists!")
            return
        
    password = input("Enter password: ").strip()
    print("Are you ---?")
    print("1: A driver")
    print("2: An admin")
    print("3: An owner of a mall")

    role_choice = input("Select (1-3): ").strip()

    if role_choice == "1":
        role = "driver"
        mall_id = "none"
    elif role_choice == "2":
        role = "admin"
        display_malls()
        mall_choice = input("Assign to mall (1-3): ").strip()
        if mall_choice in ["1", "2", "3"]:
            mall_id = MALL_IDS[int(mall_choice) - 1]
        else:
            print("Invalid mall selection!")
            return
    elif role_choice == "3":
        role = "owner"     # owner or stakeholder
        mall_id = "none"
    else:
        print("Invalid role selection!")
        return
    
    write_user_to_file(username, password, role, mall_id)
    print("User registered successfully!")


def login():
    """Login a user"""
    global current_username, current_role, current_mall_id

    print("User Login")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    users = read_user_file()
    for user in users:
        if user[0] == username and user[1] == password:
            current_username = username
            current_role = user[2]
            current_mall_id = user[3]
            print("Login successful. Welcome, " + username + "!")
            return True

    print("Invalid username or password!")
    return False


def logout():
    """Logout current user"""
    global current_username, current_role, current_mall_id, selected_mall_index
    current_username = ""
    current_role = ""
    current_mall_id = ""
    selected_mall_index = -1
    print("You have been logged out.")


def display_malls():
    """Display all available malls"""
    print("Available malls: ")
    for i in range(len(MALL_IDS)):
        print(str(i+1) + ". " + MALL_NAMES[i] + " (" + MALL_LOCATIONS[i] + ") - Capacity: " + str(MALL_CAPACITIES[i]))


def select_mall():
    """Allow driver to select a mall"""
    global selected_mall_index

    display_malls()
    choice = input("Select mall (1-3): ").strip()

    if choice in ["1", "2", "3"]:
        selected_mall_index = int(choice) - 1
        print("Selected: " + MALL_NAMES[selected_mall_index])
        return True
    else:
        print("Invalid selection!")
        return False
    

def register_car_entry():
    """Register car entry for driver"""
    if selected_mall_index == -1:
        print("Please select a mall first!")
        return
    
    mall_id = MALL_IDS[selected_mall_index]
    capacity = MALL_CAPACITIES[selected_mall_index]
    current_cars = count_active_cars(mall_id)

    if current_cars >= capacity:
        print("Sorry, " + MALL_NAMES[selected_mall_index] + " parking is full!")
        return

    records = read_parking_records()
    for record in records:
        if record[1] == current_username and record[2] == mall_id and record[5] == "":
            print("You already have a car parked at this mall!")
            return
        
    car_reg = input("Enter car registration number: ").strip()
    entry_time = datetime.now().isoformat()

    record_id = "REC" + str(len(records) + 1).zfill(6)

    write_parking_record(record_id, current_username, mall_id, car_reg, entry_time, "", "0", "no")

    print("Car registered successfully!")
    print("Record ID: " + record_id)
    print("Car: " + car_reg)
    print("Entry time: " + entry_time)


def register_car_exit():
    """Register car exit and calculate fee"""
    if selected_mall_index == -1:
        print("Please select a mall first!")
        return

    mall_id = MALL_IDS[selected_mall_index]
    records = read_parking_records()

# Find active record for this user and mall
    active_record = None
    for record in records:
        if record[1] == current_username and record[2] == mall_id and record[5] == "":
            active_record = record
            break

    if active_record is None:
        print("No active parking record found for this mall!")
        return

    exit_time = datetime.now().isoformat()
    duration_hours = calculate_duration_hours(active_record[4], exit_time)
    fee = calculate_parking_fee(selected_mall_index, duration_hours)

# Update parking record with exit time and fee
    update_parking_record(active_record[0], exit_time, fee)

    print("Car exited successfully!")
    print("Record ID: " + active_record[0])
    print("Car: " + active_record[3])
    print("Entry time: " + active_record[4])
    print("Exit time: " + exit_time)
    print("Duration: " + str(round(duration_hours, 2)) + " hours")
    print("Amount payable: R" + str(round(fee, 2)))

def make_payment():
    """Process payment for parking"""
    car_reg = input("Enter car registration number: ").strip()

    records = read_parking_records()
    target_record = None

    for record in records:
        if record[1] == current_username and record[3] == car_reg and record[7] == "no" and record[5] != "":
            target_record = record
            break
    if target_record is None:
        print("No unpaid parking record found for car " + car_reg + ".")
        return

    mark_record_as_paid(target_record[0])

    payments = read_payments()
    payment_id = "PAY" + str(len(payments) + 1).zfill(6)
    payment_time = datetime.now().isoformat()

    write_payment_to_file(payment_id, target_record[0], target_record[1], target_record[2], target_record[6], payment_time)
    print("Payment successful!")
    print("Payment ID: " + payment_id)
    print("Amount paid: R" + target_record[6])


def view_parking_history():
    """Display driver's parking history"""
    records = read_parking_records()
    user_records = []

    for record in records:
        if record[1] == current_username:
            user_records.append(record)

    if len(user_records) == 0:
        print("No parking history found.") 
        return

    print("Your parking history")
    for record in user_records:
        mall_index = MALL_IDS.index(record[2])
        print("Record ID : " + record[0])
        print("Mall: " + MALL_NAMES[mall_index])
        print("Car: " + record[3])
        print("Entry time: " + record[4])
        if record[5] == "":
            print("Exit time: Active/Still parked")
        else:
            print("Exit: " + record[5])
        if record[6] != "0":
            print("Fee: R" + record[6])
        print("Status: " + ("Paid" if record[7] == "yes" else "Unpaid"))

def view_parking_fee():
    """View fee for an unpaid exited record before payment"""
    records = read_parking_records()
    pending = []

    for record in records:
        if record[1] == current_username and record[5] != "" and record[7] == "no":
            pending.append(record)

    if len(pending) == 0:
        print("No unpaid parking records found.")
        return

    for record in pending:
        mall_index = MALL_IDS.index(record[2])
        print("Record ID: " + record[0])
        print("Mall: " + MALL_NAMES[mall_index])
        print("Car: " + record[3])
        print("Entry time: " + record[4])
        print("Exit time: " + record[5])
        print("Fee due: R" + record[6])
        print("------------------------")


def view_payment_history():
    """Display driver's payment history"""
    payments = read_payments()
    user_payments = []

    for payment in payments:
        if payment[2] == current_username:
            user_payments.append(payment)

    if len(user_payments) == 0:
        print("No payment history found.")
        return

    print("Your payment history:")
    for payment in user_payments:
        mall_index = MALL_IDS.index(payment[3])
        print("Payment ID: " + payment[0])
        print("Record ID: " + payment[1])
        print("Mall: " + MALL_NAMES[mall_index])
        print("Amount paid: R" + payment[4])
        print("Payment time: " + payment[5])
        print("------------------------")


def view_current_status():
        """Display driver's current parking status"""
        records = read_parking_records()
        active_records = []
        
        for record in records:
            if record[1] == current_username and record[5] == "":
                active_records.append(record)

        if len(active_records) == 0:
            print("You have no active parking sessions.")
            return
        
        print("Your current active parking status:")
        for record in active_records:
            mall_index = MALL_IDS.index(record[2])
            print("Record ID: " + record[0])
            print("Mall: " + MALL_NAMES[mall_index])
            print("Car: " + record[3])
            print("Entry time: " + record[4])
            print("Status: Active/Still parked")
            print("------------------------")

def view_mall_capacity():
    """Monitor parking capacity at admin's assigned mall"""
    mall_index = MALL_IDS.index(current_mall_id)
    capacity = MALL_CAPACITIES[mall_index]
    current_count = count_active_cars(current_mall_id)
    available = capacity - current_count

    print("Parking capacity at " + MALL_NAMES[mall_index])
    print("Total capacity: " + str(capacity))
    print("Currently occupied: " + str(current_count))
    print("Available spaces: " + str(available))


def view_daily_activity():
    """View today's parking activity at admin's assigned mall"""
    records = read_parking_records()
    today = datetime.now().date().isoformat()
    daily_records = []

    for record in records:
        if record[2] == current_mall_id and record[4].startswith(today):
            daily_records.append(record)

    mall_index = MALL_IDS.index(current_mall_id)
    print("Daily activity for " + MALL_NAMES[mall_index] + " on " + today)
    print("Total cars today: " + str(len(daily_records)))

    for record in daily_records:
        print("Record ID: " + record[0])
        print("Driver: " + record[1])
        print("Car: " + record[3])
        print("Entry time: " + record[4])
        if record[5] == "":
            print("Status: Still parked")
        else:
            print("Exit time: " + record[5])
            print("Fee: R" + record[6])
            print("Paid: " + ("Yes" if record[7] == "yes" else "No"))
        print("------------------------")


def view_mall_cars():
    """Display cars at admin's assigned mall"""
    records = read_parking_records()
    active_records = []

    for record in records:
        if record[2] == current_mall_id and record[5] == "":
            active_records.append(record)

    mall_index = MALL_IDS.index(current_mall_id)
    current_count = len(active_records)
    capacity = MALL_CAPACITIES[mall_index]

    print("Cars at " + MALL_NAMES[mall_index] + " (" + str(current_count) + "/" + str(capacity) + " occupied)")
    if len(active_records) == 0:
        print("No cars currently parked at this mall.")
    else:
        for record in active_records:
            print("Record ID: " + record[0])
            print("Driver: " + record[1])
            print("Car: " + record[3])
            print("Entry time: " + record[4])
            print("------------------------")


def generate_mall_report():
    """Generate report for a specific mall"""
    records = read_parking_records()
    mall_records = []

    mall_id = current_mall_id
    for record in records:
        if record[2] == mall_id and record[5] != "":
            mall_records.append(record)

    mall_index = MALL_IDS.index(mall_id)
    total_cars = len(mall_records)
    total_revenue = 0.0
    total_duration = 0.0

    for record in mall_records:
        if record[7] == "yes":
            total_revenue = total_revenue + float(record[6])
            duration = calculate_duration_hours(record[4], record[5])
            total_duration = total_duration + duration

    if total_cars > 0:
        avg_duration = total_duration / total_cars
    else:
        avg_duration = 0.0

    print("Mall Report for " + MALL_NAMES[mall_index])
    print("Total cars parked: " + str(total_cars))
    print("Total revenue: R" + str(round(total_revenue, 2)))
    print("Average duration: " + str(round(avg_duration, 2)) + " hours")


def generate_cross_mall_report():
    """Generate comparison report across all malls"""
    print("Cross mall comparison report")

    for i in range(len(MALL_IDS)):
        mall_id = MALL_IDS[i]
        records = read_parking_records()
        mall_records = []

        for record in records:
            if record[2] == mall_id and record[5] != "":
                mall_records.append(record) 

        total_cars = len(mall_records)
        total_revenue = 0.0
        total_duration = 0.0

        for record in mall_records:
            if record[7] == "yes":
                total_revenue = total_revenue + float(record[6])
                duration = calculate_duration_hours(record[4], record[5])
                total_duration = total_duration + duration

        if total_cars > 0:
            avg_duration = total_duration / total_cars
        else:
            avg_duration = 0.0

        print("Mall: " + MALL_NAMES[i])
        print(" Total cars: " + str(total_cars))
        print(" Total revenue: R" + str(round(total_revenue, 2)))
        print(" Average duration: " + str(round(avg_duration, 2)) + " hours")
        print()


def driver_menu():
    """Display driver activities"""
    while True:
        print("\n--- Driver activities ---")
        print("1. Select mall")
        print("2. Register car entry")
        print("3. Register car exit")
        print("4. View parking fee")
        print("5. Make payment")
        print("6. View current status")
        print("7. View parking history")
        print("8. View payment history")
        print("9. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            select_mall()
        elif choice == "2":
            register_car_entry()
        elif choice == "3":
            register_car_exit()
        elif choice == "4":
            view_parking_fee()
        elif choice == "5":
            make_payment()
        elif choice == "6":
            view_current_status()
        elif choice == "7":
            view_parking_history()
        elif choice == "8":
            view_payment_history()
        elif choice == "9":
            logout()
            break
        else:
            print("Invalid choice!")


def admin_menu():
    """Display and handle admin activities"""
    while True:
        print("\n--- Admin activities ---")
        print("1. View cars currently parked")
        print("2. Monitor parking capacity")
        print("3. View daily parking activity")
        print("4. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_mall_cars()
        elif choice == "2":
            view_mall_capacity()
        elif choice == "3":
            view_daily_activity()
        elif choice == "4":
            logout()
            break
        else:
            print("Invalid choice!")


def owner_menu():
    """Display and handle mall owner activities"""
    while True:
        print("\n--- Mall owner activities ---")
        print("1. Generate cross-mall report")
        print("2. View mall details")
        print("3. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            generate_cross_mall_report()
        elif choice == "2":
            for i in range(len(MALL_NAMES)):
                print(str(i+1) + ". " + MALL_NAMES[i] + " - " + MALL_LOCATIONS[i] + " - Capacity: " + str(MALL_CAPACITIES[i]))
        elif choice == "3":
            logout()
            break
        else:
            print("Invalid choice!")


def main():
    """Main function to run the application"""

    while True:
        print("\n=== KZN Smart Mall Parking Management System ===")
        print("1. Register (if using the system for the first time)")
        print("2. Login (if already registered)")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            if login():
                if current_role == "driver":
                    driver_menu()
                elif current_role == "admin":
                    admin_menu()
                elif current_role == "owner":
                    owner_menu()
        elif choice == "3":
            print("Thank you for using KZN Smart Mall Parking Management System!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()




