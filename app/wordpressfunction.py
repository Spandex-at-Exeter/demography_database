from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib2 import HTTPError
from urllib2 import URLError
import numpy as np
import pandas as pd
import datetime
import random
import re

def wordpress_data():
	optionsUrl = 'https://compadredb.wordpress.com/'
	optionsPage = urlopen(optionsUrl)
	soup = BeautifulSoup(optionsPage, "html5lib")
	# titles
	titleList = soup.findAll('h1', attrs={'class': 'entry-title'})
	titles = []
	for apples in titleList:
		titles.append(apples.get_text())
	# content	
	contentList = soup.findAll('div', attrs={'class': 'entry-content'})
	contents = []
	for pears in contentList:
		contents.append(pears.get_text()[4:])

	# link
	middle_all = soup.findAll("h1", attrs={'class': 'entry-title'})
	result = []
	for middle in middle_all:
		result.extend(middle.find_all('a', href=True))
	# date
	timesList = soup.findAll('time', attrs={'class': 'entry-date'})
	dates = []
	for oranges in timesList:
		dates.append(oranges.get_text())
	# author
	authorList = soup.findAll('a', attrs={'class': 'url fn n'})
	authors = []
	for plums in authorList:
		authors.append(plums.get_text())
	# dataframe
	wordpress_data = pd.DataFrame({
		'Titles': titles,
		'Authors': authors,
		'Contents': contents,
		'Links': result,
		'Dates': dates })
#	wordpress_data.replaceAll("[\\n\\t\\t\\t]", "")
	return wordpress_data


