#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
 
import time
 
def AutoAdd(n):
    '''
    input argument: n, 3*n is number of friends you would like to add
    '''
    Buttonletters = ["o","p","r"]
    for a in range(n):
        #driver.find_element_by_id("findFriendsNav").click()
        #driver.get("https://www.facebook.com/?sk=ff")
        
        for letter in Buttonletters:
                id_index = "u_0_1"+letter
                add_friend = driver.find_element_by_id(id_index).click()
        # driver.find_element_by_class_name("FriendButton").click()
 
 
# Facebook setup
driver = webdriver.Firefox()
driver.get("https://www.facebook.com")
driver.maximize_window()
 
# Facebook login
inputEmail = driver.find_element_by_id("email")
inputEmail.send_keys("alanzhaoxutong@hotmail.com")
inputPass = driver.find_element_by_id("pass")
inputPass.send_keys("cyc19960628face")
inputPass.submit()
 
#driver.find_element_by_id("findFriendsNav").click()
driver.get("https://www.facebook.com/?sk=ff")

AutoAdd(5)