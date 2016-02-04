#!/usr/bin/env python

import time
HEADER = '\033[95m' # colours
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

from selenium import webdriver # selenium setup
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Firefox()




def help():		# help function, to lazy to type it ever again :)
	print(OKBLUE + "start : Start the script." + ENDC)
	print(OKBLUE + "version : Version." + ENDC)
	print(OKBLUE + "exit : Exit." + ENDC)
	print(OKBLUE + "info : Info." + ENDC)
	print(OKBLUE + "clear : Clear console." + ENDC)
	print(OKBLUE + "help : This help message." + ENDC)

tool = "friends@py:~# "
n = "\n" # simply shorter
cycle = True; # login cycle




while(True) :	# the script
	c = raw_input(OKGREEN + tool + ENDC)	# command-line-like interface
	if (c == "start"):	# if user wants to start the script
		x = input(BOLD + "Number of friends to add: " + ENDC)	# number of friends to add
		cf = x # ugly way to count

		while(cycle == True) :	# cycle while the script cannot login

			nme = raw_input("Your facebook username/email: ")	# facebook email / username
			psswrd = raw_input("Your facebook password: ")	# facebook password
	
			driver.get("https://www.facebook.com")	# go to facebook.com

			email = driver.find_element_by_name("email")	# search email textbox
			email.send_keys(nme)	# enter email / username = nme
			email.send_keys(Keys.TAB)	# probably useless, TEST IT!!!

			password = driver.find_element_by_name("pass")	# search password textbox

			password.send_keys(psswrd)	# enter password
			password.send_keys(Keys.RETURN)	# RETURN
			try:	# try to find Home-button and click it, it is only possible if logged in! So, test if logged in.
				driver.find_element_by_id('u_0_e').click()	# find Home-button and click it
				cycle = False; # if succeded, not cycle
				break; # break out of the cycle
			except NoSuchElementException: # if password and/or username are incorrect
				print(FAIL + "Your username and/or password appear to be incorrect" + ENDC) # report error
				cycle = True;	# cycle again

		time.sleep(4)	# wait, probably useless, TEST IT!!!
	
		for i in xrange (x): # friend adding cycle
			try:	# try to click Add Friend-button
				driver.find_element_by_partial_link_text('Add Friend').click()	# clicks Add Friend
				driver.get("https://www.facebook.com") # reloads : facebook will not think that the script is a bot + time delay (new friends appear)
				print(UNDERLINE + "Friend number " + OKBLUE + str(i) + ENDC + UNDERLINE + " has been added." + ENDC) # reports
			except NoSuchElementException: # if button not found
				time.sleep(8)	# wait (in hope that new Add Friend-buttons will appear)
				print(FAIL + "Error, friend couldn't been added" + ENDC) # report
				cf = cf -1 # loses one friend
				driver.get('https://www.facebook.com') # reload to check if new friends appeared

		print(OKGREEN + "You have succesfully added " + str(cf) + " friends \n" + ENDC) # reports how many friends were succesfully added
		#driver.close()	# clothes firefox window
	elif(c == "exit"):	# if user wants to exit
		print(FAIL + "Exiting...")	# report
		driver.close()	# close firefox window
		quit()	# exit this script
	elif(c == "version"):	# if user want to know the version number
		print('Version 1.1 \n')	# version
	elif(c == "info"):	# if user want info
		print("""This script is a simple facebook friend-request sender, it is still in development. If you wish to help or give an advice or an idea, you are welcome at """ +  OKBLUE + UNDERLINE + """https://gist.github.com/RRobotek/6619b5ca6948f1f49ae3\n""" +  ENDC + """Cheers, RRobotek \n""")
	elif(c == "clear"): # clear
		print(n * 64)	# 64 new lines
	elif(c == "help" or c == "H" or c == "h" or c == "HELP" or c == "Help"):	# help
		help()	# function above is used
	else:	# if command not recognized
		print(FAIL + "Command not recognized..." + ENDC)