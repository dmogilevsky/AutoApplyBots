from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import undetected_chromedriver as uc
import info


class IndeedBot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-notifications")
        initial_path = info.chromeProfilePath[0:info.chromeProfilePath.rfind("/")]
        profile_dir = info.chromeProfilePath[info.chromeProfilePath.rfind("/") + 1:]
        options.add_argument('--user-data-dir=' + initial_path)
        options.add_argument('--profile-directory=' + profile_dir)
        # options.add_experimental_option('useAutomationExtension', False)
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])

        self.driver = uc.Chrome(options=options)
        self.driver.implicitly_wait(1) # We will manage wait between actions ourselves
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
            'https://www.indeed.com/jobs?q=software+engineer&sc=0kf%3Aattr%28DSQF7%29occ%28EG6MP%29%3B&vjk=ae03555c3844ff70')

        # Apply to every single job in the search
        while True:
            self.apply_to_all_jobs_on_page()
            self.click_element_and_wait(
                By.CSS_SELECTOR,
                '#jobsearch-JapanPage > div > div > div.css-hyhnne.e37uo190 > div.jobsearch-LeftPane > nav > '
                'div:last-child > a'
            )

    # Go through the jobList and open in new tab
    def apply_to_all_jobs_on_page(self):
        driver = self.driver
        main = driver.window_handles[0]
        # get list of jobs, used to be only jobs with apply by indeed only
        # but turns out many jobs without the apply by indeed icon can still be applied to through indeed
        job_list = driver.find_elements(By.CLASS_NAME, 'jobTitle')
        for job in job_list:
            job.click()
            sleep(1)

            job_title = driver.find_element(By.CSS_SELECTOR,
                                            '.jobsearch-JobInfoHeader-title > span:nth-child(1)').text

            # Make sure nothing in the job title is one of the blacklisted words
            if any(kw.lower() in job_title.lower() for kw in info.blacklisted_words):
                print("Blacklisted word found in " + job_title + ", skipping")
                continue

            # The applyButtonLinkContainer is an apply button that leads to an external company site.
            # Skip these and only attempt to apply to jobs within linked
            if self.element_exists(By.ID, 'applyButtonLinkContainer'):
                print("Skipping third party job application: " + job_title)
                continue

            if self.element_exists(By.CLASS_NAME, 'jobsearch-IndeedApplyButton--disabled'):
                print("Already applied to " + job_title)
                continue

            print("Applying to " + job_title)
            self.click_element_and_wait(By.ID, 'indeedApplyButton', 1)

            driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])

            while not self.element_exists(By.ID, 'resume-display-buttonHeader'):
                pass

            sleep(0.5)

            self.click_element_and_wait(By.ID, 'resume-display-buttonHeader', 0.5)

            keep_tab_open = False
            # Continue skipping through the indeed apply pages until we either can't
            # or we have applied for the job
            previous_url = driver.current_url
            while True:
                try:
                    if 'post-apply' in previous_url or 'applied' in previous_url or 'postresumeapply' in previous_url:
                        print("Already applied")
                        break
                    else:
                        self.click_element_and_wait(By.CLASS_NAME, 'ia-continueButton')

                    if previous_url == driver.current_url:
                        if not info.wait_for_user_input:
                            print("Couldn't apply to this posting, needed more info")
                            if info.keep_failed_applications_open: keep_tab_open = True
                            break
                        print("Need user input to continue")
                        while previous_url == driver.current_url:
                            if 'post-apply' in previous_url or 'applied' in previous_url:
                                break
                    previous_url = driver.current_url
                except Exception as e:
                    print(e)
                    break

            sleep(1)
            if not keep_tab_open:
                driver.close()
            driver.switch_to.window(main)
            sleep(1)

    # Click element normally, if an error occurs, try clicking its position instead
    def click_element_and_wait(self, by, value, wait=3.0):
        element = self.driver.find_element(by, value)
        try:
            element.click()
        except Exception:
            actions = webdriver.common.action_chains.ActionChains(self.driver)
            actions.move_to_element_with_offset(element, 1, 1).click().perform()

        sleep(wait)

    def element_exists(self, by, value):
        return not (len(self.driver.find_elements(by, value)) == 0)

IndeedBot()
