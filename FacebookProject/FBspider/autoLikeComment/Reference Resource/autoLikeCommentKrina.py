'''
http://programming-in-python.blogspot.in/2015/12/auto-like-and-auto-comment-facebook.html

Like and comment all the posts on Facebook(using python)

We will need following 2 things:
1. Access token
2. Object Id

Where to get this from????

Goto: 
developers.facebook.com->Tools and Support->GraphAPI Explorer

1. Copy access token
2. Click on submit
3. Copy id
'''

import facebook
#import re
token = "CAACEdEose0cBAHQ8pLQpHZCaEzAAJ0ZAEDkcxd7NJub5uZCXcZCDBBtTwPYmyteEUQFJBSO8BpQs9d9fPS47Epxwcm5ZAM41855xkeW7Jk6bx7DYJuq2VrB8gVfmZAgJUX6HW5sp6KZCPqTAk8LkWiYq0rgpICLRe45c5Qu6y7FP84LTsoUdFxiZAe5ZAasmqZCsylJLpi59axAFpdDtpiHsif"
graph = facebook.GraphAPI(token)
#pages = ['rahuldravid']
#profile = graph.get_object("100006358157877")
profile = graph.get_object("100006319206561")
posts = graph.get_connections(profile['id'],"posts") # this line would connect us to the facebook profile
for post in posts['data']:
        #print "code running"
        try:
            graph.put_object(post['id'],"likes") #this line would like all the posts of facebook
            #graph.put_comment(post['id'],message="Long live rahul dravid") # I am going to comment "Long live rahul dravid"
            print "Liking the topic :" +post["message"] # Just to check whether our script is working or not...Lets print message
        except:
            continue

