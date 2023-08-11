from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import undetected_chromedriver as uc


class IndeedBot:
    def __init__(self):

        # Create headless chrome
        # Create webdriver, add user data to persist login and not have to relog
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-notifications")
        # options.add_experimental_option('useAutomationExtension', False)
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # create a new Chrome session
        self.driver = uc.Chrome(options=options)

        # open indeed
        self.driver.get('https://secure.indeed.com/account/login')

        # # Login via google, not working for now so do it manually
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
        actions = webdriver.common.action_chains.ActionChains(self.driver)
        # Go through the jobList and open in new tab
        for job in jobList:
            actions.move_to_element_with_offset(job, 1, 1).click().perform()

            sleep(1)

            self.click_element(By.ID, 'indeedApplyButton')

            self.driver.switch_to.window(self.driver.window_handles[1])
            sleep(5)

            self.handle_cloudflare_auth()

            self.click_element(By.ID, 'resume-display-buttonHeader')

            # Continue skipping through the indeed apply pages until we either can't
            # or we have applied for the job
            previous_url = self.driver.current_url
            while 'post-apply' not in previous_url:
                self.click_element(By.CLASS_NAME, 'ia-continueButton')
                if previous_url == self.driver.current_url:
                    print("Need user input to continue")
                    while (previous_url == self.driver.current_url):
                        pass
                previous_url = self.driver.current_url

            sleep(2)
            self.driver.close()
            self.driver.switch_to.window(main)
            sleep(3)
            self.handle_cloudflare_auth()

    def click_element(self, by, value):
        self.handle_cloudflare_auth()
        try:
            self.driver.find_element(by, value).click()
        except Exception as e:
            print("Failed to click element, printing exception")
            print(e)
            sleep(100)
        sleep(1)
        self.handle_cloudflare_auth()

    def handle_cloudflare_auth(self):
        if 'auth' in self.driver.current_url:
            self.driver.find_element(By.ID, 'cf-stage').click()
            sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[len(self.driver.window_handles)-1])
            sleep(2)


IndeedBot()
