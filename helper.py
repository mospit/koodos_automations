import requests
import json
import os
import pandas as pd
from tkinter import filedialog

class Helper:
    @staticmethod
    def save_data():
        url = 'https://hilarious-toad-boot.cyclic.app/'
        response = requests.get(url)
        if response.status_code == 200:
            with open('response_data.json', 'w') as json_file:
                json.dump(response.json(), json_file)
            print("Response saved as JSON file.")
        else:
            print("Request failed with status code:", response.status_code)
        return response.status_code
    
    @staticmethod
    def get_data():
        with open('response_data.json', 'r') as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def upload_csv():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if file_path:
            # Read the CSV file using pandas
            try:
                df = pd.read_csv(file_path)
                # Process the dataframe as needed (e.g., print or use the data)
                print("CSV file loaded successfully.")
                print(df.head())  # Print the first few rows as an example
            except pd.errors.EmptyDataError:
                print("The selected file is empty or invalid.")
        else:
            print("No file selected.")
    @staticmethod
    def load_user_data(option=0):
        people = pd.read_csv("user_data.csv")
        if option == 0:
            people = people
        elif option == 1:
            people = people["first_name"].tolist()
        return people
    