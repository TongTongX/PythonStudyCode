from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import time

driver = webdriver.Firefox()


def init():
    print "------- initialization -------------"
    driver.get("https://www.facebook.com")
    #cookies = pickle.load(open("cookies.pkl", "rb"))
    #for cookie in cookies:
    #    driver.add_cookie(cookie)


def login():
    driver = webdriver.Firefox()

    driver.implicitly_wait(10)

    driver.get("https://www.facebook.com")
    driver.find_element_by_id('email').send_keys("email_address")
    driver.find_element_by_id('pass').send_keys("password")
    driver.find_element_by_id('u_0_n').click()

    '''
    time.sleep(1)
    print "------- login ---------"
    email = driver.find_element_by_id('email')
    email.send_keys("email_address")
    time.sleep(1)
    password = driver.find_element_by_id('pass')
    password.send_keys("password")
    time.sleep(1)
    password.send_keys(Keys.RETURN)
    time.sleep(2)
    driver.get("https://www.facebook.com")
    time.sleep(1)
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "w"))
    '''

def do_the_liking():
    links_list = driver.find_elements_by_class_name("UFILikeLink")
    print "Found %d total links." % len(links_list)

    for link in links_list:
        try:
            if "Like this comment" not in link.get_attribute("title"):
                link.click()
                time.sleep(1)
        except Exception,ex:
            print "Ex: "+ex.message

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)




if __name__ == '__main__':
    #init()
    login()

    counter = 0
    while True:
        counter += 1
        print "finished %d. ZzzZzzz" % counter
        time.sleep(5)
        driver.get("https://www.facebook.com")
        time.sleep(5)
        do_the_liking()