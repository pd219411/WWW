import urllib
import urlparse
#from BeautifulSoup import *
from bs4 import BeautifulSoup

#params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
directory_url = "http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/"
#file_url = "index.htm"
file_url = "020100.htm"

class DataExtractor:
	def extract_data(self):
		pass

def soup_html_from_url(url):
	stream = urllib.urlopen(url)
	html = stream.read()
	stream.close()
	return BeautifulSoup(html)

def extract_link_from_row(soup_row):
	return soup_row.find("a", {"class" : "link1"}).get("href")

def extract_info_from_row(soup_row):
	cells = soup_row.findAll("td")
	print cells[1].string
	print cells[2].string
	return "EMPTY DATA"
	

def extract_data_from_html(soup_html):
	table = soup_html.find("table", {"id" : "s0"})

	body = table.find_all("tbody")[0]
	rows = body.find_all("tr", {})

	data_list = []

	for row in rows:
		print "=================================== ROW >>"
		print extract_info_from_row(row)
		print extract_link_from_row(row)
		data_list.append((extract_link_from_row(row), extract_info_from_row(row)))
		print "===================================ZZZZZZZZ"

	return data_list

def data_from_url(url):
	return extract_data_from_html(soup_html_from_url(url))

def crawl_page(base_url, file_url, level):
	page_url = urlparse.urljoin(directory_url, file_url)
	print(page_url)
	
	data = data_from_url(page_url)
	print data
	if level > 0:
		for (link, info) in data:
			crawl_page(base_url, link, level - 1)

crawl_page(directory_url, file_url, 1)
