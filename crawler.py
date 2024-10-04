import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse



def assembly_headers(browser="chrome", user_agent=None, accept=None, accept_language="en-US,en;q=0.9", content_type=None):
    
    default_headers = {
        "chrome": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8',
            'Accept-Language': accept_language,
            'Content-Type': content_type or 'text/html; charset=UTF-8'
        },
        "firefox": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8',
            'Accept-Language': accept_language,
            'Content-Type': content_type or 'text/html; charset=UTF-8'
        }
    }

    headers = default_headers.get(browser.lower(), default_headers["chrome"])

    if user_agent:
        headers['User-Agent'] = user_agent
    if accept:
        headers['Accept'] = accept

    return headers


def connection(url, headers, method="GET"):
    if method == 'GET':
        response = requests.get(url=url, headers=headers)
        return response


def req_parser(url, domain=None, root_url=None): 
    response = connection(url=url, headers=assembly_headers())
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=True)
    hrefs = set(link['href'] for link in links)

    relative_urls = []
    absolute_urls = []

    for item in hrefs:
        if not item.startswith(('http://', 'https://')):
            full_url = urljoin(root_url, item)
            relative_urls.append(full_url)
        else:
            absolute_urls.append(item)

    domain_urls = []

    if domain is not None:
        for item in absolute_urls:
            if domain in item:
                domain_urls.append(item)

    result = {
        "response_time": response.elapsed.total_seconds(),
        "status": response.status_code,
        "url": response.url,
    }
    
    return domain_urls, relative_urls, result


def process_url(item, domain, sleeptime=None, root_url=None):
    domain_urls, relative_urls, result = req_parser(url=item, domain=domain, root_url=root_url)

    with open("results.txt", "a") as f:
        print(result)
        f.write(f'{result["response_time"]}; {result["status"]}; {result["url"]}\n')

    if sleeptime is not None:
        time.sleep(sleeptime)

    return domain_urls + relative_urls


def crawl(url, domain=None, sleeptime=None, root_url=None):
    all_urls = set([url])
    crawled = set()

    if root_url is None:
        root_url = url

    with ThreadPoolExecutor(max_workers=10) as executor:
        while all_urls - crawled:
            futures = {executor.submit(process_url, item, domain, sleeptime, root_url): item for item in all_urls if item not in crawled}

            for future in as_completed(futures):
                try:
                    new_urls = future.result()
                    all_urls.update(new_urls) 
                except Exception as exc:
                    print(f"Gerou exceção: {exc}")
                finally:
                    crawled.add(futures[future])

if __name__ == "__main__":
    url = input("Digite a URL: ")
    domain = input("Digite o dominio: ")
    parser = argparse.ArgumentParser(description="Web Crawler com threading.")
    parser.add_argument("-u", "--url", help="URL inicial para iniciar o crawling. ")
    parser.add_argument("-d", "--domain", help="Domínio para restringir o crawling.", default=None)
    parser.add_argument("-s", "--sleeptime", help="Tempo de espera entre requisições.", type=float, default=None)

    args = parser.parse_args()

    crawl(url, domain, args.sleeptime, root_url=url)