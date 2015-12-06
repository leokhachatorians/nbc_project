from google_api_workflow import run_google_workflow
from web_scrape_workflow import run_web_scrape_workflow
from visit_sites_workflow import run_visit_sites_workflow
from database import insert_in_db
from local_server_workflow import run_local_server_workflow
import config

if __name__ == '__main__':
	search_term = input('What would you like to search?: ')
	try:
		print('Starting Web Scraping')
		data = run_web_scrape_workflow(search_term)
	except Exception as e:
		print('Switching over to Google API due to error:<{0}>'.format(e))
		data = run_google_workflow(search_term)
	finally:
		run_visit_sites_workflow(data)
		insert_in_db(config.JSON_OUTPUT_PATH)
		run_local_server_workflow()

	print('Finished')
