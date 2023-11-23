import requests
import json

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
    