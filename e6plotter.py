from e6g_functions import DataRetriever
from collections import OrderedDict
import plotly.plotly as py
import plotly.graph_objs as go
import datetime

def generateTimeSeries(startDate, endDate):
	 curr = startDate
	 delta = datetime.timedelta(days=1)
	 while curr <= endDate:
		dic = {}
		dic[str(curr)] = 0
		yield dic
		curr += delta

dr = DataRetriever()

dr.downloadInParallel(['onta'])

plot_data = []

for tag in dr.jsonData.keys(): 
	posts_per_day = OrderedDict()

	first_date = dr.jsonData[tag][len(dr.jsonData[tag])-1]["created_at"]["s"]
	first_date = datetime.datetime.fromtimestamp(first_date).date()
	print "First date: " + str(first_date) 

	last_date = dr.jsonData[tag][0]["created_at"]["s"]
	last_date = datetime.datetime.fromtimestamp(last_date).date()
	print "Last date: " + str(last_date) 

	date_range = OrderedDict()

	for date in generateTimeSeries(first_date, last_date):
		date_range.update(date)

	for post in dr.jsonData[tag]:
		timestamp = post["created_at"]["s"]
		date = datetime.datetime.fromtimestamp(timestamp).date()

		date_str = str(date)

		date_range[date_str] += 1

		#if date_str in posts_per_day:
		#	posts_per_day[date_str] += 1
		#else:
		#	posts_per_day[date_str] = 1


	
	plot_data += [
		go.Scatter(
			x = list(date_range.keys()),
			y = list(date_range.values()),
			name = tag
		)]
	

plot_url = py.plot(plot_data, filename='hit')

#for plot in plot_data: 
#	print plot

