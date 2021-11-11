import time
from selenium import webdriver
from classes.BrowserNavigator import BrowserNavigator

def main():
    # Browser Driver
    browser = webdriver.Chrome("./driver/chromedriver")

    page = BrowserNavigator(browser)
    page.load_multi_configurations()
    page.log_in()
    page.wait_default_time()
    page.fetch_users_url()

    page.save_screenshot("screenshot_closing.png")
    print("Closing browser...")
    browser.close()


if __name__ == '__main__':
    main()
