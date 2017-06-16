#-*- coding:utf8 -*-
import requests

def get_and_parse(url,url_query_string=None):
    resp = requests.get(url, headers=headers,params=url_query_string)
    parser = MYHTMLParser()
    parser.feed(resp.text)
    next_url,data = parser.result()
    parser.close()
    return next_url,data

from html.parser import HTMLParser
class MYHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.begin = 0  #开始抓取网页标题和url
        self.flag = 0 #开始抓取下一页url
        self.each_url = ''
        self.next_url = ''
        self.name_sum = ''
        self.content_dic = {}
    def handle_starttag(self, tag, attrs):
        if tag == 'h3':
            for attr in attrs :
                if attr[0] == 'class' : self.begin += 1
        if tag == 'a' and self.begin == 1 :
            self.begin = self.begin + 1
            for attr in attrs :
                if attr[0] == 'href' : 
                    self.each_url = attr[1]
        if tag == 'p' :
            for attr in attrs :
                if attr[0]=='id' and attr[1]=='page' : self.flag += 1
        if tag == 'a' and self.flag == 1 :
            self.flag += 1
            for attr in attrs :
                if attr[0] == 'href' : self.next_url = attr[1]
    def handle_endtag(self, tag):
        if tag == 'h3' and self.begin == 1 : self.begin -= 1
        if tag == 'a' and self.begin == 2 :
            self.begin -= 1
            self.content_dic[self.name_sum] = self.each_url
            self.name_sum = ''
        if tag == 'div' and self.flag == 1 : self.flag -= 1 
        if tag == 'a' and self.flag ==2 :
            self.flag -= 1
    def handle_data(self, data):
        if self.begin == 2 : self.name_sum += data
        if self.flag == 2 and data != '下一页' : self.next_url = '' 
    def result(self):
        return self.next_url,self.content_dic

def get_real_url(temp_url) :
    resp = requests.get(temp_url,headers=headers,allow_redirects=False)
    if resp.status_code == 302 : real_url = resp.headers['location']
    elif resp.status_code == 200 :real_url = resp.url
    else : return 'status_code not 302 or 200 :%s'% resp.status_code
    return real_url

def write_to_database(data,db_name) :
    pass
    
    

if __name__ == '__main__' :
    url_base = 'http://news.baidu.com'#word=%E7%A6%8F%E5%BB%BA%E9%82%AE%E6%94%BF
    query_string = {'word':'福建邮政'}
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    next_url,data = get_and_parse(url_base+'/ns?',query_string)
#    print(next_url)
    for title,temp_url in data.items() :
        data[title] = get_real_url(temp_url)
    print(data)
    import time 
    while next_url:
        next_url,data = get_and_parse(url_base+next_url)
        time.sleep(1)
        for title,temp_url in data.items() :
            data[title] = get_real_url(temp_url)
        print(data)
