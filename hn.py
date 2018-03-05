import requests
from bs4 import BeautifulSoup
from lxml import html
from mongoengine import *
import time


BASE=  "https://news.ycombinator.com/news?p="
session_requests = requests.session()

ct=0
title=[]
score=[]
hnuser=[]
time=[]
for i in range(1,51):
	URL=BASE+str(i)
	r = session_requests.get(URL)
	soup = BeautifulSoup(r.content, 'html.parser')
	for node in soup.find_all("a", "storylink"):
		title.append(node.text)
	for node in soup.find_all("span", "age"):
		time.append(node.text)
	for node in soup.find_all("a", "hnuser"):
		hnuser.append(node.text)
	for node in soup.find_all("span", "score"):
		score.append(node.text)
	if len(title)>len(hnuser):
		title.pop()
		time.pop()

class post(Document):
	title = StringField(max_length=120, required=True)
	author = StringField(max_length=120, required=True)
	time=StringField(max_length=120,required=True)
	score=StringField(max_length=50,required=True)

#puts data in mongodb
connect( db='hackerycom', username='vutsuak', password='hn', host='ds253918.mlab.com:53918')


for i in range(len(score)):
	try:
		p=post(title=title[i],author=hnuser[i],time=time[i],score=score[i])
		p.save()
	except:
		continue




#curl -H 'Content-Type: application/x-ndjson' -XPOST 'https://site:410cc42245545394a3bffceebf1c714c@thorin-us-east-1.searchly.com/news/posts/_bulk?pretty' --data-binary @l.json
#curl -XGET 'https://site:410cc42245545394a3bffceebf1c714c@thorin-us-east-1.searchly.com/newss/posts/_search?q=python'