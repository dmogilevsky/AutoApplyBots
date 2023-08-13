import json
import os
from itertools import count
from time import sleep
from Dice import dice_config
from selenium.common import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from common import common_utils, common_config

# see if any data exists for this user
USER_DATA_PATH = os.path.join("Dice/cached_data", f"{dice_config.username}.json")
completed_jobs = []
if not os.path.exists("Dice/cached_data"):
    os.mkdir("Dice/cached_data")
if os.path.exists(USER_DATA_PATH):
    with open(USER_DATA_PATH, "r") as file_handle:
        completed_jobs = json.loads(file_handle.read())
        # dictionary of {job_id: applied boolean}

options = common_utils.chromeBrowserOptions()

driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, dice_config.wait_s)

# log in
driver.get("https://www.dice.com/dashboard/login")
try:
    elem = wait.until(EC.presence_of_element_located((By.ID, "email")))
    elem.send_keys(f"{dice_config.username}\t{dice_config.password}{Keys.RETURN}")
except Exception as e:
    print(e)
    print("Don't need to log in. Continuing.")

for keyword in common_config.keywords:
    # iterate through pages until there are no links
    for page_number in count(1):
        search_url = "https://www.dice.com/jobs?q=" + keyword + "&countryCode=US&radius=30&radiusUnit=mi&page=" + str(page_number) + "&pageSize=100"
        "&filters.easyApply=true&filters.isRemote=true&language=en'"
        driver.get(search_url)
        try:
            search_cards = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.search-card"))
            )
        except Exception:
            print("No more jobs found for keyword " + keyword)
            break
        # wait for ribbons to appear (if there are ribbons)
        try:
            ribbons = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.ribbon-inner"))
            )
        except:
            ...
        job_urls = []
        for card in search_cards:
            link = card.find_element(by=By.CSS_SELECTOR, value="a.card-title-link")
            job_id = link.get_attribute("id")
            if job_id in completed_jobs:
                continue
            try:
                ribbon = card.find_element_by_css_selector("span.ribbon-inner")
                if ribbon.text == "applied":
                    continue
            except:
                ...
            job_urls.append((job_id, link.text, link.get_attribute("href")))

        for job_id, job_text, job_url in job_urls:
            # Job keywords, you want at least one of these to be present
            matching_title = False
            for s in common_config.keywords:
                if s.lower() in job_text.lower():
                    matching_title = True
                    break
            if not matching_title:
                continue

            # Make sure nothing in the job title is one of the blacklisted words
            if any(kw.lower() in job_text.lower() for kw in dice_config.blacklist):
                continue
            print(f"Applying to {job_text}.")
            driver.get(job_url)

            # This is important, if we failed to apply to a previous job, going to a new link will trigger an alert
            # about leaving the old page. The code below handles the alert if it exists
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except NoAlertPresentException:
                pass
            try:
                sleep(4)

                apply_container = driver.find_element(By.CSS_SELECTOR,
                                                      "#__next > div > main > header > div > div > div.order-last.col-span-full.flex.flex-wrap.justify-around.items-start.md\:items-end.md\:col-span-4.md\:justify-end.lg\:col-start-7.lg\:col-span-6 > div.w-full.flex.md\:justify-end > apply-button-wc")
                # Possibly some logic here can be added to ensure the apply_container is valid

                apply_container.click()

                sleep(4)
                driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(2)").click()

                if "submit" not in driver.current_url:
                    print("This job application had more than 2 pages, we cannot apply")
                else:
                    sleep(1)
                    driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(2)").click()

                    print("Applied")
                sleep(1)

            except Exception as e:
                print("Applying to this job failed with error:", e)
            # job is done processing
            completed_jobs.append(job_id)
            with open(USER_DATA_PATH, "w") as file_handle:
                file_handle.write(json.dumps(completed_jobs))
