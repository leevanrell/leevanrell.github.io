#!/usr/bin/python3

import requests
import yaml
import json
import sys
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

#store_file = "/home/r3g3n7/git/leevanrell.github.io/_data/bookmarks.yml"
#bkmk_file = "/home/r3g3n7/git/leevanrell.github.io/misc/bookmarks.txt"


class parser():
	def __init__(self, link):
		link =  link.replace('\n','')
		self.entry = None
		soup = self.getContent()
		if soup:
			title = self.getTitle(soup.head)
			description = self.getDescription(soup)
			tags = self.getTags(soup)
			self.entry = {
				'title': title,
				'excerpt': description,
				'categories': tags,
				'url': link
			}

	def __repr__(self):
		return str(self.entry)

	def getContent(self):
		try:
			result = requests.get(self.link, timeout=1)
			soup = BeautifulSoup(result.content, "lxml")
			return soup
		except:
			return None

	def getTitle(self, head):
		try:
			title = head.find("meta", property="og:title")["content"]
		except Exception as E:
			try:
				title =  head.find(property="title").text
			except Exception as E:
				title = ""
		return title

	def getDescription(self, soup):
		try: 
			description = soup.find("meta", property="og:description")["content"].replace('\n', ' ')
		except Exception as E:
			description = ""
		return description

	def getTags(self, soup):
		try: 	
			tags = [x["content"] for x in soup.find_all("meta", property="article:tag")][:3]
		except Exception as E:
			tags = ""
		return tags


class stackoverflow_parser(parser):
	def __init__(self, link):
		super().__init__(link)

	def getTags(self):
		tags = [tag.text for tag in soup.find_all('a', class_='post-tag')][:3]
		return tags


def main(link):
	p = ''
	if 'https://stackoverflow.com/' in link:
		p = stackoverflow_parser(link)
	else:
		p = parser(link)
	print(p)
	if p.entry:	
		noalias_dumper = yaml.dumper.SafeDumper
		noalias_dumper.ignore_aliases = lambda self, data: True
		print(yaml.dump(p.entry))#, Dumper=noalias_dumper))
	else:
		print('Failed')


if __name__ == "__main__":
	main(sys.argv[1])