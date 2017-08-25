import urllib
import re
import time
from threading import Thread
import MySQLdb
import mechanize
import readability
from bs4 import BeautifulSoup
from readability.readability import Document
import urlparse


def scraper(root,steps):
    urls = [root]
    visited = [root]
    counter = 0
    scraped=[]
    while counter < steps:
        step_url = scrapeStep(urls,scraped)
        urls = []
        for u in step_url:
            if u not in visited and urlparse.urlparse(root).hostname in u:
                urls.append(u)
                visited.append(u)
        counter+=1
    return visited

def scrapeStep(root,scraped):
    result_urls = []
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]

    for url in root:
        if url not in scraped:
            try:
                br.open(url)
                for link in br.links():
                    newurl = urlparse.urljoin(link.base_url,link.url)
                    result_urls.append(newurl)
                scraped.append(url)
            except:
                error= "error"
    return result_urls
