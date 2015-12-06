import requests
import json
import config

class JsonifyMe():
	"""
	Description:
		JSON Serializer, creates a class which recursively
	creates a JSON output of the class. Thanks to Onur Yildirim for
	coming up with it.
	http://stackoverflow.com/questions/3768895/python-how-to-make-a-class-json-serializable
	"""
	def _try(self, o):
		"""
		Description:
			When the object given does not contain __dict__,
		return it as a string.
		"""
		try: 
			return o.__dict__ 
		except:
			return str(o)

	def to_JSON(self):
		"""
		Description:
			Function which does the actual JSON serilizaion of the class.
		"""
		return json.dumps(self, 
			default=lambda o: self._try(o), 
			sort_keys=True, 
			indent=0, 
			separators=(',',':')).replace('\n', '')

def get_requests_response(url):
	"""
	Arguments:
		url - the url we wish to visit
	Description:
		Given a url, call requests to create and return a response object
	"""
	requests_response = requests.get(url)
	return requests_response

def get_headers(requests_response):
	"""
	Arguments:
		requests_response - A response object created by requests
	Description:
		Return the sites headers.
	"""
	try:
		return requests_response.headers
	except AttributeError:
		return None

def get_cookies(requests_response):
	"""
	Arguments:
		requests_response - A response object created by requests
	Description:
		Return any cookies if available.
	"""
	try:
		return requests_response.cookies
	except AttributeError:
		return None

def check_time_elapsed(requests_response):
	"""
	Arguments:
		requests_response - A response object created by requests
	Description:
		Return the amount of time it took from the request to the response
	"""
	try:
		return requests_response.elapsed
	except AttributeError:
		return None

def visit_each_site(data):
	"""
	Arguments:
		data - The combination of urls, titles, and snippets of each search result
			taken from Google
	Description:
		Iterate over each url contained within data and use requests to visit each page
	and return all data as needed.

	data[i][0] = the url of the search result
	data[i][1] = the title of the search result
	data[i][2] = the snippet of the search result
	"""
	headers = []
	cookies = []
	elapsed_time = []

	for search_result in range(len(data)):
		print('Visiting Search Result: {0}. {1}'.format(search_result + 1, data[search_result][0]))
		requests_response = get_requests_response(data[search_result][0])
		headers.append(get_headers(requests_response))
		cookies.append(get_cookies(requests_response))
		elapsed_time.append(check_time_elapsed(requests_response))

	json_dict = package_into_json(headers, cookies, elapsed_time, data)

	return json_dict

def package_into_json(headers, cookies, elapsed_time, data):
	"""
	Arguments:
		headers - List containing all headers for each site
		cookies - List containing all cookies for each site
		elapsed_time - List containing all the elapsed times of each site vist
		data - The combination of urls, titles, and snippets of each search result
			taken from Google
	Description:
		Create a dictionary with a key of 'items' with a list as a value which will
	house the contents of each of the websites we visited.
		We use the JsonifyMe class, kindly created by Onur Yildirim,
	to easily create a JSON ok dictionary of each websites contents.

	It's packaged as such:
		{
			"items": 
			[
				{
					'search_result':{
						'url':'the url',
						'snippet':'the snippet',
						'title':'the title',
						'headers':'the headers'
						'cookkies':'cookies',
						'elapsed_time':'the elapsed time'
					},
					'search_result':{
					....
					},
					'search_result':{
					....
					}
				}
			]
		}
	"""
	json_dict = {'items':[]}

	for i in range(len(headers)):
		result = JsonifyMe()
		result.url = data[i][0]
		result.title = data[i][1]
		result.snippet = data[i][2]
		result.headers = headers[i]
		result.cookies = cookies[i]
		result.elapsed_time = elapsed_time[i]
		json_dict['items'].append({'search_result':{}})
		json_dict['items'][i]['search_result'] = json.loads(result.to_JSON())

	return json_dict

def write_json_to_disk(json_dict):
	"""
	Arguments:
		json_dict = A JSON ok dictionary
	Description:
	 	Create and write a .json file to the specified output.
	"""
	with open(config.JSON_OUTPUT_PATH, 'w') as f:
		json.dump(json_dict, f)

def run_visit_sites_workflow(data):
	"""
	Arguments:
		data - List containing all urls, titles, and snippets of the sites we
			wish to vist
	Description:
		Function which runs the process of actaully visiting each site
	and extracting the needed data. We finish off by creating and writing
	a .json file which will then be used by the local server to pull up and
	display the data in a user-friendly manner.
	"""
	json_dict = visit_each_site(data)
	write_json_to_disk(json_dict)