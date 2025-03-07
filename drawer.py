import time
from data import  config
from selenium import webdriver
from time import sleep
import warnings
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from random import randint, sample, choice
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.window import WindowTypes
from seleniumbase import Driver
from seleniumbase import extensions
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import os

# Get the current working directory
current_dir = os.getcwd()

# List all files in the current directory
files = os.listdir(current_dir)

images = "images"
main_folder = os.path.join(current_dir, images)
if not images in files:
    os.mkdir(os.path.join(current_dir, images))


class Setup:
    def __init__(self, ticker="AAPL"):
        self.ticker = ticker
        self.filepath = f"{main_folder}/{ticker}.png"
    def init(self):
        self.driver = Driver(headless=config.production)
        self.driver.set_page_load_timeout(200)
        self.driver.set_window_size(1200, 800)
    def get_image_url(self):
        return self.filepath

    def check_offer_win(self):
        class_close_but = "tv-dialog__close"

        x_button = self.driver.find_elements(By.CLASS_NAME, class_close_but)
        if x_button:
            x_button[0].click()
        time.sleep(2)


    def screenshot(self):
        ticker = self.ticker
        self.filepath = os.path.join(main_folder, f"{ticker}.png")
        self.driver.get('https://www.tradingview.com/chart/?symbol=' + ticker)
        time.sleep(2)
        self.check_offer_win()


        chart = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]")
        screenshot = chart.screenshot_as_png
        image = Image.open(BytesIO(screenshot))
        image.save(self.filepath)
        return self.filepath



    def close_browser(self):
        self.driver.delete_all_cookies()
        self.driver.quit()







