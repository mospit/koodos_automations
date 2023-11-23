from http.client import FAILED_DEPENDENCY
from socket import timeout
from urllib import response
from urllib.robotparser import RequestRate
from helper import Helper as helper
import time 
from tqdm import tqdm

class BotCluster:
    def __init__(self, id, page, bots):
        self.id = id
        self.page = page
        self.bots = bots
        self.failed_bots = set()


    async def run_bots(self):
        count = 1
        for bot in self.bots:
            try:
                await bot.run(self.page) 

                if not bot.ran: 
                    self.failed_bots.add(bot)
                else:
                    print(f"<<<<< {bot.get_url()} Complete! >>>>>>")
            except Exception as e:
                self.failed_bots.add(bot)
                # Handle the exception, log it, or take appropriate action to continue
              
        await self.page.close() # close page once done
        return [self.failed_bots, len(self.failed_bots)]

class Bot:
    def __init__(self, url, sequence, user_data):
        self.ran = True
        self.url = url
        self.sequence = sequence
        self.inputs = {}
        self.user_data = user_data

        # fill in the inputs to insert into the webpage
        self.fill_input_hashtable()
        
    def get_url(self):
        return self.url
            
    def fill_input_hashtable(self):
        for s in self.sequence:
            if s["action"] == "Input":
                self.inputs[s["variable"]] = self.user_data[s["variable"]]

    async def intercept(self, route):
        if route.request.resource_type in {"stylesheet", 'image', 'fonts', 'script'}:
            await route.abort()
        else:
            await route.continue_()

    async def run(self, context, sem):   
        try:
            async with sem:
                print(f"Running: {self.get_url()}")
                # request interception
                await context.route('**/*', self.intercept)

                # Create page
                page = await context.new_page()
                await page.goto(self.get_url(), wait_until="domcontentloaded", timeout=0)
                
                # Run sequence
                for s in self.sequence:
                    if s["action"] == "Input":
                        await page.locator(s["identifier"]).fill( self.inputs[s["variable"]], timeout=2500)
            
                    elif s["action"] == "click":
                        if s["variable"] == "submit":
                            # Override default timeout for click action
                            await page.locator(s["identifier"]).click(timeout=2500)
                            self.ran = True
                        else:
                            await page.locator(s["identifier"]).click( timeout=2500)
                return self.ran
        except Exception as e:
            self.ran = False
            print(f" Exception in {self.get_url()}: {e}")