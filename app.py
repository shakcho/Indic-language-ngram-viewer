from flask import Flask,render_template
from flask import request


app = Flask(__name__)
@app.route('/')
def index():
	return render_template('index.html')
@app.route('/mpl')
def mpl():
	import matplotlib.pyplot as plt, mpld3
	import numpy as np
	fig, ax = plt.subplots()
	np.random.seed(0)
	x, y = np.random.normal(size=(2, 200))
	color, size = np.random.random((2, 200))

	ax.scatter(x, y, c=color, s=500 * size, alpha=0.3)
	ax.grid(color='lightgray', alpha=0.7)
	mpld3.save_json(fig,"data.json")
	mpld3.save_html(fig,"data.html")
	return mpld3.fig_to_html(fig)

def read_wfile(word, year_range, wfile, tfile): 
	import csv as csv
	import numpy as np
	from datetime import datetime as dt
	import matplotlib.pyplot as plt
	from csv import reader
	import operator
	import mpld3
	year, vol = zip(*list(reader(open('datafiles3/'+tfile))))[0:2]
	year_range_array = range(year_range[0], year_range[1]+1)

	#initialize a dictionary
	mydata = {}
	for r in reader(open('datafiles3/'+wfile),delimiter='\t'):
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
		ax.plot(*zip(*x))
	plt.xlabel("Year")
	plt.ylabel("Relative frequency")
	plt.grid()
	plt.legend(word)
	#plt.show()
	return mpld3.fig_to_html(fig)

@app.route('/view',methods=['POST','GET'])
def view():
	terms =  request.form['ngram'];
	ngrams = terms.split(',')
	#ngrams = [ str.strip(x) for x in ngrams]
	startyear = request.form['startyear']
	endyear = request.form['endyear']
	#ngrams = ['horse', 'computer','Art']
	time_range = list()
	time_range.append(startyear)
	time_range.append(endyear)
	time_range = [ int(i) for i in time_range ]
	graph = read_wfile(ngrams,time_range, 'all_words.csv', 'total_counts.csv')
	return graph


if __name__ == '__main__':
	app.run(debug=True)