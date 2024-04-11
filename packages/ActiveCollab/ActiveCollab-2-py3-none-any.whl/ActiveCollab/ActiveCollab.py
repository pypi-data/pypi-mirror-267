import itertools
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import quote
from re import fullmatch
import time , os


class Connect:
    def __init__(self , host_url , login_email , login_password):
        self.host_url = host_url.rsplit('/' , (host_url.count('/') - 2))[0]
        chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        chrome_options = Options()
        options = [
            # "--headless" ,
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
        self.wait_30 = WebDriverWait(driver , 30)
        self.wait_10 = WebDriverWait(driver , 10)
        self.wait_5 = WebDriverWait(driver , 5)
        driver.get(host_url)
        time.sleep(5)

        try:
            if self.wait_10.until(EC.presence_of_element_located(
                    (By.XPATH , '//*[@id="projects"]/div/div/h1'))).text == 'Sign in to ActiveCollab':
                self.driver = driver
                driver.find_element(By.XPATH , value="//input[@placeholder='Email']").send_keys(login_email)
                driver.find_element(By.XPATH , value="//input[@placeholder='Password']").send_keys(login_password)
                driver.find_element(By.XPATH , value="//button[@type='submit']").click()
                time.sleep(3)
            try:

                if driver.find_element(By.XPATH,value='//*[@id="main_message_inner"]/span').text:
                    # driver.close()
                    # driver.quit()
                    print(driver.find_element(By.XPATH,value='//*[@id="main_message_inner"]/span').text)
            except:
                pass

        except Exception as e:
            print('Something went wrong.')
            print(e)
            driver.close()
            driver.quit()

    def list_projects(self):
        """
        :return: list of all projects you have with their project number
        """
        self.driver.get(f'{self.host_url}/projects')
        try:
            if self.wait_5.until(EC.presence_of_element_located(
                    (By.XPATH , '//*[@id="projects"]/div/div/h1'))).text == 'Sign in to ActiveCollab':
                print('You are not logged in')
        except:
            pass
        try:
            if self.wait_5.until(EC.presence_of_element_located(
                    (By.XPATH , '//*[@id="main_message_inner"]/span'))).text:
                print(self.driver.find_element(By.XPATH,value='//*[@id="main_message_inner"]/span').text)
        except:
            pass
        project_list = {}
        time.sleep(2)
        all_projects = self.driver.find_elements(By.CLASS_NAME , value="list-item")
        for i in all_projects:
            project_name = i.find_element(By.CLASS_NAME , value="entity-property-name").text
            project_id = project_name.split(':')[0].split('#')[1]
            # print(f" Project Id: {project_id}  Project Name: {project_name.split(':')[1]} ")
            project_list[project_id] = project_name.split(':')[1]
        return project_list

    def list_users(self):
        """
        :return: list of all users
        """
        self.driver.get(f'{self.host_url}/people')
        try:
            if self.wait_5.until(EC.presence_of_element_located(
                    (By.XPATH , '//*[@id="projects"]/div/div/h1'))).text == 'Sign in to ActiveCollab':
                print('You are not logged in')
        except:
            pass
        try:
            if self.wait_5.until(EC.presence_of_element_located(
                    (By.XPATH , '//*[@id="main_message_inner"]/span'))).text:
                print(self.driver.find_element(By.XPATH,value='//*[@id="main_message_inner"]/span').text)
        except:
            pass
        user_list = []
        time.sleep(2)
        all_users = self.driver.find_elements(By.CLASS_NAME , value="col_name")
        all_users_email = self.driver.find_elements(By.CLASS_NAME , value="col_email")
        for (i,j) in itertools.zip_longest(all_users,all_users_email):
            user_id = i.find_element(By.CSS_SELECTOR,value="a").get_attribute('href').rsplit('/',1)[1]
            user_name = i.text
            user_email = j.text
            user_list.append([user_id,user_name,user_email])
        return user_list

    def list_users_in_project(self , project_id):
        """
        :param project_id: Project id you want to search user from
        :return: List of users in passed project id
        """
        self.driver.get(f'{self.host_url}/projects/{project_id}/members')
        try:
            if self.wait_5.until(EC.presence_of_element_located(
                    (By.XPATH , '//*[@id="projects"]/div/div/h1'))).text == 'Sign in to ActiveCollab':
                print('You are not logged in')
        except:
            pass
        try:
            if self.wait_5.until(EC.presence_of_element_located(
                    (By.XPATH , '//*[@id="main_message_inner"]/span'))).text:
                print(self.driver.find_element(By.XPATH,value='//*[@id="main_message_inner"]/span').text)
        except:
            pass
        users_list_in_project = {}
        time.sleep(2)
        all_users = self.driver.find_elements(By.CLASS_NAME,value="people_list_name")
        j = 1
        for i in all_users:
            users_list_in_project[j] = i.text
            j = j+1
        return users_list_in_project

    def add_user_in_project(self,project_id,user_name_or_user_email):
        """

        :param project_id: Project id in which you want to add the user
        :param user_name_or_user_email: User name or email that you want to add, Make sure to use full name to avoid
        :return: User added OR something went wrong
        """
        self.driver.get(f'{self.host_url}/projects/{project_id}/members')
        try:
            if self.wait_5.until(EC.presence_of_element_located(
                    (By.XPATH , '//*[@id="projects"]/div/div/h1'))).text == 'Sign in to ActiveCollab':
                print('You are not logged in')
        except:
            pass
        try:
            if self.wait_5.until(EC.presence_of_element_located(
                    (By.XPATH , '//*[@id="main_message_inner"]/span'))).text:
                print(self.driver.find_element(By.XPATH,value='//*[@id="main_message_inner"]/span').text)
        except:
            pass
        current_member_count = self.driver.find_element(By.XPATH,value='//*[@id="project_people"]/div/div[2]/div/div/div/div[1]/h3').text.split(' (')[1].split(')')[0]
        print(current_member_count)
        try:
            input_field = self.driver.find_element(By.XPATH,value='//*[@id="project_people"]/div/div[2]/div/div/div/div[1]/form/div/span/span/div/div[1]/input')
            input_field.click()
            input_field.send_keys(user_name_or_user_email.strip())
            input_field.send_keys(Keys.RETURN)
            invite_button = self.driver.find_element(By.XPATH, value='//*[@id="project_people"]/div/div[2]/div/div/div/div[1]/form/div/button')
            invite_button.click()
            updated_member_count = self.driver.find_element(By.XPATH ,value='//*[@id="project_people"]/div/div[2]/div/div/div/div[1]/h3').text.split(' (')[1].split(')')[0]
            print(updated_member_count)
            if current_member_count<updated_member_count:
                return print(f"User: {user_name_or_user_email} added in project {project_id}")
        except Exception as e:
            print('Something went wrong.')
            print(e)
            self.driver.close()
            self.driver.quit()





