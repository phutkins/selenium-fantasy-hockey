import os

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import syfh_params


def login_to_yahoo():
    input("Need to login to Yahoo.  Please manually log in and press <Enter> when complete")
    print()
    return

    # logintxt = browser.find_element_by_name("username")
    # logintxt.send_keys(config.config['username'])
    # button = browser.find_element_by_id("login-signin")
    # button.click()
    #
    # # This block of code was too fast! I grabbed passwd, but by the next statement it was stale.
    # #    passwdtxt = browser.find_element_by_name("passwd")
    # #    WebDriverWait(browser, 10).until(
    # #        EC.visibility_of(passwdtxt)
    # #    )
    # passwdtxt = WebDriverWait(browser, 5).until(
    #     EC.visibility_of_element_located((By.NAME, "passwd"))
    # )
    # passwdtxt.send_keys(config.config['password'])
    # button = browser.find_element_by_id("login-signin")
    # button.click()


def chromedriver_executable_path(dirpath):
    exe_name = 'chromedriver'
    if sys.platform.startswith('win'):
        exe_name = 'chromedriver.exe'
    fullpath = os.path.join(dirpath, exe_name)
    return fullpath


def main():
    config = syfh_params.Config()
    config.confirm_params()
    browser = webdriver.Chrome(chromedriver_executable_path(config.config['chromedriver_path']))

    # attempt to go directly to the team website
    browser.get(config.config['team_website'])

    while "login.yahoo.com" in browser.current_url:
        login_to_yahoo()

    for i in range(int(config.config['days_to_start_active_payers']) + 1):
        print('Day %d: Now on %s' % (i, browser.current_url))

        try:
            start_active = browser.find_element_by_link_text('Start Active Players')
            print('Found <%s> element' % (start_active.text))
        except:
            print('Was not able to find Start Active Players button on page {}.'.format(browser.current_url))

        try:
            start_active.click()
        except:
            print('Unable to click Start Active Players')

        # clicking start_active causes a page reload.
        try:
            next_arrow = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'Js-next'))
            )
        except Exception as e:
            print('Was not able to find next arrow on page {}.'.format(browser.current_url))

        try:
            next_arrow.click()
        except:
            pass

        print()

    print("Saving parameters in {}".format(config.yaml_filename))
    config.save_params()
    print("DONE.")
    input('Press <Enter> to close browser')
    browser.quit()


if __name__ == '__main__':
    main()
