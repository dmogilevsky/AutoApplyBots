from time import sleep

from selenium import webdriver
import config


def chromeBrowserOptions():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    initial_path = config.chromeProfilePath[0:config.chromeProfilePath.rfind("/")]
    profile_dir = config.chromeProfilePath[config.chromeProfilePath.rfind("/") + 1:]
    options.add_argument('--user-data-dir=' + initial_path)
    options.add_argument('--profile-directory=' + profile_dir)
    return options


def prRed(prt):
    print(f"\033[91m{prt}\033[00m")


def prGreen(prt):
    print(f"\033[92m{prt}\033[00m")


def prYellow(prt):
    print(f"\033[93m{prt}\033[00m")


def printInfoMes(bot: str):
    prYellow("ℹ️ " + bot + " is starting soon... ")


def donate(self):
    prYellow('If you like the project, please support me so that i can make more such projects, thanks!')
    try:
        self.driver.get('https://commerce.coinbase.com/checkout/923b8005-792f-4874-9a14-2992d0b30685')
    except Exception as e:
        prRed("Error in donate: " + str(e))


# Click element normally, if an error occurs, try clicking its position instead
def click_element_and_wait(selenium_driver, by, value, wait=3.0):
    element = selenium_driver.find_element(by, value)
    try:
        element.click()
    except Exception:
        actions = webdriver.common.action_chains.ActionChains(selenium_driver)
        actions.move_to_element_with_offset(element, 1, 1).click().perform()

    sleep(wait)


def element_exists(selenium_driver, by, value):
    return not (len(selenium_driver.find_elements(by, value)) == 0)
