# FBSpider - A facebook crwalling software
#
#  Copyright (c) 2016 Michael(Zichun) Lin, Yu Zhu, Xutong Zhao. All rights reserved.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#from selenium.webdriver.common.by import By

from selenium import webdriver # selenium setup
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


import sys

class FBLogin():
    # get log in info from text file
    def __init__(self):
        with open('key') as file:
            for line in file:
                line = line.strip().split(" ")
                self.username = line[0]
                self.password = line[1]

    # simulate login
    def login(self):
        browser = webdriver.Firefox()

        browser.implicitly_wait(10)

        browser.get("https://www.facebook.com")
        browser.maximize_window()
        browser.find_element_by_id('email').send_keys(self.username)
        browser.find_element_by_id('pass').send_keys(self.password)
        browser.find_element_by_id('u_0_n').click()

        
        # go to friend list page
        browser.find_element_by_class_name("_2dpe").click()
        friendURL = browser.current_url + '/friends'
        browser.get(friendURL)
	
	# TO_DO: since Facebook doesn't consider links going to friend's homepage as
	# "links", friends' name cannot be located using find_element_by_link_text or
	# find_element_by_partial_link_text. Needs to be fixed using a different method.

        '''
        #browser.find_element_by_partial_link_text('Bruce').click()
        '''
        '''
        # auto like
        for i in xrange (1): # friend adding cycle
            try:    # try to click Add Friend-button
                browser.find_element_by_partial_link_text('Recently Added').click()  # clicks Add Friend
                #browser.get("https://www.facebook.com") # reloads : facebook will not think that the script is a bot + time delay (new friends appear)
                #print(UNDERLINE + "Friend number " + OKBLUE + str(i) + ENDC + UNDERLINE + " has been added." + ENDC) # reports
            except NoSuchElementException: # if button not found
                time.sleep(8)   # wait (in hope that new Add Friend-buttons will appear)
                print "Error, cannot open friend's page"  # report
                
                browser.get('https://www.facebook.com') # reload to check if new friends appeared

        #browser.find_element_by_class_name("_48-k UFLikeLink").click()
        '''
        
        # like posts on this page 
        browser.get("https://www.facebook.com/foreverkev")
        for i in xrange(5):
            try:
                like_link = browser.find_elements_by_class_name("UFILikeLink").click()
                print "Like #" + str(i) +", liked friend's post"
                browser.get(browser.current_url)
            except:
                time.sleep(8)
                print "Error #" + str(i) +", cannot like friend's post"
                browser.get(browser.current_url)

        '''
        like_link = browser.find_elements_by_class_name("UFILikeLink")
        #print "Found %d total links." % len(like_link)
        print "like_link: " + str(len(like_link))
        for x in range(len(like_link)):
            print x
            #like_link[x].click()
            try:
                #if link.is_displayed():
                like_link[x].click()
            except Exception,ex:
                print "Ex: "+ ex.message
            
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        '''
    
        


    # login before runing this function
    # get access token from Facebook API Explorer
    def accessToken(self):
        browser = webdriver.Firefox()
        browser.get("https://developers.facebook.com/tools/explorer")




        

