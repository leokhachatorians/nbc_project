from flask import Flask, render_template, jsonify, url_for
from multiprocessing import Process
import config
import json
import webbrowser

app = Flask(__name__)

def run_local_server_workflow():
	"""
	Description:
		We initiate and run the Flask local server. Note however
	to leave 'app.run(debug=False)' as it is. Doing so will cause
	the Flask reloader to reload our google_search_app.py script,
	causing us to start over again.
	"""
	print('Starting local server')
	app.run(debug=False)

def read_json_file(json_path):
	"""
	Arguments:
		json_path - The path where our .json file is located
	Description:
		Read the .json file and return it for further use
	"""
	with open(json_path, 'r') as f:
		parsed = json.load(f)
	return parsed

@app.route('/')
def index():
	"""
	Description:
		Main index page
	"""
	return render_template('index.html')

@app.route('/regular_output')
def regular_output():
	"""
	Description:
		Display the contents within 'json_file' in an
	easy to read format.
	"""
	json_file = read_json_file(config.JSON_OUTPUT_PATH)
	results = []

	# Loop through all of the search results within 'items',
	# and assign it to a dictionary value. This makes it easier
	# for us when we have to render it in the template; we can
	# just loop through results and output each key's value
	for i in range(len(json_file['items'])):
		results.append(
			dict(
				url = json_file['items'][i]['search_result']['url'],
				title = json_file['items'][i]['search_result']['title'],
				snippet = json_file['items'][i]['search_result']['snippet'],
				cookie = json_file['items'][i]['search_result']['cookies'],
				header = json_file['items'][i]['search_result']['headers'],
				elapsed = json_file['items'][i]['search_result']['elapsed_time']
				)
			)

	return render_template('search_results_regular.html',
		results=results)

@app.route('/json_output')
def json_output():
	"""
	Description:
		Use flask.jsonify to easily create and display our .json file's
	contents
	"""
	json_file = read_json_file(config.JSON_OUTPUT_PATH)
	return jsonify(**json_file)