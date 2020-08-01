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
		self.link =  link.replace('\n','')
		self.soup = self.getContent()
		if self.soup:
			self.head = self.soup.head
			self.title, self.description, self.tags  = '','',''
			self.setTitle()
			if self.title != 0:
				self.setDescription()
				self.setTags()
			self.entry = {
				'title': self.title,
				'excerpt': self.description,
				'categories': self.tags,
				'url': self.link
			}
		else:
			self.title = None

	def __repr__(self):
		return self.entry

	def getContent(self):
		try:
			result = requests.get(self.link, timeout=1)
			soup = BeautifulSoup(result.content, "lxml")
			return soup
		except:
			return None

	def setTitle(self):
		try:
			self.title = self.head.find("meta", property="og:title")["content"]
		except Exception as E:
			try:
				self.title =  self.head.find(property="title").text
			except Exception as E:
				self.title =  ""

	def setDescription(self):
		try: 
			self.description = self.soup.find("meta", property="og:description")["content"].replace('\n', ' ')
		except Exception as E:
			self.description = ""

	def setTags(self):
		try: 	
			self.tags = [x["content"] for x in self.soup.find_all("meta", property="article:tag")][:3]
		except Exception as E:
			self.tags = ""


class stackoverflow_parser(parser):
	def __init__(self, link):
		super().__init__(link)

	def setTags(self):
		self.tags = [tag.text for tag in self.soup.find_all('a', class_='post-tag')][:3]


def main(link):
	p = ''
	if 'https://stackoverflow.com/' in link:
		p = stackoverflow_parser(link)
	else:
		p = parser(link)
	if p.title:	
		noalias_dumper = yaml.dumper.SafeDumper
		noalias_dumper.ignore_aliases = lambda self, data: True
		print(yaml.dump(p.entry))#, Dumper=noalias_dumper))
		#successes.append(p.entry)
	else:
		print('Failed')
		#fails.append(p.link)


if __name__ == "__main__":
	main(sys.argv[1])