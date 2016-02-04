'''
	For this program, access token needs to be copied from Facebook Graph API Explorer.
	Status: not completed, target id can only be the user himself/herself or a public 
	account (e.g. harrypottermovies, emmawatson, etc). It seems better to use selenium.
'''

import facebook

token = "CAACEdEose0cBAGYzWog8leug7TJl8zDwMaZBJGZCw4WeGCYuI4TIeQagduDpozo4FcRriv7ZCJ3Q3dQCQyn70yGYxkprZAZB6nwMMi4Sin9uDa9BwactvOfBCYZCTiemsJIkWD7VjHBmtExxE6oOZBThjyUhK6CSVIjt5qWZBB8Q3fOkdbH9OpvUAhI50ZBspRcuAdF2elQkUJAZDZD"
graph = facebook.GraphAPI(token)

profile = graph.get_object("xutong.zhao.7")
#profile = graph.get_object("100006358157877")
posts = graph.get_connections(profile['id'],"posts")

for post in posts['data']:
	print "code running"
	try:
		graph.put_object(post['id'],"likes")
		print "Liking the topic: " + post["story"]
	except:
		continue
	
