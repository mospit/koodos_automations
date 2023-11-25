import asyncio
from window import Window

if __name__ == "__main__":
    try:
        window = Window()
        window.show()
    except Exception as e:
            print(f"Exception in main function execution: {e}")