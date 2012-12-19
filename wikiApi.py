# -*- coding:utf-8 -*-
import pycurl
import requests
import json
import urllib
import sys
import cStringIO
from datetime import datetime, timedelta
from wikiParser import wikiParser


class wikiApi:
    @staticmethod
    def request(url):
        r = requests.get(url)
        return r.text

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
            reqStr = wikiApi.request(content_url + urllib.urlencode(page_title))
            content = json.loads(reqStr.decode('utf-8'))
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
        reqStr = wikiApi.request(url)
        content = json.loads(reqStr)
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
        reqStr = wikiApi.request(url)
        return json.loads(reqStr)

    @staticmethod
    def getYearlyViews(title, wikiLang='es', years=None):
        if years is None:
            return {}
        months = ['%02d' % i for i in range(1, 12)]
        baseUrl = 'http://stats.grok.se/json/'
        views = {'project': 'en', 'title': title, 'ranks': {}, 'daily_views': {}}
        for year in years:
            for month in months:
                url = '%s/%s/%s/%s' % (baseUrl, wikiLang.encode('utf-8'),
                                       year.encode('utf-8') + month, title.encode('utf-8'))
                reqStr = wikiApi.request(url)
                j = json.loads(reqStr)
                views['daily_views'].update(j['daily_views'])
                views['ranks'][month] = j['rank']
        return views

    @staticmethod
    def convertToWeeklyViews(views, outFile):
        weeklyViews = {}
        out = open(outFile, 'w')
        for day in views['daily_views']:
            viewCnt = views['daily_views'][day]
            try:
                dObj = datetime.strptime(day, '%Y-%m-%d')
                delta_days = timedelta(days=dObj.isoweekday(), weeks=0)
                firstDayOfWeek = (dObj - delta_days).strftime('%Y-%m-%d')
            except ValueError:
                continue
            if firstDayOfWeek in weeklyViews:
                weeklyViews[firstDayOfWeek] += viewCnt
            else:
                weeklyViews[firstDayOfWeek] = viewCnt

        sortedKeys = weeklyViews.keys()
        sortedKeys.sort()
        for k in sortedKeys:
            out.write("%s,%s\n" % (k.replace('/', '_'), weeklyViews[k]))
        out.close()

        return weeklyViews

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Usage: Wiki "query_string"'
        print 'Note: use "-" for negation. Example "cold - flu"'
        exit()
    query = sys.argv[1]
    lang = sys.argv[2]
    print query
    j = wikiApi.get_article(query, lang)
    print j.keys()
    a = wikiParser(j['Human flu']['content'])
    out = open('wikiMarkup.example', 'w')
    out.write(j["Human flu"]["content"].encode('utf-8'))
    out.close()
    exit()

    print "headers %s", a.headers
    raw_input()
    print "links %s", a.links
    raw_input()
    print "websites %s", a.websiteRef
    raw_input()
    print "sections %s", a.sections
    raw_input()
    print "links %s", a.links
    raw_input()
    print "references %s", a.text.encode('utf-8')
    raw_input('here')
    for k in j.keys():
        #wikiApi.get_category(['Influenza'], lang)
        wikiApi.get_views(k, 'en', '201102')
        a = wikiApi.getYearlyViews(k, lang, ['2006', '2007', '2008', '2009', '2010', '2011', '2012'])
        wikiApi.convertToWeeklyViews(a, 'views/%s' % k)
    #print wikiApi.convertToWeeklyViews(a, 'weeklyQueries.txt')
