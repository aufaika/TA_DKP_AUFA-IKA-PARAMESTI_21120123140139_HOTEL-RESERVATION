import tkinter as tk
from tkinter import messagebox
from collections import deque
from tkcalendar import DateEntry
from datetime import datetime

#variabel
registered_users = {
    "user1": "password1",
    "user2": "password2"
}

reservations = {}

hotel_data = {
    "available_rooms": ["Standard", "Deluxe", "Suite"],
    "room_prices": {"Standard": 500_000, "Deluxe": 1_500_000, "Suite": 2_000_000},
    "breakfast_price": 50_000
}

# Queue 
date_queue = deque()

logged_in = False

#oop getter setter
class HotelReservation:
    def __init__(self):
        self._check_in = None
        self._check_out = None
        self._room_type = None
        self._breakfast = False
        self.room_prices = {
            'Standard': 500_000,
            'Deluxe': 1_500_000,
            'Suite': 2_000_000
        }

    def get_check_in(self):
        return self._check_in

    def set_check_in(self, check_in):
        self._check_in = check_in

    def get_check_out(self):
        return self._check_out

    def set_check_out(self, check_out):
        self._check_out = check_out

    def get_room_type(self):
        return self._room_type

    def set_room_type(self, room_type):
        self._room_type = room_type

    def get_breakfast(self):
        return self._breakfast

    def set_breakfast(self, breakfast):
        self._breakfast = breakfast

    def calculate_total(self):
        total_price = self.room_prices[self._room_type]
        if self._breakfast:
            total_price += 50_000
        return total_price

def login():
    global logged_in
    username = entry_username.get()
    password = entry_password.get()

#pengkondisian if else
    if username in registered_users and registered_users[username] == password:
        button_result.config(text="Login successful!", bg="green")
        logged_in = True
    else:
        button_result.config(text="Incorrect username or password.", bg="red")
        logged_in = False

def register():
    global logged_in
    username = entry_username.get()
    password = entry_password.get()

    if username in registered_users:
        button_result.config(text="Username already taken.", bg="red")
        logged_in = False
    else:
        registered_users[username] = password
        button_result.config(text="Registration successful!", bg="green")
        logged_in = True

def show_room_price(*args):
    room_type = variable_room_type.get()
    price = hotel_data["room_prices"][room_type]
    button_room_price.config(text="Room Price: Rp {}".format(price))

def choose_dates():
    if not logged_in:
        button_result.config(text="Please log in or register first.", bg="red")
        return

    checkin_date = entry_checkin_date.get_date().strftime("%Y-%m-%d")
    checkout_date = entry_checkout_date.get_date().strftime("%Y-%m-%d")

    checkin_date_dt = datetime.strptime(checkin_date, "%Y-%m-%d")
    checkout_date_dt = datetime.strptime(checkout_date, "%Y-%m-%d")

    if checkout_date_dt <= checkin_date_dt:
        button_result.config(text="Check-out date must be after check-in date.", bg="red")
    else:
        date_queue.append((checkin_date, checkout_date))
        button_result.config(text="Check-in Date: {}\nCheck-out Date: {}".format(checkin_date, checkout_date), bg="saddlebrown")

def calculate_total():
    if not logged_in:
        label_total.config(text="Please log in or register first.", bg="red")
        return

    room_type = variable_room_type.get()
    breakfast = variable_breakfast.get() == "Yes"

    # Get reservation data from queue
    if not date_queue:
        label_total.config(text="Please choose check-in and check-out dates.", bg="red")
        return

    checkin_date, checkout_date = date_queue.popleft()

    checkin_date_dt = datetime.strptime(checkin_date, "%Y-%m-%d")
    checkout_date_dt = datetime.strptime(checkout_date, "%Y-%m-%d")

    duration = (checkout_date_dt - checkin_date_dt).days

    reservation = HotelReservation()
    reservation.set_room_type(room_type)
    reservation.set_breakfast(breakfast)

    total_price = reservation.calculate_total() * duration

    label_total.config(text="Total Payment: Rp {}".format(total_price), bg="green")

window = tk.Tk()
window.title("Hotel Reservation")
window.geometry("400x580")
window.configure(bg="saddlebrown")

label_title = tk.Label(window, text="Welcome to Hotel 11", bg="saddlebrown", fg="wheat", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

label_username = tk.Label(window, text="Username:", bg="saddlebrown", fg="wheat")
label_username.pack()
entry_username = tk.Entry(window)
entry_username.pack()

label_password = tk.Label(window, text="Password:", bg="saddlebrown", fg="wheat")
label_password.pack()
entry_password = tk.Entry(window, show="*")
entry_password.pack()

button_login = tk.Button(window, text="Login", command=login, bg="wheat", fg="saddlebrown")
button_login.pack(pady=5)
button_register = tk.Button(window, text="Register", command=register, bg="wheat", fg="saddlebrown")
button_register.pack()

button_result = tk.Label(window, text="", bg="saddlebrown", fg="wheat")
button_result.pack(pady=5)

label_checkin_date = tk.Label(window, text="Check-in Date:", bg="saddlebrown", fg="wheat")
label_checkin_date.pack()
entry_checkin_date = DateEntry(window, date_pattern='yyyy-mm-dd')
entry_checkin_date.pack()

label_checkout_date = tk.Label(window, text="Check-out Date:", bg="saddlebrown", fg="wheat")
label_checkout_date.pack()
entry_checkout_date = DateEntry(window, date_pattern='yyyy-mm-dd')
entry_checkout_date.pack()

buttom_room_type = tk.Label(window, text="Room Type:", bg="saddlebrown", fg="wheat")
buttom_room_type.pack()

variable_room_type = tk.StringVar(window)
variable_room_type.set(hotel_data["available_rooms"][0])
option_menu_room_type = tk.OptionMenu(window, variable_room_type, *hotel_data["available_rooms"], command=show_room_price)
option_menu_room_type.pack()

button_room_price = tk.Label(window, text="Room Price : Rp", bg="wheat", fg="saddlebrown")
button_room_price.pack()

label_breakfast_price = tk.Label(window, text="Add Breakfast:", bg="saddlebrown", fg="wheat")
label_breakfast_price.pack()

button_breakfast_price = tk.Label(window, text="Breakfast Price: Rp {}".format(hotel_data["breakfast_price"]), bg="wheat", fg="saddlebrown")
button_breakfast_price.pack()

variable_breakfast = tk.StringVar(window)
variable_breakfast.set("No")
option_menu_breakfast = tk.OptionMenu(window, variable_breakfast, "Yes", "No")
option_menu_breakfast.pack()

button_choose_dates = tk.Button(window, text="Choose Dates", command=choose_dates, bg="wheat", fg="saddlebrown")
button_choose_dates.pack(pady=5)

button_calculate_total = tk.Button(window, text="Calculate Total", command=calculate_total, bg="wheat", fg="saddlebrown")
button_calculate_total.pack(pady=5)

label_total = tk.Label(window, text="Total Payment: Rp 0", bg="green", fg="wheat")
label_total.pack(pady=10)

window.mainloop()
