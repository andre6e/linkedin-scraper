import time
from selenium import webdriver
from classes.BrowserNavigator import BrowserNavigator

def main():
    page = BrowserNavigator()
    page.script_entry_point()

if __name__ == '__main__':
    main()
