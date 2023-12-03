import asyncio
import time
import tqdm
from playwright.async_api import async_playwright
from bot import Bot
from helper import Helper

class Session:
    def __init__(self, user_data, num_websites=0):
        self.data = Helper.get_data()
        self.n_failed = 0
        self.n_passed = 0
        self.processes = 5
        self.n_websites = num_websites if num_websites > 0 else len(self.data)
        self.bots = []
    
        self.user_data = user_data

        for i in range(self.n_websites):
            bot = Bot(self.data[i]['sequence']['url'], self.data[i]['sequence']['sequence'], self.user_data)
            self.bots.append(bot)
        
    async def run(self):
        try:
            async with async_playwright() as p:
                start_time = time.time()
               
                n_context = 1
                browser = await p.firefox.launch(headless=True)
                context = []
                if self.n_websites > n_context:
                    for i in range(n_context):
                        c = await browser.new_context(user_agent=Helper.get_user_agent())
                        await c.add_init_script(path="program.js")
                        context.append(c)
                else:
                    context = await browser.new_context()

                tasks = []
                results = []
                errors = []
                sem = asyncio.Semaphore(self.processes)

                for i, bot in enumerate(self.bots):
                    idx = i % len(context)
                    tasks.append(bot.run(context[idx], sem))

                # Retrieve results from running bots
                bot_results = await asyncio.gather(*tasks)

                for result in bot_results:
                    website, logs = next(iter(result.items()))  # Unpack bot's result
                    if logs[0]:
                        self.n_passed += 1
                    for i in range(1, len(logs)):
                        errors.append(logs[i])
                    
                self.n_failed = self.n_websites - self.n_passed  # Calculate failed runs

                # Printing errors, counts, success rate
                Helper.create_error_log_csv(bot_results)
                print(f"Total passed: {self.n_passed} Total Failed: {self.n_failed} Total websites: {len(self.data)} Success rate: {(self.n_passed / self.n_websites) * 100} %")
                end_time = time.time()  # Get the current time again

                execution_time = end_time - start_time  # Calculate the time difference
                print(f"Execution time: {execution_time / 60} minutes | { execution_time/ self.n_websites} seconds per wesite")
        except Exception as e:
            print(f"Exeption: {e}")