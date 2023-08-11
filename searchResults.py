# # searchResults.py - open several search results


# import requests, sys, bs4, webbrowser

# def main():
#     print('Searching...')   # display text while downloading the search result page
#     res = requests.get('https://google.com/search?q=' 'https://pypi.org/search/q='
#                     + ' '.join(sys.argv[1:]))
#     res.raise_for_status()

#     # Retrieve top search links
#     soup = bs4.BeautifulSoup(res.text, 'html.parser')

#     # Open Browser tabs for retrieved search links
#     linkElems = soup.select('.package-snippet')
#     numOpen = min(5, len(linkElems))

#     for i in range(numOpen):
#         urlToOpen = 'https://pypi.org' + linkElems[i].get('href')
#         print('Opening', urlToOpen)
#         webbrowser.open(urlToOpen)

import webbrowser, urllib.parse

def open_search_results(query):
    query = urllib.parse.quote(query)  #Url encode the search query
    search_url = f"https://www.google.com/search?q={query}"

    # Open the search URL in the default browser
    webbrowser.open(search_url)

    # Open the top 10 search results in new tabs
    for i in range (2,12):
        result_url = f"https://www.google.com/search?q={query}&start={i}O"
        webbrowser.open_new_tab(result_url)

searchQuery = input('Enter your search...')
open_search_results(searchQuery)