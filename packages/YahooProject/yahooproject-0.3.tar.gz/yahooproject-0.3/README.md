# SocialCrawler

SocialCrawler is a Python package designed to scrape search results from Yahoo Search for specific domains. It utilizes requests and BeautifulSoup to extract search results from Yahoo Search pages.

## Installation

You can install SocialCrawler via pip:

```bash
pip install socialCrawler
```

## Usage

```python
from socialCrawler import search

# Define your search query
query = "python tutorials"

# Define the list of domains to search within
domains = ["stackoverflow", "instagram"]

# Define the number of search results to retrieve per domain
num_results = 5

# Perform the search
results = search(query, domains, num_results)

# Print the search results
for result in results:
    print(result)
```

## Functions

### search(query, domains, num_results=1, proxies=None)

Search for the specified query in the specified domains and retrieve search results.

- `query (str)`: The search query.
- `domains (list)`: List of domains to search within.
- `num_results (int)`: Number of search results to retrieve per domain. Default is 1.
- `proxies (list)`: List of dictionaries containing proxy information. Default is None.

Returns:
- `list`: A list of dictionaries containing search results.

### scrape(url, proxy, domain)

Scrape search results from the specified URL for a given domain.

- `url (str)`: The URL to scrape.
- `proxy (dict)`: Dictionary containing proxy information.
- `domain (str)`: The domain for which to scrape search results.

Returns:
- `list`: A list of dictionaries containing scraped search results.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.