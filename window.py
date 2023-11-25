from cgitb import text
import tkinter as tk
from tkinter import ttk
from session import Session
from helper import Helper
import pandas as pd
import string
import random
import asyncio

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

        self.options = Helper.load_user_data(1)  # Example list of options

        self.variable = tk.StringVar(self.window)
        self.variable.set(self.options[0])  # Set default option
        asyncio.run(self.create_elements())

    async def create_elements(self):
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

        self.website_cont_label = ttk.Label(master=self.footer_frame, text="# websites")
        self.website_cont_entry = ttk.Entry(master=self.footer_frame)
        self.website_cont_entry.insert(0, "0")
        self.run_button = ttk.Button(master=self.footer_frame, text="RUN", command=self._run_button_callback)
        self.upload_button = ttk.Button(master=self.footer_frame, text="Upload User Data", command=Helper.upload_csv)
        self.option_menu = tk.OptionMenu(self.footer_frame, self.variable, *self.options, command=self.on_option_select)

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

        self.website_cont_label = ttk.Label(master=self.footer_frame, text="# websites")
        self.website_cont_label.grid(column=0, row=2)
        self.website_cont_entry.grid(column=1, row=2)
        self.run_button.grid(column=2, row=2)
        self.upload_button.grid(column=3, row=2)
        self.option_menu.grid(column=4, row=2)
        self.footer_frame.grid(column=0, row=2)
        self.form_frame.pack()

    def _get_input_feilds(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        full_name = first_name + " " + last_name
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        street1 = self.street1_entry.get()
        street2 = self.street2_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zip_code = self.zip_entry.get()
        return {"firstName": first_name, "lastName": last_name, "fullName": full_name, "email": email,
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

    def _run_button_callback(self):
        # Run the async function using asyncio.run()
        asyncio.run(self._run())

    async def _run(self):
        user_data = self._get_input_feilds()
        num_websites = int(self.website_cont_entry.get())
        session = Session(user_data,num_websites)
        await session.run()

    def on_option_select(self, event):
        selected_option = self.variable.get()
        print(f"Selected option: {selected_option}")
        self._fill_fields(selected_option)

    def _fill_fields(self, p):
        person = Helper.load_user_data(option=2, person=p)
        print(f"person: {person}")
        self.first_name_entry.delete(0, tk.END)
        self.first_name_entry.insert(0, person[0][0])

        self.last_name_entry.delete(0, tk.END)
        self.last_name_entry.insert(0, person[0][1])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, person[0][2])

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, person[0][3])

        self.street1_entry.delete(0, tk.END)
        self.street1_entry.insert(0, person[0][4])

        self.street2_entry.delete(0, tk.END)
        self.street2_entry.insert(0, person[0][5])

        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, person[0][6])

        self.state_entry.delete(0, tk.END)
        self.state_entry.insert(0, person[0][7])

        self.zip_entry.delete(0, tk.END)
        self.zip_entry.insert(0, person[0][8])

    def show(self):
        self._create_grid()
        self.window.mainloop()
