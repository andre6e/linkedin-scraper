import configparser, csv, time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException

config = configparser.ConfigParser()
config.read('config.ini')

class Finders:
    # INIT

    def __init__(self, browser):
        print('Initializing Finders class')
        self.browser = browser

        # App config
        self.SLEEP_TIME = int(config['CONFIG']['SLEEP_TIME'])
        self.MAX_LOADING_ATTEMPTS = int(config['CONFIG']['MAX_LOADING_ATTEMPTS'])

    # HELPERS

    def save_screenshot(self, fn):
        self.browser.save_screenshot(fn)

    def refresh_page(self):
        print('Refreshing page!')
        self.browser.refresh()

    # SAFE FINDERS

    def safe_find_element_by_class_name(self, cname, el = None):
        el = el if el else self.browser

        try:
            return el.find_element_by_class_name(cname)
        except NoSuchElementException:
            return None
   
    def safe_find_element_by_id(self, id_param, el = None):
        el = el if el else self.browser

        try:
            return el.find_element_by_id(id_param)
        except NoSuchElementException:
            return None
  
    def safe_find_elements_by_class_name(self, cname, el = None):
        el = el if el else self.browser

        try:
            return el.find_elements_by_class_name(cname)
        except NoSuchElementException:
            return None

    # FINDER (element by class name)

    def find_element(self, class_name, el = None):
        el = el if el else self.browser

        element = el.find_element_by_class_name(class_name)
        return element

    def try_find_element(self, class_name, el = None):
        try:
            return self.find_element(class_name, el)
        except NoSuchElementException:
            pass
    
    def wait_to_find_element_by_class_name(self, class_name, el = None):
        return self.generic_wait_to_find_element(self.try_find_element, class_name, el)
    
    # FINDER (elementS by class name)

    def find_elements(self, class_name, el = None):
        el = el if el else self.browser

        element = el.find_element_by_class_name(class_name)
        return element

    def try_find_elements(self, class_name, el = None):
        try:
            return self.find_elements(class_name, el)
        except NoSuchElementException:
            pass
    
    def wait_to_find_elements_by_class_name(self, class_name, el = None):
        return self.generic_wait_to_find_element(self.try_find_elements, class_name, el)

    # FINDER (element by id)

    def find_element_by_id(self, id_param, el = None):
        el = el if el else self.browser

        element = el.find_element_by_id(id_param)
        return element

    def try_find_element_by_id(self, id_param, el = None):
        try:
            return self.find_element_by_id(id_param, el)
        except NoSuchElementException:
            pass
    
    def wait_to_find_element_by_id(self, id_param, el = None):
        return self.generic_wait_to_find_element(self.try_find_element_by_id, id_param, el)

    # GENERIC

    def generic_wait_to_find_element(self, function, param, el):
        sleep_time = self.SLEEP_TIME
        for attempts in range(self.MAX_LOADING_ATTEMPTS):
            print("Attempt n°" + str(attempts + 1) + ". \nCurrent page: " + self.browser.current_url + " element searched: " + param)

            if attempts >= int(self.MAX_LOADING_ATTEMPTS) / 2:
                self.refresh_page()

            time.sleep(sleep_time)
            element = function(param, el)
            if element is not None:
                time.sleep(sleep_time)
                return element
        
        self.save_screenshot("screenshot_error.png")
        return None