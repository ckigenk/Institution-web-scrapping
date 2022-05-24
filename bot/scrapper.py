from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import csv
from .constants import PATH, URL

class Staff:
    def __init__(self):
        driver = webdriver.Chrome(service=Service(PATH))
        self.driver=driver
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        super(Staff, self).__init__()

    def land_site_page(self):
        self.driver.get(URL)
    
    def get_staff_data(self, profile):
        title = profile.find_element(By.XPATH, './/span[contains(@class,"lastname")]').text
        lastname = profile.find_element(By.XPATH, './/span[contains(@class,"lastname")]/following-sibling::span').text
        firstname = profile.find_element(By.XPATH, './/span[contains(@class,"firstname")]').text
        country = profile.find_element(By.XPATH, './/span[contains(@class,"governing_country")]').text
        short_bio = profile.find_element(By.XPATH, './/div[contains(@class,"profile_body")]/child::div[2]').text
        image_url=profile.find_element(By.XPATH, './/img').get_attribute('src')
        profile.find_element(By.XPATH, './/a').click()
        sleep(2)
        try:
          full_bio = self.driver.find_element(By.XPATH, '//div[@class="prof_body"]').text.strip('\n')
        except:
          full_bio = 'Not found'
        try:
          email = self.driver.find_element(By.XPATH, './/a[contains(@href,"mailto")]').get_attribute('href').strip('mailto:')
        except:
          email='Not found'
        sleep(1)
        self.driver.back()
        sleep(2)
        self.driver.execute_script("window.scrollBy(0, 125)")
        return (title, lastname, firstname, country, email, short_bio,image_url,full_bio )

    def scrape_data(self):
        all_data=[]
        self.all_data = all_data
        while True:
            print("Scrapping...")
            profiles = self.driver.find_elements(By.XPATH, '//div[contains(@class,"general_profile")]')
            for profile in profiles:
                data=self.get_staff_data(profile)
                if bool(data):
                    all_data.append(data)
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            try:
                self.driver.find_element(By.XPATH, '//a[@title="Go to next page"]').click()
                sleep(2)
                self.driver.execute_script("scrollBy(0,-document.body.scrollHeight)")
            except:
                break
        self.driver.close()
        print("Scrapping complete")
        return all_data

    def save_data(self, output_file_path='icipe_staff.csv'):
        with open(f"{output_file_path}", 'w', encoding='utf-8', newline='') as f:
            writer=csv.writer(f)
            header=['Title', 'Lastname', 'Firstname', 'Country', 'Email', 'Shortbio', 'Image_url', 'Fullbio']
            writer.writerow(header)
            writer.writerows(self.all_data)