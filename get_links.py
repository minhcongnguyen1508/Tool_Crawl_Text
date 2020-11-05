import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import urllib.request
import re
import codecs

# colorama.init()
# GREEN = colorama.Fore.GREEN
# GRAY = colorama.Fore.LIGHTBLACK_EX
# RESET = colorama.Fore.RESET

internal_urls = set()
external_urls = set()

total_urls_visited = 0


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            if href not in external_urls:
                # print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        # print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, max_urls=50):
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

def get_text(filename):
    sentences = []
    try:
        html = urllib.request.urlopen(filename).read()
        soup = BeautifulSoup(html)
        p_tags = soup.find_all('p')
        
        for p in p_tags[1:]:
            sent = p.text.split(' ')
            if '' in sent:
                while (sent.count('')): 
                    sent.remove('')
            sentence = ''
            for s in sent:
                sentence += s
                sentence += ' '
            sentences.append(sentence)
    except:
        print("Couldn't get text from file html. Please check get_text function")
        pass

    return sentences

def write2text(domain_name, file_out):
    f1 = codecs.open(f"{domain_name}_internal_links.txt", "r", "utf-8")
    f2 = codecs.open(file_out, 'w', 'utf-8')
    
    for link in f1:
        paragraph = get_text(link)
        for sent in paragraph:
            sent = sent.replace('\n', '')
            sent = sent.replace('\r', '')
            sent = sent.replace('\t', ' ')
            f2.write(sent + '\n')            
    
    f1.close()
    f2.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)

    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls

    # print(url)
    domain_links = codecs.open(url, "r", "utf-8")
    try:
        for i in domain_links:
            url = i.replace('\r', '')
            url = url.replace('\n', '')
            print(url.split(' '))
            if 'https://' in url:
                internal_urls = set()
                external_urls = set()
                total_urls_visited = 0
                crawl(url, max_urls=max_urls)
                print("[+] Total Internal links:", len(internal_urls))
                print("[+] Total External links:", len(external_urls))
                print("[+] Total URLs:", len(external_urls) + len(internal_urls))
                domain_name = urlparse(url).netloc
                # save the internal links to a file
                f1 = codecs.open(f"{domain_name}_internal_links.txt", "w", "utf-8")
                for internal_link in internal_urls:
                    f1.write(internal_link.strip() + '\n')
                    # save the external links to a file
                f2 = codecs.open(f"{domain_name}_external_links.txt", "w", "utf-8")
                for external_link in external_urls:
                    f2.write(external_link.strip() + '\n')
                f1.close()
                f2.close()
                # Get text
                write2text(domain_name, domain_name+'.mono_km')
            else:
                url = 'https://'+url
                internal_urls = set()
                external_urls = set()
                total_urls_visited = 0
                crawl(url, max_urls=max_urls)
                print("[+] Total Internal links:", len(internal_urls))
                print("[+] Total External links:", len(external_urls))
                print("[+] Total URLs:", len(external_urls) + len(internal_urls))
                domain_name = urlparse(url).netloc
                # save the internal links to a file
                f1 = codecs.open(f"{domain_name}_internal_links.txt", "w", "utf-8")
                for internal_link in internal_urls:
                    f1.write(internal_link.strip() + '\n')
                    # save the external links to a file
                f2 = codecs.open(f"{domain_name}_external_links.txt", "w", "utf-8")
                for external_link in external_urls:
                    f2.write(external_link.strip() + '\n')
                f1.close()
                f2.close()
                # Get text
                write2text(domain_name, domain_name+'.mono_km')
    except:
        print("Error get link html. Please check main function")
        pass
    