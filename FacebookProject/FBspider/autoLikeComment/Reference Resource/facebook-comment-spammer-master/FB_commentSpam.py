import json
import fb                     #To install this package run: sudo pip install fb
from facepy import GraphAPI   #To install this package run: sudo pip install facepy

def spam():
    token="CAACEdEose0cBAGYzWog8leug7TJl8zDwMaZBJGZCw4WeGCYuI4TIeQagduDpozo4FcRriv7ZCJ3Q3dQCQyn70yGYxkprZAZB6nwMMi4Sin9uDa9BwactvOfBCYZCTiemsJIkWD7VjHBmtExxE6oOZBThjyUhK6CSVIjt5qWZBB8Q3fOkdbH9OpvUAhI50ZBspRcuAdF2elQkUJAZDZD"#Insert access token here.  
    facebook=fb.graph.api(token)
    graph1 = GraphAPI(token)
    
    vid=input("Enter victim's id: ")
    query=str(vid)+"/posts?fields=id&limit=5000000000"
    r=graph1.get(query)
    
    
    
    idlist=[x['id'] for x in r['data']]
    idlist.reverse()
    print("There are "+ str(len(idlist)) +" spammable posts.")
    
    char1=raw_input("Do you want to spam? (y/n) ")
    count=0
    if char1=='y':
        nos=input("Enter number of posts to be spammed with comments: ")
        mess=raw_input("Enter the message to be commented: ")
        if nos<=len(idlist):
           for indid in (idlist[(len(idlist)-nos):]):
        
              facebook.publish(cat="comments",id=indid,message=mess) #Comments on each post
              facebook.publish(cat="likes",id=indid)                 #Likes each post
              count=count+1
              print("Notification number:"+str(count)+" on www.facebook.com/"+str(indid).split('_')[0]+"/posts/"+str(indid).split('_')[1])
        else: 
              print("Not that many spammable posts available. No spam happening.")
    else :
      print("No spam happening then.")

spam()

'''
Facebook Comment Spammer
To use:  
1. Get a Facebook Graph API access token at: https://developers.facebook.com/tools/explorer  
2. Open terminal and run python.  
3. Make sure "fb" and "facepy" libraries are installed (see comments for instructions).  
4. Run program.  
'''