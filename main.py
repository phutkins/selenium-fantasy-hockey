import os

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import syfh_params


def login_to_yahoo():
    input("User needs to login to Yahoo.  Press <Enter> when logged in to continue.")
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




def main():
    config = syfh_params.Config()
    config.confirm_all_params()
    browser = webdriver.Chrome(config.config['chromedriver_path'])
    browser.implicitly_wait(10)     # implicit wait fo 10s for all actions

    # attempt to go directly to the team website
    browser.get(config.config['team_website'])

    while "login.yahoo.com" in browser.current_url:
        login_to_yahoo()

    for i in range(int(config.config['days_to_start_active_payers']) + 1):
        print('Day %d: Now on %s' % (i, browser.current_url))

        try:
            # start_active = browser.find_element_by_link_text('Start Active Players')
            start_active = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Start Active Players'))
            )
            print('Found <%s> element' % (start_active.text))
        except:
            print('Was not able to find Start Active Players button on page {}.'.format(browser.current_url))

        try:
            # browser.execute_script("return arguments[0].scrollIntoView();", start_active)
            start_active.click()
            print('Clicking start active element')
        except Exception as exc:
            print('Unable to click Start Active Players. {}'.format(exc))

        # clicking start_active causes a page reload.
        try:
            next_arrow = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'Js-next'))
            )
            print('Found next arrow element')
        except Exception as e:
            print('Was not able to find next arrow on page {}.'.format(browser.current_url))

        try:
            # browser.execute_script("return arguments[0].scrollIntoView();", next_arrow)
            next_arrow.click()
            print('Clicked next arrow element')
        except Exception as exc:
            print('Unable to click next arrow to get to next page. {}'.format(exc))

        print()

    print("Saving parameters in {}".format(config.yaml_filename))
    config.save_params()
    print("DONE.")
    input('Press <Enter> to close browser')
    browser.quit()


if __name__ == '__main__':
    main()
