import random

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from urllib.parse import quote
from re import fullmatch
import time , os


class Connect:
    def __init__(self , host_url , login_email , login_password):
        self.host_url = host_url.rsplit('/' , (host_url.count('/') - 2))[0]
        chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        chrome_options = Options()
        options = [
            "--headless" ,
            "--disable-gpu" ,
            "--window-size=1920,1200" ,
            "--ignore-certificate-errors" ,
            "--disable-extensions" ,
            "--no-sandbox" ,
            "--disable-dev-shm-usage"
        ]
        for option in options:
            chrome_options.add_argument(option)

        driver = webdriver.Chrome(service=chrome_service , options=chrome_options)
        wait_30 = WebDriverWait(driver , 30)
        driver.get(host_url)
        time.sleep(5)

        try:
            if wait_30.until(EC.presence_of_element_located(
                    (By.XPATH , '//*[@id="projects"]/div/div/h1'))).text == 'Sign in to ActiveCollab':
                self.driver = driver
                driver.find_element(By.XPATH , value="//input[@placeholder='Email']").send_keys(login_email)
                driver.find_element(By.XPATH , value="//input[@placeholder='Password']").send_keys(login_password)
                driver.find_element(By.XPATH , value="//button[@type='submit']").click()
                time.sleep(3)
        except Exception as e:
            print(e)
            driver.close()
            driver.quit()
            print('Something went wrong. Kindly check host_url,login_email or login_password')

    def list_projects(self):
        """
        :return: list of all projects you have with their project number
        """
        project_list = {}
        self.driver.get(f'{self.host_url}/projects')
        time.sleep(2)
        all_projects = self.driver.find_elements(By.CLASS_NAME , value="list-item")
        for i in all_projects:
            project_name = i.find_element(By.CLASS_NAME , value="entity-property-name").text
            project_id = project_name.split(':')[0].split('#')[1]
            # print(f" Project Id: {project_id}  Project Name: {project_name.split(':')[1]} ")
            project_list[project_id] = project_name.split(':')[1]
        return project_list

    def list_users_in_project(self , project_id):
        """
        :param project_id: Project id you want to search user from
        :return: List of users in passed project id
        """
        users_list_in_project = {}
        self.driver.get(f'{self.host_url}/projects/{project_id}/members')
        time.sleep(2)
        all_users = self.driver.find_elements(By.CLASS_NAME,value="people_list_name")
        j = 1
        for i in all_users:
            users_list_in_project[j] = i.text
            j = j+1
        return users_list_in_project

