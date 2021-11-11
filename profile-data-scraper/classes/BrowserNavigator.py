import time, configparser, csv, random
from selenium import webdriver
from classes.Helpers import Helpers
from classes.Finders import Finders
from classes.ProfileScraper import ProfileScraper
from selenium.common.exceptions import NoSuchElementException

config = configparser.ConfigParser()
config.read('config.ini')

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class BrowserNavigator:

    # RANDOMIZERs

    def randomize_to_be_done(self):
        return random.choice([0, 1, 1, 1])

    def behaviour_randomizer(self):
        random.choice([
            self.fake_linkedin_feed_scoll_behaviour, self.fake_linkedin_sales_feed_scroll_behaviour, 
            self.fake_linkedin_feed_scoll_behaviour, self.fake_linkedin_sales_feed_scroll_behaviour, 
            self.fake_google_search_and_scroll_behaviour, self.fake_wikipedia_behaviour,
            self.fake_random_choise_normal_scrcoll
        ])()

    def handle_random_behaviour(self):
        if self.randomize_to_be_done() == 1:
            self.behaviour_randomizer()
            self.Helpers.wait_default_time()

    # FAKERS & LOGIN

    def fake_google_search_and_scroll_behaviour(self):
        self.Helpers.fake_google_search_and_scroll_behaviour()

    def fake_linkedin_feed_scoll_behaviour(self):
        self.Helpers.fake_linkedin_feed_scoll_behaviour()

    def fake_linkedin_sales_feed_scroll_behaviour(self):
        self.Helpers.fake_linkedin_sales_feed_scroll_behaviour()

    def fake_wikipedia_behaviour(self):
        self.Helpers.fake_wikipedia_behaviour()

    def fake_random_choise_normal_scrcoll(self):
        self.Helpers.fake_random_choise_normal_scrcoll()

    def log_in(self):
        self.Helpers.log_in()

    # MAIN

    def scrape_profiles_info(self):
        for csv_name in self.CSV_TO_IMPORT:
            df = self.ProfileScraper.import_csv(csv_name)

            dfc = df.copy()
            dfc = self.ProfileScraper.initialize_empty_columns(dfc)

            self.Helpers.zoom_out_browser()

            try:
                for index, row in df.iterrows():
                    print('Fetching user number: ' + str(index) + '\n')
                   
                    if (index != 0 and index % 20 == 0):
                        # Closing browser and deleting classes
                        self.close_current_browser()
                        self.delete_current_classes()

                        # Reinitializing browser and classes
                        self.initialize_browser_and_script_variable()
                        self.log_in()

                    url = row['Url']
                    self.Helpers.go_to_url(url)
                    self.Helpers.wait_two_seconds()

                    # Logs in if needed
                    new_log_happened = self.Helpers.check_if_login_is_required()
                    if new_log_happened is True:
                        self.Helpers.go_to_url(url)
                        self.Helpers.wait_two_seconds()
                    
                    self.Helpers.zoom_out_browser()
                    self.ProfileScraper.scrape_profile(dfc, index)

                    # Randomizes behaviour before next profile
                    self.handle_random_behaviour()
            except:
                print('ERRORE GENERICO CATTURATO: Salvataggio del csv di cio che è stato recuperato fino ad ora.' + '\n')
            finally:
                print('Saving elaborated csv. CSV_NAME: ' + csv_name  + '\n')
                self.ProfileScraper.save_csv(dfc, csv_name)

    def script_entry_point(self):
        # Script scraping 
        self.initialize_browser_and_script_variable()
        self.log_in()
        self.scrape_profiles_info()


        # TEST reCaptcha solver
        
        # time.sleep(5)
        # el = self.Finders.safe_find_element_by_id('nocaptcha')
        # if el is not None:
        #     button = self.browser.find_element_by_class_name('recaptcha-checkbox')
        #     self.browser.execute_script("arguments[0].click();", button)

        # time.sleep(5)

    # Variable Initialization 

    def return_new_browser(self):
        print('Opening new browser')

        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        options.add_argument("disable-web-security")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        browser = webdriver.Chrome(options=options, executable_path=r'./driver/chromedriver')
        
        return browser

    def close_current_browser(self):
        print("Closing current browser...")
        self.browser.close()

    def delete_current_classes(self):
        print('Deleting current classes instances')
        self.Helpers.log_out()
        del self.Helpers
        del self.Finders
        del self.ProfileScraper

    def initialize_browser_and_script_variable(self):
        self.browser = self.return_new_browser()

        # App config
        self.SLEEP_TIME = int(config['CONFIG']['SLEEP_TIME'])
        self.MAX_LOADING_ATTEMPTS = int(config['CONFIG']['MAX_LOADING_ATTEMPTS'])
        self.CSV_TO_IMPORT = str(config['IMPORT']['CSV_NAMES'])
        self.CSV_TO_IMPORT = self.CSV_TO_IMPORT.split(',')
        
        # Classes
        self.Helpers = Helpers(self.browser)
        self.Finders = Finders(self.browser)
        self.ProfileScraper = ProfileScraper(self.browser)

    # INIT

    def __init__(self):
        print('Browser Navigator init')