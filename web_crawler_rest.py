#After runing a application
#http://0.0.0.0:5000

#pass depth as a url arguement
#http://0.0.0.0:5000/1
#http://0.0.0.0:5000/2


from bs4 import BeautifulSoup
import requests
import re
import sys
import json
print sys.argv
from flask_restful import Api
from flask import Blueprint
from flask_restful import Resource, Api
from flask import Flask

app = Flask(__name__)
api = Api(app)


def get_url():
	"""
	return the list of images
	"""
	url_to_poll = 'https://gale.agency'
	page = requests.get(url_to_poll)
	soup = BeautifulSoup(page.content , features="html.parser") 
	links = soup.findAll("a") 
	links = []
	for link in soup.findAll('a', attrs={'href': re.compile("^https://gale")}):
	    links.append(link.get('href'))
	return list(set(links))

def get_imge(url):
	"""
	Get the iamges from list of url
	"""
	images_from_url  = []
	page = requests.get(url)
	soup = BeautifulSoup(page.content , features="html.parser") 
	images = soup.findAll('img')
	for image in images:
		if image['src'] not in images_from_url:
			images_from_url.append(image['src'])
	return images_from_url


class HomePage(Resource):
    def get(self):
        return {'data':'homePage of url poller'}


class UrlPoller(Resource):
    def get(self, depth):
		image_extrcted =[]
		if depth == 1:
			urls = get_url()
			return json.loads(json.dumps(urls))
		elif depth <= 2:
			urls = get_url()
			for url in set(urls):
				images = get_imge(url)
				image_extrcted.append({url : images})
			return json.loads(json.dumps(image_extrcted))


api.add_resource(HomePage, '/')
api.add_resource(UrlPoller, '/<int:depth>')


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
