import requests
from bs4 import BeautifulSoup
import random

def scrape(url, proxy, domain):
    """
    Scrape search results from the specified URL for a given domain.

    Args:
        url (str): The URL to scrape.
        proxy (dict): Dictionary containing proxy information.
        domain (str): The domain for which to scrape search results.

    Returns:
        list: A list of dictionaries containing scraped search results.
    """
    try:
        response = requests.get(url, proxies=proxy)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            web_div = soup.find('div', id='web')
            if web_div:
                results = []
                li_elements = web_div.find_all('li')
                for li in li_elements:
                    anchor = li.find('a')
                    if anchor:
                        link = anchor.get('href')
                        title = anchor.get('aria-label', domain.upper())
                        span = anchor.find('span')
                        extra_title = span.text if span else domain.upper()
                        result_data = {
                            'link': link,
                            'title': title,
                            'extra_title': extra_title
                        }
                        results.append(result_data)
                return results
        else:
            print(f"Failed to retrieve data from {url}")
            return None
    except Exception as e:
        print(f"Error occurred while scraping {url}: {str(e)}")
        return None


def search(query, domains, num_results=1, proxies=None):
    """
    Search for the specified query in the specified domains and retrieve search results.

    Args:
        query (str): The search query.
        domains (list): List of domains to search within.
        num_results_per_domain (int): Number of search results to retrieve per domain. Default is 1.
        proxies (list): List of dictionaries containing proxy information. Default is None.

    Returns:
        list: A list of dictionaries containing search results.
    """
    results = []
    for domain in domains:
        current_result_count = 0 
        domain_results = [] 
        
        while current_result_count < num_results:
            proxy = None
            if proxies:
                proxy_info = random.choice(proxies)
                proxy_url = f"{proxy_info['protocol']}://{proxy_info['ip']}:{proxy_info['port']}"
                proxy = {proxy_info['protocol']: proxy_url}
            
            b = len(domain_results) + 1
            
            url = f"https://search.yahoo.com/search;_ylt=?fr=yfp-t&fr2=p%3Afp%2Cm%3Asb&ei=UTF-8&fp=1&p={query}+site%3Awww.{domain}.com&b={b}&pz=7&bct=0&xargs=0"
            
            page_results = scrape(url, proxy, domain)
            if page_results:
                domain_results.extend(page_results)
                current_result_count += len(page_results)
        
        results.extend(domain_results[:num_results])
    
    return results
