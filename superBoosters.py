import json
import pprint
import requests
import pytumblr
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

client = pytumblr.TumblrRestClient(
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
)

# data is a dict

link = 'https://staff.tumblr.com/post/667496084224032768/'
domain = link.split('/')[2]
blog_name = domain.split('.')[0]
id = link.split('/')[-1:][0]

parent_blogs = []

def getParentBlogs(blog_name, id, before_timestamp):
    data = client.notes(blog_name, id=id, before_timestamp = before_timestamp)
    notes = data['notes']
    for note in notes:
        if note['type'] == 'reblog':
            reblog_parent_blog_name = note['reblog_parent_blog_name']
            parent_blogs.append(reblog_parent_blog_name)
    try:
        before_timestamp = data['_links']['next']['query_params']['before_timestamp']
    except KeyError:
        print('Iteration Complete.')
        return
    try:
        getParentBlogs(blog_name, id, data['_links']['next']['query_params']['before_timestamp'])
    except:
        return


getParentBlogs(blog_name, id, str(int(time.time())))

def getSuperSpreaders():
        dict = {}
        for x in parent_blogs:
            if x in dict:
                dict[x] += 1
            else:
                dict[x] = 1
        top = sorted(dict, key=lambda x: (-dict[x], x))
        return top[:10]

print(getSuperSpreaders())
