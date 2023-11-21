from threading import Thread

import Indeed
import Dice
from common import common_utils

webdriver_options = common_utils.chromeBrowserOptions()
indeed_thread = Thread(target=Indeed.indeed.IndeedBot, args=webdriver_options)
dice_thread = Thread(target=Dice, args=webdriver_options)
thread.start()
thread.join()