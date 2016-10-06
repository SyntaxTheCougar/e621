import plotly.plotly as py
import plotly.graph_objs as go
import urllib
import urllib2
import json
import datetime
from threading import Thread

class DataRetriever :
	BASE_URL =  "https://e621.net/" 
	
	def __init__(self):
		self.jsonData = {}

	
	def buildQuery(self, controller, action, params):
		url = "https://e621.net/" + controller + "/" + action + ".json?"
		
		if not params:
			return url

		for key,value in params.iteritems(): 
			url += key + "=" + str(value)
			url += "&"  
	
		url = url[:-1]	
		return url

	def getPostsForTag(self, tagname):
		params = {'limit': 320, 'tags' : tagname}
		url = self.buildQuery('post', 'index', params)
		page = "&page="
		page_num = 1
		post_list = []

		while True:
			fullURL =  url + page + str(page_num)
			print "Getting page " + str(page_num) + " for " + tagname
			print "URL: " + fullURL
			parsed = self.jsonFromURL(fullURL)
			post_list = post_list + parsed
	
			page_num += 1

			if not parsed:
				break
	
		for post in post_list: 
				print str(post["id"]) + " : " + str(datetime.datetime.fromtimestamp(post["created_at"]["s"]).date())
		print "Posts gotten for " + tagname + ": " + str(len(post_list))
		
		self.jsonData[tagname] = post_list
		return post_list 

	def jsonFromURL(self, url):
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
		response = urllib2.urlopen(req)
		json_data = response.read()
		parsedJson = json.loads(json_data)
		return parsedJson

	def getFirstPage(self):
		url = self.buildQuery("post", "index", None)
		return self.jsonFromURL(url)
		
	def getFirstN(self, num):
		params = {'limit': num}
		url = self.buildQuery("post", "index", params)
		return self.jsonFromURL(url)
		
	def downloadInParallel(self, tags):
		threads = [] 
		for tag in tags:
			print tags
			threads = threads + [Thread(target=self.getPostsForTag, args=(tag,))]
	
		for thread in threads:
			thread.start() 

		for thread in threads:
			thread.join() 

		print "Complete!"
		return self.jsonData 

