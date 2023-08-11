from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep

import info


class IndeedBot:
    def __init__(self):

        # Create headless chrome
        # Create webdriver, add user data to persist login and not have to relog
        options = Options()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-notifications")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # create a new Chrome session
        self.driver = webdriver.Chrome(service=Service(), options=options)

        # open indeed
        self.driver.get('https://secure.indeed.com/account/login')

        # # Login via google
        # self.driver.find_element(By.ID, 'login-google-button').click()
        # window_before = self.driver.window_handles[0]
        # window_after = self.driver.window_handles[1]
        # self.driver.switch_to.window(window_after)
        # sleep(2)
        #
        # emailEntry = self.driver.find_element(By.ID, 'identifierId')
        # emailEntry.send_keys(info.email)
        # emailEntry.send_keys(Keys.ENTER)
        #
        # sleep(2)
        # passwordEntry = self.driver.find_element(By.NAME, 'Passwd')
        # passwordEntry.send_keys(info.password)
        # passwordEntry.submit()

        print('Waiting for user login')
        while 'auth' in self.driver.current_url:
            pass
        print('User has logged in')

        # Go to our specific job search
        self.driver.get(
            'https://www.indeed.com/jobs?q=software+engineer&sc=0kf%3Aattr%28DSQF7%29%3B&vjk=e14527580da91c17')

        # get list of jobs with apply by indeed only
        jobList = self.driver.find_elements(By.CLASS_NAME, 'iaIcon')

        # initialize main page
        main = self.driver.window_handles[0]

        # Go through the jobList and open in new tab
        for job in jobList:
            job.click()

            # get new tab and switch to it
            jobWin = self.driver.window_handles[1]
            self.driver.switch_to.window(jobWin)
            title = self.driver.title
            print('Applying job ' + title)

            # Click on Apply Now
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'jobsearch-IndeedApplyButton-contentWrapper'))).click()

            # Locate the parent iframe and switch to it
            parentIframe = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id,'modal-iframe')]")))
            self.driver.switch_to.frame(parentIframe)

            # Locate the parent iframe and switch to it
            childIframe = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src,'resumeapply')]")))
            self.driver.switch_to.frame(childIframe)
            conButton = self.driver.find_element_by_xpath('//*[@id="form-action-continue"]')
            # Click on continue button if there any             
            if conButton.is_enabled():
                self.driver.implicitly_wait(30)
                conButton.click()
                if conButton.is_enabled():
                    self.driver.close()
                    self.driver.switch_to.window(main)
                else:
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="form-action-submit"]'))).click()
                    self.driver.close()
                    self.driver.switch_to.window(main)

                    # If no button close the window and switch to main window
            # WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="form-action-submit"]'))).click()
            # if self.driver.find_element_by_xpath('//*[@id="ia-container"]/div/div[2]/a'):
            else:
                self.driver.close()
                self.driver.switch_to.window(main)


IndeedBot()
