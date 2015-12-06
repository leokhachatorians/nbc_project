import requests
from lxml import html
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

##### Get Search Results via Scraping #####
def create_user_agent():
	"""
	Description:
		Create a random User-Agent which we will be passed
	to Google whenever we make a request.
	"""
	user_agent = UserAgent()
	return dict([('User-Agent', user_agent.random)])

def get_requests_response(search_term, user_agent):
	"""
	Arguments:
		search_term - User inputted search term
		user_agent - The User-Agent we wish to pass with our request 
	Description:
		All we do here is create the appropriate URL and pass in our
	User-Agent when we call for a 'GET' response with requests. Once
	we have the requests response, we return it.
	"""
	base_url = 'https://www.google.com/search?num=20&espvd=1&q={0}'.format(search_term)
	requests_response = requests.get(base_url, headers=user_agent)
	return requests_response

def create_lxml_tree(requests_response):
	"""
	Arguments:
		requests_response - A requests object
	Description:
		In order to limit the amount of requests we make,
	we create the actual lxml tree and return that.
	"""
	tree = html.fromstring(requests_response.text)
	return tree

def create_bs4_soup(requests_response):
	"""
	Arguments:
		requests_response: A requests object
	Description:
		Create a BeautifulSoup4 soup object and return it. Helps
	limit the amount of times we call for requests.
	"""
	bs4_soup = BeautifulSoup(requests_response.text, 'html.parser')
	return bs4_soup

def get_search_urls_lxml(lxml_tree):
	"""
	Arguments:
		lxml_tree - A lxml tree
	Description:
		Using our lxml tree, parse through it and grab the search links.
	Occasionally, there will be additional links nested witin a search result,
	causing there to be more than twenty links, so we just return the first twenty.
	"""
	search_result_urls = lxml_tree.xpath('//*[@class="r"]/a/@href')
	return search_result_urls[:20]

def get_search_titles_lxml(lxml_tree):
	"""
	Arguments:
		lxml_tree - A lxml tree
	Description:
		Using our lxml tree, parse through it and grab the search titles.
	Occasionally, there will be additional titles nested witin a search result,
	causing there to be more than twenty links, so we just return the first twenty.
	"""
	titles = lxml_tree.xpath('//*[@class="r"]/a/text()')
	return titles[:20]

def get_search_snippets_bs4(soup):
	"""
	Arguments:
		soup - a beautiful-soup object
	Description:
		Finds all search result snippets. Truncate the amount we return
	to twenty as some search results may have nested results.
	"""
	search_result_snippets = []
	for chunk in soup.find_all('span', class_='st'):
		search_result_snippets.append(chunk.text)

	return search_result_snippets[:20]

def clean_urls(urls):
	"""
	Arguments:
		urls - A list of URLs we wish to format
	Description:
		Sometimes when we attempt to crawl for links,
	the href's become quite muddled. While this isn't an
	exhaustive attempt are creating clean URLs, it has done
	a pretty good job in the occurences when the urls need
	to be trimmed.
	"""
	clean = []
	try:
		for url in urls:
			start_index = url.index('?url=')
			end_index = url.index('&rct')

			clean.append(url[start_index:end_index])
		return clean
	except Exception:
		return urls

def organise_results(urls, titles, snippets):
	"""
	Arguments:
		urls - a list of all urls found
		titles - a list of all titles found
		snippets - a list of all snippets found
	Description:
		Iterate over the length of urls, and create a more
	organised grouping of each search result.

		new_grouping[i][0] = urls
		new_grouping[i][1] = titles
		new_grouping[i][2] = snippets

	"""
	new_grouping = []
	for i in range(len(urls)):
		new_grouping.append([
			urls[i],
			titles[i],
			snippets[i]])

	return new_grouping

def run_web_scrape_workflow(search_term):
	"""
	Arguments:
		search_term - User inputted search term
	Description:
		Will run the process of grabbing search results through
	web scraping if there is an error/problem with the google workflow.
		Returns a nested list of urls, titles, and snippets.
	"""
	user_agent = create_user_agent()
	requests_response = get_requests_response(search_term, user_agent)
	soup = create_bs4_soup(requests_response)
	tree = create_lxml_tree(requests_response)

	urls = get_search_urls_lxml(tree)
	urls = clean_urls(urls)
	titles = get_search_titles_lxml(tree)
	snippets = get_search_snippets_bs4(soup)

	data = organise_results(urls, titles, snippets)

	return data