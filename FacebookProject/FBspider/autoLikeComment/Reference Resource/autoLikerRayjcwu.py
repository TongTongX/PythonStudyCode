"""
a graph API script to press like on all statuses posted by target user
"""
import requests  # Use 3rd party request module for http request.
import json
import time

"""
search for your target user name in desktop version facebook.
when you press enter, you could see URL like https://www.facebook.com/profile.php?id=##############&fref=ts for a while
put the id field as TARGET_ID

get access token from facebook graph explorer https://developers.facebook.com/tools/explorer
with at least these permissions:

User data permissions: user_friends
Friends data permissions: friends_status, friends_photos, friends_likes
Extended permissions: publish_stream, publish_action
"""
TARGET_ID = ''   
ACCESS_TOKEN = ''

# like latest num statuses
def press_like(num=10):
    payload = {"fields": "statuses.limit(%d).fields(id)" % (num), "access_token": ACCESS_TOKEN}
    token = {"access_token": ACCESS_TOKEN}
    req = requests.get("https://graph.facebook.com/" + TARGET_ID, params=payload)
    content = req.content

    print content

    json_content = json.loads(content)

    for status_id in map(lambda x: x['id'], json_content['statuses']['data']):
        res = requests.post("https://graph.facebook.com/%s/likes" % status_id, params=token)
        print res.text


if __name__ == "__main__":
    while True:
        press_like()
        time.sleep(20)  # polling every 20 seconds
