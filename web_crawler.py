from bs4 import BeautifulSoup
import requests
import re
import sys
print sys.argv



def get_url():
	"""
	return the list of images
	"""
	page = requests.get(sys.argv[1])
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


def main():
	url_with_image = {}
	image_extrcted = []
	if len(sys.argv) <= 2:
		print "pass 3 arguements exsmaple python web_crawler.py https://gale.agency 2"
		sys.exit()
	urls = get_url()
	print "url extracted" ,urls
	if len(sys.argv) <=3 and int(sys.argv[2]) >= 2:
		for url in set(urls[:]):
			images = get_imge(url)
			image_extrcted.append({url : images})
		print image_extrcted

if __name__ == '__main__':
	main()