#!/usr/bin/python3

import requests
import yaml
import json
import sys
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

store_file = "/home/r3g3n7/git/leevanrell.github.io/_data/bookmarks.yml"
bkmk_file = "/home/r3g3n7/git/leevanrell.github.io/misc/bookmarks.txt"

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

def getLinks():
	with open(bkmk_file , "r") as f:
		text = f.readlines()
	clean = []
	for t in text:
		t.strip()
		if not t.isspace():
			clean.append(t)
	return clean

def readArticles():
	stored = []
	try:
		with open(store_file, "r") as f:
			stored = yaml.load(f)
	except:
		stored = None
	return stored

def mergeArticles(stored, new):
	c = 0
	try:
		stored_titles = [x['title'] for x in stored['articles']]
		for article in new:
			if article['title'] not in stored_titles:
				stored['articles'].append(article)
				c += 1
	except Exception as e:
		print(f"Failed to merge with yaml {e}")
		print("Stored:")
		print([print("\t->{entry['title'][:60]}\n") for entry in stored])
		print("New:")
		print([print("\t->{entry['title'][:60]}\n") for entry in new])
		res = input("Only use New? (y/n): ")
		print("")
		if res[0] == 'y' or res[0] == 'Y':
			stored = {'articles': new}
		else:
			print('exiting!')
			sys.exit(1)
		c = len(new)	
	return c, stored 

def writeArticles(store):
	noalias_dumper = yaml.dumper.SafeDumper
	noalias_dumper.ignore_aliases = lambda self, data: True
	with open(store_file, "w") as f:
		yaml.dump(store, f, Dumper=noalias_dumper)

def main():
	stored_articles = readArticles()
	links = getLinks()
	fails = []
	successes = []
	for link in links:
		p = ''
		if 'https://stackoverflow.com/' in link:
			p = stackoverflow_parser(link)
		else:
			p = parser(link)
		if p.title:
			successes.append(p.entry)
		else:
			fails.append(p.link)

	print(f"Failed to scrape {len(fails)} out of {len(links)}")
	for f in fails:
		print(f"\t-> {f[:60]}")

	c, store = mergeArticles(stored_articles,successes)

	print(f"Added {c} new articles out of {len(links)}")
	writeArticles(store)

if __name__ == "__main__":
	main()
	sys.exit(0)