import asyncio
import time
from playwright.async_api import async_playwright
from bot import Bot, BotCluster
from helper import Helper

async def main():
    try:
        # Helper.save_data()
        data = Helper.get_data()
        n_failed = 0
        n_passed = 0
        processes = 5
        n_websites = len(data)
        bots = []
    
        user_data = {"firstName": "Sarah", "lastName": "Smith", "fullName": "Sarah Smith", "email": "9dbtyfhi7w@pirolsnet.com",
                     "phone": "5803114985", "password": "KawakiChapter@24", "zipcode": "78612"}

        for i in range(n_websites):
            bot = Bot(data[i]['sequence']['url'], data[i]['sequence']['sequence'], user_data)
            bots.append(bot)

        async with async_playwright() as p:
   
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context()

            tasks = []
            results = []
            sem = asyncio.Semaphore(processes)

            for i, bot in enumerate(bots):
                tasks.append(bot.run(context, sem))

            failed_bots_list = await asyncio.gather(*tasks)  # Gather results from run_bots()
            results.extend(failed_bots_list)  # Collect all results
            await browser.close()

            for idx, result in enumerate(results):
                if result: 
                    n_passed += 1
                else:
                    n_failed += 1
            print(f"Total passed: {n_passed} Total Failed: {n_failed} Total websits: {len(data)} Success rate: {(n_passed / len(data)) * 100} %")
    except Exception as e:
        print(f"Exeption: {e}")

if __name__ == "__main__":
    try:
        start_time = time.time()
        asyncio.run(main())
        end_time = time.time()  # Get the current time again

        execution_time = end_time - start_time  # Calculate the time difference
        print(f"Execution time: {execution_time} seconds")
    except Exception as e:
            print(f"Exception in main function execution: {e}")