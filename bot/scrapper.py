from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
from .constants import PATH, URL

class Tweet:
    def __init__(self):
        driver = webdriver.Chrome(service=Service(PATH))
        self.driver=driver
        self.driver.implicitly_wait(10)
        super(Tweet, self).__init__()