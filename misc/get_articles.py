#!/usr/bin/python3

import requests
import yaml
import json
import sys
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

store_file = "/home/r3g3n7/git/leevanrell.github.io/_data/bookmarks.yml"
bkmk_file = "/home/r3g3n7/git/leevanrell.github.io/misc/bookmarks.txt"

def getArticle(link):
	link = link.replace('\n','')
	result = requests.get(link)
	soup = BeautifulSoup(result.content, "lxml")
	head = soup.head
	try:
		title = head.find("meta", property="og:title")["content"]
	except Exception as E:
		try:
			title = head.find(property="title").text
		except Exception as E:
			return 0, link
	try: 
		description = soup.find("meta", property="og:description")["content"]
	except Exception as E:
		description = ""
	try: 	
		tags = [x["content"] for x in soup.find_all("meta", property="article:tag")][:2]
	except Exception as E:
		tags = ""
	return 1, {"url":link, "title": title.replace('\n',''), "excerpt": description.replace('\n',''), "categories": tags}

def getLinks():
	with open(bkmk_file , "r") as f:
		text = f.readlines()
	return text

def readArticles():
	stored = []
	try:
		with open(store_file, "r") as f:
			stored = yaml.load(f)
	except:
		stored = NULL
	return stored

def mergeArticles(stored, out):
	c = 0
	try:
		stored_titles = [x['title'] for x in stored['articles']]
		for article in out:
			if article['title'] not in stored_titles:
				stored['articles'].append(article)
				c += 1
	except Exception as e:
		print(f"Failed to merge with yaml {e}")
		print("Stored:")
		print(stored)
		print("New:")
		print(old)
		res = input("Only use New? (y/n)")
		if res[0] == 'y' or res[0] == 'Y':
			stored = {'articles': out}
		else:
			print('exiting!')
			sys.exit(1)
		c = len(out)	
	return c, stored 

def writeArticles(stored):
	noalias_dumper = yaml.dumper.SafeDumper
	noalias_dumper.ignore_aliases = lambda self, data: True
	with open(store_file, "w") as f:
		yaml.dump(stored, f, Dumper=noalias_dumper)

def main():
	links = getLinks()
	fails = []
	out = []
	for link in links:
		state, entry = getArticle(link)
		if state:
			out.append(entry)
		else:
			fails.append(entry)

	print(f"Failed to scrape {len(fails)} out of {len(links)}")
	for f in fails:
		print(f"\t-> {f[:60]}")

	c, stored = mergeArticles(readArticles(),out)

	print(f"Added {c} new articles out of {len(links)}")
	writeArticles(stored)

if __name__ == "__main__":
	main()
	sys.exit(0)