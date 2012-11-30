# -*- coding:utf-8 -*-
import pycurl
import json
import urllib
import sys
import cStringIO


class wikiApi:
    @staticmethod
    def query(url, buf):
        #function to query media wiki api .
        #raises pycurl.error
        curlHandle = pycurl.Curl()
        curlHandle.setopt(curlHandle.URL, url)
        curlHandle.setopt(curlHandle.TIMEOUT, 10)
        curlHandle.setopt(curlHandle.WRITEFUNCTION, buf.write)
        curlHandle.perform()

    @staticmethod
    def get_article(query_string, wikiLang='en'):
        buf = cStringIO.StringIO()
        search_param = urllib.urlencode({"srsearch": query_string})
        search_url = "http://{}.wikipedia.org/w/api.php?action=query&list=search&format=json&srwhat=text&srprop=wordcount%7Csectiontitle&srlimit=50&{}".format(wikiLang, search_param)
        wikiApi.query(search_url, buf)
        j = json.loads(buf.getvalue())
        page_contents = {}
        content_url = "http://{}.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&".format(wikiLang)
        for page in j['query']['search']:
            title = page['title']
            page_title = {"titles": title.encode('utf-8')}
            buf = cStringIO.StringIO()
            wikiApi.query(content_url + urllib.urlencode(page_title), buf)
            content = json.loads(buf.getvalue().decode('utf-8'))
            page_contents[title] = {}
            page_id = content["query"]["pages"].keys()[0]
            page_contents[title]['id'] = page_id
            page_contents[title]['content'] = content['query']['pages'][page_id]['revisions'][0]['*']
        return page_contents

    @staticmethod
    def get_category(titles, wikiLang='en'):
        '''titles is an array of titles'''
        titleStr = '|'.join(titles)
        url = "http://{}.wikipedia.org/w/api.php?action=query&prop=categories&format=json&clprop=timestamp&clshow=!hidden&cllimit=500&cldir=ascending&{}".format(wikiLang, urllib.urlencode({'titles': titleStr}))
        buf = cStringIO.StringIO()
        wikiApi.query(url, buf)
        content = json.loads(buf.getvalue())
        category_names = {}
        pages = content['query']['pages']
        for page in pages:
            category_names[pages[page]['title']] = [k['title'] for k in pages[page]['categories']]
        return category_names

    @staticmethod
    def get_views(title, wikiLang='en', period=None):
        '''title: String
           period: String of the form YYYYMM
        '''
        if period is None:
            period = 'latest90'
        url = 'http://stats.grok.se/json/%s/%s/%s' % (wikiLang.encode('utf-8'), period.encode('utf-8'), title.encode('utf-8'))
        buf = cStringIO.StringIO()
        wikiApi.query(url, buf)
        return json.loads(buf.getvalue())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Usage: Wiki "query_string"'
        print 'Note: use "-" for negation. Example "cold - flu"'
        exit()
    query = sys.argv[1]
    j = wikiApi.get_article(query, 'en')
    print j.keys()
    wikiApi.get_category(['Influenza'], 'en')
    wikiApi.get_views(u'Russian flu', 'en', '201102')
