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
        browser.get("https://www.facebook.com")
        browser.find_element_by_id('email').send_keys(self.username)
        browser.find_element_by_id('pass').send_keys(self.password)
        browser.find_element_by_id('u_0_n').click()
