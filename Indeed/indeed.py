from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import undetected_chromedriver as uc
import info


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
        initialPath = info.chromeProfilePath[0:info.chromeProfilePath.rfind("/")]
        profileDir = info.chromeProfilePath[info.chromeProfilePath.rfind("/") + 1:]
        options.add_argument('--user-data-dir=' + initialPath)
        options.add_argument('--profile-directory=' + profileDir)
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
        # self.driver.switch_to.window(window_before)
        print('Waiting for user login')
        while 'auth' in self.driver.current_url:
            pass
        print('User has logged in')

        # Go to our specific job search
        self.driver.get(
            'https://www.indeed.com/jobs?q=software+engineer&sc=0kf%3Aattr%28DSQF7%29%3B&vjk=e14527580da91c17')

        # Apply to every single job in the search
        while True:
            self.apply_to_all_jobs_on_page()
            self.click_element(By.CSS_SELECTOR, '#jobsearch-JapanPage > div > div > div.css-hyhnne.e37uo190 > div.jobsearch-LeftPane > nav > div:last-child > a')


    # Go through the jobList and open in new tab
    def apply_to_all_jobs_on_page(self):
        # get list of jobs with apply by indeed only
        job_list = self.driver.find_elements(By.CLASS_NAME, 'iaIcon')
        main = self.driver.window_handles[0]
        for job in job_list:
            self.click_element_using_position(job)
            job_title = self.driver.find_element(By.CSS_SELECTOR, '.jobsearch-JobInfoHeader-title > span:nth-child(1)').text
            already_applied = False
            try:
                self.driver.find_element(By.CLASS_NAME, 'jobsearch-IndeedApplyButton--disabled')
                already_applied = True
            except Exception:
                pass

            if already_applied:
                continue

            print("Applying to " + job_title)
            self.click_element(By.ID, 'indeedApplyButton')

            self.driver.switch_to.window(self.driver.window_handles[1])
            application_page_loaded = False
            while not application_page_loaded:
                try:
                    self.driver.find_element(By.ID, 'resume-display-buttonHeader')
                    application_page_loaded = True
                except Exception:
                    pass

            sleep(0.5)

            self.click_element(By.ID, 'resume-display-buttonHeader')

            # Continue skipping through the indeed apply pages until we either can't
            # or we have applied for the job
            previous_url = self.driver.current_url
            while 'post-apply' not in previous_url or 'applied' not in previous_url or 'postresumeapply' not in previous_url:
                try:
                    if 'work-experience' in self.driver.current_url:
                        self.click_element_using_position(self.driver.find_element(By.CLASS_NAME, 'ia-continueButton'))
                    else:
                        self.click_element(By.CLASS_NAME, 'ia-continueButton')
                    if previous_url == self.driver.current_url:
                        if not info.wait_for_user_input:
                            break
                        print("Need user input to continue")
                        while previous_url == self.driver.current_url:
                            if 'post-apply' in previous_url or 'applied' in previous_url:
                                break
                    sleep(1)
                    previous_url = self.driver.current_url
                except Exception as e:
                    print(e)
                    break

            self.driver.close()
            self.driver.switch_to.window(main)
            sleep(3)

    def click_element(self, by, value):
        self.driver.find_element(by, value).click()
        sleep(1)

    def click_element_using_position(self, element):
        actions = webdriver.common.action_chains.ActionChains(self.driver)
        actions.move_to_element_with_offset(element, 1, 1).click().perform()
        sleep(1)


IndeedBot()
