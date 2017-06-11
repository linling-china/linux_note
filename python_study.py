#-*- coding:utf8 -*-

import requests

url = 'http://www.baidu.com/s?'
url_query_string = {'wd':'intitle:""-(管理)'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
def spyder(url,headers,url_query_strint=None):
    resp = requests.get(url, headers=headers,params=url_query_string)
#print(resp.text)

from html.parser import HTMLParser
class MYHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.begin = 0
        self.count = 0
    def handle_starttag(self, tag, attrs):
        if tag == 'h3':
            self.begin = self.begin + 1
        if tag == 'a' and self.begin == 1 :
            self.begin = self.begin + 1
            print("Start tag:", tag)
        if self.begin == 2:  
            for attr in attrs:#print("     attr:", attr)
                if attr[0] == 'href':print(attr[1])
    def handle_endtag(self, tag):
        if tag == 'h3':
            self.begin = 0
        if tag == 'a' and self.begin == 2 :
           print("End tag  :", tag)
    def handle_data(self, data):
        if self.begin == 2:print("Data     :", data)
    def result(self):
        return next_url,data_dic

if __name__ == __main__ :
    url = 'http://www.baidu.com/s?'
    url_query_string = {'wd':'intitle:""-(管理)'}
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    while url:
        resp = requests.get(url, headers=headers,params=url_query_string)    
        parser = MYHTMLParser()
        parser.feed(resp.text)
        url,data = parser.result()
