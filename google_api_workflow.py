from apiclient.discovery import build
import json
import config

##### Get Search Results via Google API #####
def get_json_google_api_search(search_term, api_key, engine_id, pages=2):
	"""
	Arguments:
		search_term - User inputted search term
		api_key - API given by Google
		engine_id - ID number of the search engine
		pages - How many pages of results we want to grab
	Description:
		So what we have here is the direct connection to Google search.
	This function will work all the time as long as we remain within
	our allotted API calls, which is 100 queries a day on a free
	subscription. The way works is that we use Google's Custom Search
	service to actually search Google for us, this would normally be used
	by websites to allow a user to search their own website through the power
	of Google.
		We first need to create a our connection to the API by inputting
	what API we wish to use, the version number, and our api_key. Afterwards
	we create a collection variable which ties in our connection to the API
	with our custom search engine (thats the 'service.cse()' part).
		Once that is completed we jump to actually getting the results. One
	should note that using this service we are limited to only 10 results per
	page, and thus, we need to make two API calls per search term. The first
	call for the first page and the second for the second page. I added in the
	'pages' argument with a default value of two just for extra flexibilty.
		We then append each page response into a list, and then dump and load
	the list to create a JSON compatiable collection of both pages. Not doing
	so will just throw out errors since JSON doesn't really work well with two
	dictionaries.
	"""
	service = build('customsearch', 'v1', developerKey=api_key)
	collection = service.cse()

	both_pages = []

	for page in range(pages):
		page = 1 + (page * 10)
		call_api = collection.list(
			q=search_term,
			num=10,
			start=page,
			cx=engine_id)

		json_response = call_api.execute()
		both_pages.append(json_response)

	# Unless I missed something somewhere, changing this will
	# throw a 'ValueError: Extra Data' error.
	both_pages_json_ok = json.loads(json.dumps(both_pages))
	return both_pages_json_ok


def grab_urls_from_json(json_data):
	"""
	Arguments:
		json_data - The JSON collection of all pages of search results
	Description:
		For each page of search results, extract all the links
	and return them within a list.
	"""
	urls = []

	for result in range(len(json_data)):
		for page in range(len(json_data[result]['items'])):
			urls.append(json_data[result]['items'][page]['link'])

	return urls

def grab_snippets_from_json(json_data):
	"""
	Arguments:
		json_data - The JSON collection of all pages of search results
	Description:
		For each page of search results, extract all the snippets
	and return them within a list.
	"""
	snippets = []

	for result in range(len(json_data)):
		for page in range(len(json_data[result]['items'])):
			snippets.append(json_data[result]['items'][page]['snippet'].replace('\n',''))

	return snippets

def grab_titles_from_json(json_data):
	"""
	Arguments:
		json_data - The JSON collection of all pages of search results
	Description:
		For each page of search results, extract all the titles
	and return them within a list.
	"""
	titles = []

	for result in range(len(json_data)):
		for page in range(len(json_data[result]['items'])):
			titles.append(json_data[result]['items'][page]['title'])

	return titles

def organise_results(urls, titles, snippets):
	"""
	Arguments:
		urls - a list of all urls found
		titles - a list of all titles found
		snippets - a list of all snippets found
	Description:
		Iterate over the length of urls, and create a more
	organised grouping of each search result.
	"""
	new_grouping = []
	try:
		for i in range(len(urls)):
			new_grouping.append([
				urls[i],
				titles[i],
				snippets[i]])
	except Exception as e:
		print(e)

	return new_grouping

def run_google_workflow(search_term):
	"""
	Arguments:
		search_term - User inputted search term
	Description:
		Main function used to begin the process of grabbing
	search results with the Google API. Will return found
	urls, titles, and snippets within a nested list.
	"""
	json_data = get_json_google_api_search(
		search_term,
		config.API_KEY,
		config.ENGINE_ID)

	urls = grab_urls_from_json(json_data)
	titles = grab_titles_from_json(json_data)
	snippets = grab_snippets_from_json(json_data)

	data = organise_results(urls, titles, snippets)
	return data