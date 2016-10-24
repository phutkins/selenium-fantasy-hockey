from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MY_TEAM_PAGE = 'https://hockey.fantasysports.yahoo.com/hockey/46760/2'
NUMBER_OF_DAYS = 10


CHROME_DRIVER_LOCATION = "/Users/phutkins/bin/chromedriver"
browser = webdriver.Chrome(CHROME_DRIVER_LOCATION)


browser.get(MY_TEAM_PAGE)
#browser.get('https://login.yahoo.com/')


def login_to_yahoo():
    logintxt = browser.find_element_by_name("username")
    logintxt.send_keys(USERNAME)

    button = browser.find_element_by_id("login-signin")
    button.click()

# This block of code was too fast! I grabbed passwd, but by the next statement it was stale.
#    passwdtxt = browser.find_element_by_name("passwd")
#    WebDriverWait(browser, 10).until(
#        EC.visibility_of(passwdtxt)
#    )
    passwdtxt = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.NAME,"passwd"))
    )
    passwdtxt.send_keys(SECRET_PASSWORD)

    button = browser.find_element_by_id("login-signin")
    button.click()


def main():
    if "login.yahoo.com" in browser.current_url:
        login_to_yahoo()

    browser.get(MY_TEAM_PAGE)

    for i in range(NUMBER_OF_DAYS + 1):
        print('Day %d: Now on %s' % (i, browser.current_url))

        try:
            start_active = browser.find_element_by_link_text('Start Active Players')
            print('Found <%s> element' % (start_active.text))
        except:
            print('Was not able to find an element with that name.')

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
            print('Was not able to find an element for the next arrow.')

        try:
            next_arrow.click()
        except:
            pass

        print()

    print("DONE.")
    browser.quit()



if __name__ == '__main__':
    main()
