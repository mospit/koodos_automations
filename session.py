import asyncio
import time
import tqdm
from playwright.async_api import async_playwright
from bot import Bot, BotCluster
from helper import Helper

class Session:
    def __init__(self, user_data):
        self.data = Helper.get_data()
        self.n_failed = 0
        self.n_passed = 0
        self.processes = 5
        self.n_websites = len(self.data)
        self.bots = []
    
        self.user_data = user_data

        for i in range(self.n_websites):
            bot = Bot(self.data[i]['sequence']['url'], self.data[i]['sequence']['sequence'], self.user_data)
            self.bots.append(bot)

    async def run(self):
        try:
            async with async_playwright() as p:
                start_time = time.time()

                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()

                tasks = []
                results = []
                errors = []
                sem = asyncio.Semaphore(self.processes)

                for i, bot in enumerate(self.bots):
                    tasks.append(bot.run(context, sem))

                # Retrieve results from running bots
                bot_results = await asyncio.gather(*tasks)
                results.extend(bot_results)

                for bot_result in results:
                    if bot_result is not None:
                        ran, bot_errors = bot_result  # Unpack bot's result
                        n_passed += 1 if ran else 0  # Store the ran status
                        errors.extend(bot_errors)  # Extend the errors list with bot-specific errors
                    else:
                        # Handle the case where bot_result is None
                        errors.append("Bot result is None")

                n_passed = sum(results)  # Count the number of successful runs
                n_failed = self.n_websites - n_passed  # Calculate failed runs

                # Printing errors, counts, success rate
                print(f"Errors: {errors}")
                print(f"Total passed: {n_passed} Total Failed: {n_failed} Total websites: {len(self.data)} Success rate: {(n_passed / len(self.data)) * 100} %")
                end_time = time.time()  # Get the current time again

                execution_time = end_time - start_time  # Calculate the time difference
                print(f"Execution time: {execution_time} seconds")
        except Exception as e:
            print(f"Exeption: {e}")