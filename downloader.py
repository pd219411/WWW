import urllib
import urlparse
#from BeautifulSoup import *
from bs4 import BeautifulSoup

#params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
directory_url = "http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/"

file_url = "index.htm"
#file_url = "020100.htm"
#file_url = "http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/P/020000/020702_1.html"

def soup_html_from_url(url):
	stream = urllib.urlopen(url)
	html = stream.read()
	stream.close()
	return BeautifulSoup(html)

def extract_link_from_row(soup_row):
	return soup_row.find("a", {"class" : "link1"}).get("href")

def extract_info_from_row(soup_row):
	cells = soup_row.findAll("td")
	name = cells[1].string
	votes = cells[2].string
	return (name, votes)
	
def extract_data_from_html(soup_html):
	table = soup_html.find("table", {"id" : "s0"})
	if table is None:
		return None

	body = table.find_all("tbody")[0]
	rows = body.find_all("tr", {})

	data_list = []

	for row in rows:
		data_list.append((extract_link_from_row(row), extract_info_from_row(row)))

	return data_list

def data_from_url(url):
	return extract_data_from_html(soup_html_from_url(url))

def crawl_page(base_url, file_url, level, location):
	separator = "@"
	page_url = urlparse.urljoin(directory_url, file_url)

	data = data_from_url(page_url)
	if data is None:
		print location
	else:
		for (link, info) in data:
			(name, votes) = info
			#location_subzone = location + ", " + name + ", " + link
			location_subzone = location + separator + name
			crawl_page(base_url, link, level + 1, location_subzone)

if __name__ == "__main__":
	crawl_page(directory_url, file_url, 0, "Polska")
