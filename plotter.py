from e6g_connection import DataRetriever
from collections import OrderedDict
import plotly.plotly as py
import plotly.graph_objs as go
import datetime

py.sign_in('humun', '9aq7qo7ayd')
plot_data = []

def generateTimeSeries(startDate, endDate):
	 curr = startDate
	 delta = datetime.timedelta(days=1)
	 while curr <= endDate:
		dic = {}
		dic[str(curr)] = 0
		yield dic
		curr += delta

def posts_per_day(jsonPosts):
	for tag in jsonPosts.keys(): 
		posts_per_day = OrderedDict()

		first_date = jsonPosts[tag][len(jsonPosts[tag])-1]["created_at"]["s"]
		first_date = datetime.datetime.fromtimestamp(first_date).date()
		print "First date: " + str(first_date) 

		last_date = jsonPosts[tag][0]["created_at"]["s"]
		last_date = datetime.datetime.fromtimestamp(last_date).date()
		print "Last date: " + str(last_date) 

		date_range = OrderedDict()

		for date in generateTimeSeries(first_date, last_date):
			date_range.update(date)
		
		for post in reversed(jsonPosts[tag]):
			timestamp = post["created_at"]["s"]
			date = datetime.datetime.fromtimestamp(timestamp).date()

			date_str = str(date)
			
			date_range[date_str] += 1

		plot(date_range, tag)

def total(jsonPosts):
	for tag in jsonPosts.keys(): 
		total = 0
		date_range = OrderedDict()
		
		for post in reversed(jsonPosts[tag]):
			timestamp = post["created_at"]["s"]
			date = datetime.datetime.fromtimestamp(timestamp).date()
			date_str = str(date)

			total = total + 1
			date_range[date_str] = total 
			
		plot(date_range, tag)
		
def plot(data, tag):
	global plot_data
	plot_data += [
		go.Scatter(
			x = list(data.keys()),
			y = list(data.values()),
			name = tag
		)]

dr = DataRetriever()
dr.downloadInParallel(['darkgem', 'sindoll', 'narse', 'the_weaver', 'kihu', 'slugbox', 'daigaijin', 'aogami'])

total(dr.jsonData)
plot_url = py.plot(plot_data, filename='hit')




