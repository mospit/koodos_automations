from http.client import FAILED_DEPENDENCY
from socket import timeout
from urllib import response
from urllib.robotparser import RequestRate
from helper import Helper as helper
import time 
from tqdm import tqdm

class Bot:
    def __init__(self, url, sequence, user_data):
        self.ran = None
        self.url = url
        self.sequence = sequence
        self.inputs = {}
        self.errors = []
        self.output = {}
        self.user_data = user_data
        self.output[self.get_url()] = []

        # fill in the inputs to insert into the webpage
        self.fill_input_hashtable()
        
    def get_url(self):
        return self.url
            
    def fill_input_hashtable(self):
        try:
            for s in self.sequence:
                if s["action"] == "Input":
                    self.inputs[s["variable"]] = self.user_data[s["variable"]]
        except Exception as e:
            print(f"fill input hashtable: {e}")


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
                #await context.route('**/*', self.intercept)

                # Create page
                page = await context.new_page()
                await page.goto(self.get_url(), wait_until="load")
                
                # Run sequence
                for s in self.sequence:
                    if s["action"] == "Input":
                        text = await self.fill(page, s["identifier"], self.inputs[s["variable"]])
                        if text is not self.inputs[s["variable"]]:
                            self.ran = False
                    elif s["action"] == "click":
                        if s["variable"] == "submit":
                            # Override default timeout for click action
                           # await page.locator(s["identifier"]).dispatch_event('click')
                            
                            await self.click(page, s["identifier"])
                            self.ran = True
                            await page.wait_for_timeout(2000)
                        else:
                            await page.locator(s["identifier"]).click(force=True)
                self.output[self.get_url()].append(self.ran)
                await page.close()
                time.sleep(1)
                return self.output
        except Exception as e:
            self.ran = False
            self.output[self.get_url()].append(self.ran)
            self.output[self.get_url()].append(e)
            await page.close()
            return self.output

    async def click(self, page, element):
        try:
            await page.locator(element).click(timeout=5000)
        except Exception as e:
            print(f"{self.get_url()}: click failed")
            await page.locator(element).dispatch_event('click')

    async def fill(self, page, element, text):
         try:
             await page.locator(element).press_sequentially(text, timeout=5000)  
             value = await page.locator(element).input_value()
             return value
         except Exception as e:
             print(f"{self.get_url()}: fill failed")
             await page.locator(element).fill( text, timeout=5000)
             value = await page.locator(element).input_value()
             return value
