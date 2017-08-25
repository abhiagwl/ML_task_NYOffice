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


class MultiScrape(object):
    visited = []
    urls = []
    glob_visited = []
    depth = 0
    counter = 0
    threadlist = []
    root = ""

    def __init__(self, url, depth):
        self.glob_visited.append(url)
        self.depth = depth
        self.root = url
   
    def run(self):
        while self.counter < self.depth:
            for w in self.glob_visited:
                if w not in self.visited:
                    self.visited.append(w)
                    self.urls.append(w)
            self.glob_visited = []       
            for r in self.urls:
                try: 
                    t = Thread(target=self.scrapeStep, args=(r,))
                    self.threadlist.append(t)
                    t.start()            
                except:
                    nnn = True 
            for g in self.threadlist:
                g.join() 
            self.counter+=1
        return self.visited  

    def scrapeStep(self,root):
        result_urls = []
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]
        try:
            br.open(root)
            for link in br.links():
                newurl =  urlparse.urljoin(link.base_url,link.url)
                if urlparse.urlparse(link.base_url).hostname.replace("www.","") in self.root:
                    result_urls.append(newurl)   
        except:
            err = True     
        for res in result_urls:
            self.glob_visited.append(res)
            
    






def getReadableArticle(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Firefox')]

    html = br.open(url).read()

    readable_article = Document(html).summary()
    readable_title = Document(html).short_title()

    soup = BeautifulSoup(readable_article)

    final_article = soup.text

    links = soup.findAll('img', src=True)

    title_article = []
    title_article.append(final_article)
    title_article.append(readable_title)
    return title_article

    



def dungalo(urls):
    article_text =getReadableArticle(urls)[0]
    d[urls] = article_text

        

def getMultiHtml(urlsList,steps):

    for urls1 in urlsList:
        try:
            t = Thread(target=scraper, args=(urls1,steps,))
            threadlist.append(t)
            t.start()            
        except:
            nnn = True

    for g in threadlist:
        g.join()