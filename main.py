import asyncio
from helper import Helper
from window import Window

if __name__ == "__main__":
    try:
        #Helper.save_data()
        window = Window()
        window.show()
    except Exception as e:
            print(f"Exception in main function execution: {e}")