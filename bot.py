from helper import Helper as helper
from playwright.async_api import async_playwright, expect

class Bot:
    def __init__(self, url, sequence, user_data):
        self.ran = None
        self.url = url
        self.sequence = sequence
        self.inputs = {}
        self.input_data = []
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
        if route.request.resource_type in {"stylesheet", 'image', 'fonts'}:
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
                await page.goto(self.get_url(), wait_until="load", timeout=0)
                
                # Run sequence
                for s in self.sequence:  
                    # Decide which action to take
                    element = await self.wait_for_element( page, s["identifier"])
                    
                    # Check if element exists
                    if element is None:
                        self.ran = False
                        msg = "Selector: " + s["identifier"] + " return none"
                        self.output[self.get_url()].append(self.ran)
                        self.output[self.get_url()].append(msg)
                        await page.close()
                        return self.output

                    # Scroll element into view
                    await element.scroll_into_view_if_needed()

                    if s["action"] == "Input":
                        # Check is the input can be edited
                        input_element = await self.wait_for_editable(page, s["identifier"])

                        if not input_element:
                            self.ran = False
                            msg = "Selector: " + s["identifier"] + " cannot be edited"
                            self.output[self.get_url()].append(self.ran)
                            self.output[self.get_url()].append(msg)
                            await page.close()
                            return self.output

                        # Try to insert tbe text into the input
                        await input_element.type(self.inputs[s["variable"]])
                        await input_element.dispatch_event("change")
                        value = await input_element.input_value()

                        # Check the value of the input
                        if not value.strip():
                            self.ran = False
                            msg = "Selector: " + s["identifier"] + " cannot insert " + self.inputs[s["variable"]]
                            self.output[self.get_url()].append(self.ran)
                            self.output[self.get_url()].append(msg)
                            await page.close()
                            return self.output
                        
                    elif s["action"] == "click":
                        # Click button
                        await element.evaluate('(el) => el.click()')
                
                self.ran = True # Set ran state 
                await page.wait_for_timeout(2000) # Wait niumber of miliseconds
                self.output[self.get_url()].append(self.ran)
                await page.close()
                return self.output
        except Exception as e:
            self.ran = False
            self.output[self.get_url()].append(self.ran)
            self.output[self.get_url()].append(e)
            await page.close()
            return self.output

    async def wait_for_element(self, page, selector, max_attempts=30):
        for _ in range(max_attempts):
            element = await page.query_selector(selector)
            if element and await element.is_visible() and await element.is_enabled():
                return element
            await page.wait_for_timeout(1000)  # Wait for 1 second before rechecking
        return None  # If conditions aren't met after max_attempts, return None

    
    async def wait_for_editable(self, page, selector, max_attempts=30):
        for _ in range(max_attempts):
            element = await page.query_selector(selector)
            if element and await element.is_editable():
                return element
            await page.wait_for_timeout(1000)  # Wait for 1 second before rechecking
        return None  # If element is not editable after max_attempts, return None
