from flask import Flask,render_template
from flask import request


app = Flask(__name__)
@app.route('/')
def index():
	return render_template('index.html')

def read_wfile(word, year_range, wfile, tfile):
	import csv as csv
	import numpy as np
	from datetime import datetime as dt
	import matplotlib.pyplot as plt
	from csv import reader
	import operator
	import mpld3
	import codecs
	import json
	from scipy.interpolate import spline
	from matplotlib import rc
	from matplotlib.dates import MONDAY
	from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
	import matplotlib.dates as mdates
	#years = mdates.YearLocator()   # every year
	#months = mdates.MonthLocator()  # every month
	#yearsFmt = mdates.DateFormatter('%Y')
	year, vol = list(zip(*list(reader(open('datafiles/'+tfile)))))[0:2]
	year_range_array = range(year_range[0], year_range[1]+1)
	'''
	date1 = datetime.date(int(year_range[0], 1, 1)
	date2 = datetime.date(int(year_range[1]), 12, 1)

	# every monday
	mondays = WeekdayLocator(MONDAY)

	# every 3rd month
	months = MonthLocator(range(1, 13), bymonthday=1, interval=3)
	monthsFmt = DateFormatter("%b '%y")
	'''
	#initialize a dictionary
	mydata = {}
	for r in reader(open('datafiles/'+wfile,encoding='utf-8'),delimiter=','):
		#Num times the word appears/Total number of words from all texts
		f = float(r[2]) / float(vol[year.index(r[1])])

		#If the term is already in my dictionary, append another value to the key
		#Else create a new key
		if r[0] in mydata and r[0] in word and int(r[1]) in year_range_array:
			mydata[r[0]].append((int(r[1]), f))
		elif r[0] not in mydata and r[0] in word and int(r[1]) in year_range_array:
			mydata[r[0]] = [(int(r[1]), f)]

	#Dictionary has word as a key and a list of tuples as the value.
	#This removes the list from the key/value pair
	mydata_list = [mydata[x] for x in word]
	#print mydata_list
	#print mydata

	#mpld3 implementation
	fig , ax = plt.subplots()

	#This takes the list of tuples and plots it
	for x in mydata_list:
		#print x
		#print zip(*x)
		k = np.array(list(zip(*x))[0])
		l = np.array(list(zip(*x))[1])
		k_smooth = np.linspace(k.min(),k.max(),100)
		l_smooth = spline(k,l,k_smooth)
		ax.plot(*zip(*x))
		#ax.plot(k_smooth,l_smooth,linewidth=1.7)
	plt.rc('font',family='Lucida Grande')
	plt.xlabel("Year")
	plt.ylabel("Relative frequency")
	plt.grid(alpha=0.3)
	plt.legend(word)
	plt.savefig('static/img/data.png')
	#plt.show()
	#return mpld3.fig_to_html(fig)
	return json.dumps(mpld3.fig_to_dict(fig))

@app.route('/view',methods=['POST','GET'])
def view():
	terms =  request.form['ngram'];
	ngrams = terms.split(',')
	#ngrams = [ str.strip(x) for x in ngrams]
	startyear = request.form['startyear']
	endyear = request.form['endyear']
	time_range = list()
	time_range.append(startyear)
	time_range.append(endyear)
	time_range = [ int(i) for i in time_range ]
	graph = read_wfile(ngrams,time_range, 'data.csv', 'total_count.csv')
	return graph


if __name__ == '__main__':
	app.run(debug=True)
