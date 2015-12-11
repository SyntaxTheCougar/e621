from e6g_functions import DataRetriever
from collections import OrderedDict
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import date, datetime, timedelta


def generateTimeSeries(startDate, endDate):
	 curr = startDate
	 delta = timedelta(days=1)
	 while curr < endDate:
		dic = {}
		dic[str(curr)] = 0
		yield dic
		curr += delta

tmp = generateTimeSeries(date(2011, 10, 10), date(2011, 12, 12))

for res in tmp:
	print res
