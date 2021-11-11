import configparser, csv, time, random, json
from datetime import datetime
from classes.Finders import Finders
from selenium.webdriver.common.keys import Keys

config = configparser.ConfigParser()
config.read('config.ini')

LOGIN_URL = "https://www.linkedin.com/uas/login"
LINKEDIN_SALES_LOGIN = 'https://www.linkedin.com/sales/login'

WEBSITE_URLS_LIST_NORMAL_BEHAVIOUR = [
    'https://www.amazon.it/', 'https://news.google.it/', 
    'https://www.open.online/', 'https://www.freecodecamp.org/', 
    'https://www.unipi.it/', 'http://didawiki.di.unipi.it/'
]

VISUALLY_HIDDEN_NAME_CNAME = 'visually-hidden'

class Helpers:

    # INIT

    def __init__(self, browser):
        print('Initializing Helpers class')
        self.browser = browser
        self.Finders = Finders(browser)

        # App config
        self.SLEEP_TIME = int(config['CONFIG']['SLEEP_TIME'])
        self.MAX_LOADING_ATTEMPTS = int(config['CONFIG']['MAX_LOADING_ATTEMPTS'])
        self.SCROLL_SECONDS_SLOW = int(config['CONFIG']['SCROLL_SECONDS_SLOW'])

        # App variable
        self.load_words_from_json()

    # NAVIGATORS

    def go_to_url(self, url):
        print('Going to url ' + str(url))
        self.browser.get(url)
        self.wait_and_zoom_out()

    # ZOOMERS

    def zoom_out_browser(self):
        self.browser.execute_script("document.body.style.zoom = '70%'")

    # WAITERS

    def wait_default_time(self):
        time.sleep(self.SLEEP_TIME)

    def wait_two_seconds(self):
        time.sleep(2)

    def wait_three_seconds(self):
        time.sleep(3)

    def wait_five_seconds(self):
        time.sleep(5)

    def wait_ten_seconds(self):
        time.sleep(10)

    def wait_given_time(self, to_sleep):
        time.sleep(to_sleep)

    def wait_and_zoom_out(self):
        self.zoom_out_browser()
        self.wait_default_time()

    # SCROLLERS

    def scroll_to_element_height(self, elem):
        # Distanza da top pagina
        elem_scroll_height = elem.get_attribute("offsetTop")
        # Altezza elemento
        elem_offset_height = elem.get_attribute("offsetHeight")
        to_scroll = str(int(elem_scroll_height) + int(elem_offset_height) - (int(elem_offset_height) / 2) )
        print("scrolling to %s element height" % (to_scroll))
        self.browser.execute_script("window.scrollTo(0, %s);" % (to_scroll))

    def scroll_page_to_end(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_page_to_height(self, to_scroll):
        self.browser.execute_script("window.scrollTo(0, %s);" % (to_scroll))

    def slow_scroll_page_to_end(self):
        page_height = self.get_page_scroll_height()
        offset_height = int(round(page_height / self.SCROLL_SECONDS_SLOW))

        for i in range(1, self.SCROLL_SECONDS_SLOW):
            self.wait_default_time()
            self.scroll_page_to_height(offset_height)
            offset_height += offset_height

    def slow_scroll_back_up(self):
        page_height = self.get_page_scroll_height()
        offset_height = int(round(page_height / self.SCROLL_SECONDS_SLOW))
        to_scroll = page_height - offset_height

        for i in range(1, self.SCROLL_SECONDS_SLOW):
            self.wait_default_time()
            self.scroll_page_to_height(to_scroll)
            to_scroll -= offset_height
   
    # HELPERS

    def load_words_from_json(self):
        with open('words.json', 'r') as f:
            self.WORDS_LIST = json.load(f)

    def get_random_word_from_list(self):
        return random.choice(self.WORDS_LIST)

    def get_page_scroll_height(self):
        return self.browser.execute_script("return document.body.scrollHeight;")

    def is_profile_blocked(self, el):
        return 1 if el.tag_name == 'span' else 0

    def get_string_without_hidden_text(self, el):
        el_text = el.text
        hidden = self.Finders.safe_find_element_by_class_name(VISUALLY_HIDDEN_NAME_CNAME, el)
                
        if hidden is not None:
            el_text = el_text.replace(hidden.text, '').strip()
            
        return el_text

    def check_if_login_is_required(self):
        # potrebbe capitare di non essere loggati (probabilmente perche linkedin fa scadere la sessione), in quel caso si rifa il login. Check fatto in base all current url
        current_url = self.browser.current_url

        if current_url == LINKEDIN_SALES_LOGIN or current_url == LOGIN_URL or self.IS_LOGGED == False:
            print('LOGIN REQUIRED: Redirecting to login...')
            self.sales_log_in()
            self.wait_two_seconds()
            return True
        else:
            return False

    # LOGIN & LOGOUT

    def log_in(self):
        print('Logging in...')
        self.browser.get(LOGIN_URL)
        self.wait_default_time()

        # Login
        username = config['LOGIN']['EMAIL']
        password = config['LOGIN']['PASSWORD']

        elementID = self.browser.find_element_by_id('username')
        elementID.send_keys(username)

        elementID = self.browser.find_element_by_id('password')
        elementID.send_keys(password)

        elementID.submit()

        while self.browser.current_url == LOGIN_URL:
            time.sleep(3)

        self.IS_LOGGED = True
        print("Logged")

    def sales_log_in(self):
        print('Logging in...')
        self.browser.get(LINKEDIN_SALES_LOGIN)
        self.wait_default_time()

        # Login
        username = config['LOGIN']['EMAIL']
        password = config['LOGIN']['PASSWORD']

        elementID = self.browser.find_element_by_id('username')
        elementID.send_keys(username)

        elementID = self.browser.find_element_by_id('password')
        elementID.send_keys(password)

        elementID.submit()

        while self.browser.current_url == LOGIN_URL:
            time.sleep(3)

        self.IS_LOGGED = True
        print("Logged")

    def log_out(self):
        self.IS_LOGGED = False

    # FAKE BEHAVIOUR

    def fake_google_search_and_scroll_behaviour(self):
        random_word = self.get_random_word_from_list()

        self.browser.get('https://www.google.com/')
        self.wait_default_time()

        q = self.browser.find_element_by_name('q')
        q.send_keys(random_word)
        q.send_keys(Keys.RETURN)

        self.wait_default_time()
        self.slow_scroll_page_to_end()
        self.slow_scroll_back_up()

    def fake_wikipedia_behaviour(self):
        random_word = self.get_random_word_from_list()

        self.browser.get('https://www.wikipedia.org/')
        self.wait_and_zoom_out()

        q = self.browser.find_element_by_name('search')
        q.send_keys(random_word)
        q.send_keys(Keys.RETURN)

        self.wait_default_time()
        self.slow_scroll_page_to_end()
        self.slow_scroll_back_up()

    def fake_linkedin_feed_scoll_behaviour(self):
        if self.IS_LOGGED is False:
            self.log_in()
        
        self.browser.get('https://www.linkedin.com/feed/')
        self.wait_default_time()

        self.slow_scroll_page_to_end()
        self.slow_scroll_back_up()

    def fake_linkedin_sales_feed_scroll_behaviour(self):
        if self.IS_LOGGED is False:
            self.log_in()
            
        self.browser.get('https://www.linkedin.com/sales/homepage')
        self.wait_and_zoom_out()
        
        self.slow_scroll_page_to_end()
        self.slow_scroll_back_up()

    def fake_random_choise_normal_scrcoll(self):
        url = random.choice(WEBSITE_URLS_LIST_NORMAL_BEHAVIOUR)

        self.browser.get(url)
        self.wait_and_zoom_out()
        
        self.slow_scroll_page_to_end()
        self.slow_scroll_back_up()