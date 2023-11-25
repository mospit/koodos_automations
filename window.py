from cgitb import text
import tkinter as tk
from tkinter import ttk
from session import Session
from helper import Helper
import pandas as pd
import string
import random

class Window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Koodos Automations")
        self.window.geometry("600x400")

        # Title
        self.title_label = ttk.Label(master=self.window, text="PR BOT", font="Calibri 24 bold")
        self.title_label.pack()

        # Frames    
        self.form_frame = ttk.Frame(master=self.window)
        self.header_frame = ttk.Frame(master=self.form_frame)
        self.contact_label_frame = ttk.Frame(master=self.window)
        self.contact_frame = ttk.Frame(master=self.form_frame)
        self.residental_frame = ttk.Frame(master=self.form_frame)
        self.footer_frame = ttk.Frame(master=self.form_frame)

        options = Helper.load_user_data(1)  # Example list of options

        self.variable = tk.StringVar(self.window)
        self.variable.set(options[0])  # Set default option
        # Contact entries
        self.first_name_label = ttk.Label(master=self.contact_frame, text="First Name")
        self.first_name_entry = ttk.Entry(master=self.contact_frame)

        self.last_name_label = ttk.Label(master=self.contact_frame, text="Last Name")
        self.last_name_entry = ttk.Entry(master=self.contact_frame)

        self.phone_label = ttk.Label(master=self.contact_frame, text="Phone")
        self.phone_entry = ttk.Entry(master=self.contact_frame)

        self.email_label = ttk.Label(master=self.contact_frame, text="Email")
        self.email_entry = ttk.Entry(master=self.contact_frame)

        # Residental entries
        self.street1_label = ttk.Label(master=self.residental_frame, text="Street1")
        self.street1_entry = ttk.Entry(master=self.residental_frame)

        self.street2_label = ttk.Label(master=self.residental_frame, text="Street2")
        self.street2_entry = ttk.Entry(master=self.residental_frame)

        self.city_label = ttk.Label(master=self.residental_frame, text="City")
        self.city_entry = ttk.Entry(master=self.residental_frame)

        self.state_label = ttk.Label(master=self.residental_frame, text="State")
        self.state_entry = ttk.Entry(master=self.residental_frame)

        self.zip_label = ttk.Label(master=self.residental_frame, text="Zip")
        self.zip_entry = ttk.Entry(master=self.residental_frame)

        self.run_button = ttk.Button(master=self.footer_frame, text="RUN", command=self._run)
        self.upload_button = ttk.Button(master=self.footer_frame, text="Upload User Data", command=Helper.upload_csv)
        self.option_menu = tk.OptionMenu(self.footer_frame, self.variable, *options, command=self.on_option_select)

    def _create_grid(self):
        self.first_name_label.grid(column=0, row=0)
        self.last_name_label.grid(column=1, row=0)
        self.phone_label.grid(column=2, row=0)
        self.email_label.grid(column=3, row=0)

        self.first_name_entry.grid(column=0, row=1)
        self.last_name_entry.grid(column=1, row=1)
        self.phone_entry.grid(column=2, row=1)
        self.email_entry.grid(column=3, row=1)

        # Residental frame grid
        self.street1_label.grid(column=0, row=0, padx=5)
        self.street2_label.grid(column=1, row=0, padx=5)
        self.city_label.grid(column=0, row=2, padx=5)
        self.state_label.grid(column=1, row=2, padx=5)
        self.zip_label.grid(column=2, row=2, padx=5)

        self.street1_entry.grid(column=0, row=1, padx=5)
        self.street2_entry.grid(column=1, row=1, padx=5)
        self.city_entry.grid(column=0, row=3, padx=5)
        self.state_entry.grid(column=1, row=3, padx=5)
        self.zip_entry.grid(column=2, row=3, padx=5)

        # Adjustments for the grid layout of frames
        self.contact_frame.grid(column=0, row=0)  # Place contact frame in the grid
        self.residental_frame.grid(column=0, row=1)  # Place residential frame in the grid

        self.run_button.grid(column=0, row=2)
        self.upload_button.grid(column=1, row=2)
        self.option_menu.grid(column=2, row=2)
        self.footer_frame.grid(column=0, row=2)
        self.form_frame.pack()

    def _get_input_feilds(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        street1 = self.street1_entry.get()
        street2 = self.street2_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zip_code = self.zip_entry.get()
        print(f"first name: {first_name}, last name:{last_name}, phone: {phone}, email: {self.email}, street1: {self.street1}, street2: {self.street2}, city: {self.city}, state: {self.state}, zip code: {self.zip_code}")
        return {"firstName": first_name, "lastName": last_name, "fullName": "Sarah Smith", "email": "jw8ia6dqsx@sfolkar.com",
                "phone": phone, "password": self._generate_password(), "zipcode": zip_code}

    def _generate_password(self, length=12, include_uppercase=True, include_lowercase=True, include_digits=True, include_special=True):
        chars = ''
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_digits:
            chars += string.digits
        if include_special:
            chars += string.punctuation

        # Make sure the password length is at least 4 characters
        length = max(length, 4)

        # Generate the password
        password = ''.join(random.choice(chars) for _ in range(length))
        return password

    def _run(self):
        user_data = self._get_input_feilds()
        session = Session(user_data)
        session.run()

    def on_option_select(self, event):
        selected_option = self.variable.get()
        print(f"Selected option: {selected_option}")

    def show(self):
        self._create_grid()
        self.window.mainloop()
