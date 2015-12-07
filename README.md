# nbc_project
### What It Does
- Given a search term, we will scrape the first twenty search results off Google. These results will then be inserted into a   MongoDB with the help of pymongo.
- User will be able to view various tidbits of each search result in their browser at their localhost.
- If there happens to be an issue with grabbing any results, the scraping will defer to grabbing the results with Google's Custom Search Engine, but this is limited to 50 search terms a day.

### Notes
- built using python3
- make sure you have the neccesary packages

### How To Use
- run python google_search_app.py
- enter your search term
- voila
