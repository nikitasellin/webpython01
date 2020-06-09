#!/usr/bin/env python3

import argparse
import logging
from urllib.request import Request, urlopen
from urllib.parse import quote_plus, urlparse, parse_qs, urljoin, unquote_plus
from urllib.error import URLError
from bs4 import BeautifulSoup
import time


USER_AGENT = 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:76.0) \
Gecko/20100101 Firefox/76.0'
# Lapse to wait between HTTP requests.
PAUSE = 2.0


def get_args():
    arg_parser = argparse.ArgumentParser(
        description='Google (default)/Yahoo (optional) console search engine.')
    arg_parser.add_argument('-q', '--query', nargs='+',
                            type=str, help='Search query')
    arg_parser.add_argument(
        '-y', '--yahoo', action='store_true', help='Search with Yahoo')
    arg_parser.add_argument('-c', '--results-count', type=int, default=10)
    # @TODO: Add recursion.
    # arg_parser.add_argument('-r', '--recursion-depth', type=int, default=0)
    # @TODO: Add different output formats.
    # arg_parser.add_argument('-f', '--output-format',
    #                        default='t',
    #                        help='t - text(console), j - JSON, c - CSV')
    # arg_parser.add_argument('-o', '--output-dir', default='downloads')
    arg_parser.add_argument('-l', '--logfile', default=None)
    return arg_parser.parse_args()


def get_page(url, engine):
    user_agent = USER_AGENT
    request = Request(url)
    request.add_header('User-Agent', user_agent)
    response = urlopen(request)
    html = response.read()
    response.close()
    return html


def extract_links_from_page(html, engine):
    results = []
    hashes = set()
    soup = BeautifulSoup(html, 'html.parser')
    if engine == 'google':
        anchors = soup.find('div', id='search').find_all('a')
        next_page_url = soup.find('a', id='pnnext')['href']
        next_page_url = urljoin('https://www.google.com/', next_page_url)
    else:
        anchors = soup.find_all('a', class_='ac-algo fz-l ac-21th lh-24')
        next_page_url = soup.find('a', class_='next')['href']
    for a in anchors:
        link = a['href']
        # Exclude excess results.
        link = filter_result(link, engine)
        h = hash(link)
        if not link or h in hashes:
            continue
        hashes.add(h)
        text = clean_text(a)
        results.append((text, link))
    return results, next_page_url


def filter_result(link, engine):
    # Decode hidden URLs.
    if link.startswith('/url?'):
        o = urlparse(link, 'http')
        link = parse_qs(o.query)['q'][0]

    o = urlparse(link, 'http')
    if not o.netloc:
        return None
    # Exclude results like 'images.google.com', etc for Google search
    if engine == 'google' and engine in o.netloc:
        return None
    if engine == 'yahoo':
        # Trim 'search.yahoo.com' for Yahoo search
        link = link.split('RU=')[-1]
        link = unquote_plus(link.split('/RK=')[0])
    return link


def clean_text(anchor):
    try:
        # Some links for 'google.com'
        text = anchor.find('h3').text
    except AttributeError:
        # All other links
        text = anchor.text
    return text


def fetch_results(query, results_count, engine):
    total_found_count = 0
    links = []
    if engine == 'google':
        url = 'https://www.google.com/search?q={}'
    else:
        url = 'https://search.yahoo.com/search?p={}'
    query = ' '.join(query)
    query = quote_plus(query)
    url = url.format(query)
    while True:
        logging.info(f'Fetching url: "{url}".')
        html = get_page(url, engine)
        found_links, next_page_url = extract_links_from_page(html, engine)
        for link in found_links:
            links.append(link)
            total_found_count += 1
            if total_found_count >= results_count:
                return links
        url = next_page_url
        time.sleep(PAUSE)


def print_results(links):
    # @TODO: Add other formats. Plain text (console) by default.
    for link in links:
        print(f'{link[0]}: {link[1]}')
    return


def main():
    args = get_args()
    logging.basicConfig(filename=args.logfile,
                        level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    if not args.query:
        logging.error('Nothing to search. Use -q or --query option. Exit.')
        exit()
    engine = 'yahoo' if args.yahoo else 'google'
    try:
        links = fetch_results(args.query, args.results_count, engine)
    except URLError:
        logging.error('Check Internet connection. Exit.')
        exit()
    print_results(links)
    logging.info(f'Total links count: {len(links)}. Exit.')
    exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info('Interrupted by user.')
    except Exception as e:
        logging.exception('Unexpected exception: %s', e)
