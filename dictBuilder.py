#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    *.py: Description of what * does.
    Last Modified:Wed Dec 19 06:05:10 2012
"""

from wikiParser import wikiParser
from wikiApi import wikiApi
import json
import nltk
from nltk.collocations import *
import sys
from unidecode import unidecode
import os
import re
from BeautifulSoup import BeautifulSoup


__author__ = "Sathappan Muthiah"
__email__ = "sathap1@vt.edu"
__version__ = "0.0.1"

bigram_measures = nltk.collocations.BigramAssocMeasures()
htmltags = [k.strip().lower() for k in open('htmltags.txt')]

def getPageViews(titles, lang, dir):
    for k in titles:
        views = wikiApi.getYearlyViews(k, lang, ['2012', '2011', '2010', '2009', '2008', '2007', '2006'])
        wikiApi.convertToWeeklyViews(views, '%s/%s' % (query, unidecode(k.replace('/', ''))))
    return


def collocations(query, lang):
    langMap = {'es': 'Spanish', 'en': 'English'}
    stemmer = nltk.stem.snowball.SnowballStemmer(langMap[lang].lower())
    j = wikiApi.get_article(query, lang)
    wordDict = {}
    corpus = ''
    for page in j:
        wikitext = wikiParser(j[page]['content']).text
        bfSoup = ' '.join(BeautifulSoup(wikitext).findAll(text=True))
        corpus = corpus + " " + bfSoup
    tokens = nltk.wordpunct_tokenize(corpus)
    assert(tokens)
    finder  = BigramCollocationFinder.from_words(tokens, window_size=20)
    finder.apply_freq_filter(4)
    ignored_words = nltk.corpus.stopwords.words('english')
    ignored_words.extend(htmltags)
    finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
    a = finder.nbest(bigram_measures.likelihood_ratio, 500)
    final = []
    for k in a:
        if k in final or (k[1], k[0]) in final:
            continue
        final.append(k)
    return final

def main(query, lang):
    langMap = {'es': 'Spanish', 'en': 'English'}
    stemmer = nltk.stem.snowball.SnowballStemmer(langMap[lang].lower())
    j = wikiApi.get_article(query, lang)
    wordDict = {}
    for page in j:
        t = wikiParser(j[page]['content'])
        for header in t.headers:
            try:
                stemmedHeader = stemmer.stem(header)
            except Exception, e:
                print str(e)
                header = unidecode(header)
                stemmedHeader = stemmer.stem(header)
            if stemmedHeader in wordDict:
                wordDict[stemmedHeader]['count'] = 1
            else:
                wordDict[stemmedHeader] = {'count': 1, 'form': stemmedHeader}
        text = t.text
        print type(text)
        tokens = [k.split('|')[0] for k in nltk.PunktWordTokenizer().tokenize(text)
                  if re.match('[a-zA-Z]', k)]
        words = [w.lower() for w in tokens if w.encode('utf-8').lower() not in
                 nltk.corpus.stopwords.words(langMap[lang].lower())]
        print len(words)
        for w in words:
            try:
                st = stemmer.stem(w)
            except Exception, e:
                st = stemmer.stem(unidecode(w))
                w = unidecode(w)
                continue
            if st in wordDict:
                wordDict[st]['count'] += 1
            else:
                wordDict[st] = {'count': 1, 'form': w}
        for w in t.links:
            try:
                st = stemmer.stem(w[0])
            except Exception, e:
                print str(e)
                w[0] = unidecode(w[0])
                st = stemmer.stem(unidecode(w[0]))
            if st in wordDict:
                wordDict[st]['count'] += 1
            else:
                wordDict[st] = {'count': 1, 'form': w[0]}
    print len(wordDict)
    return wordDict, j


if __name__ == "__main__":
    query = sys.argv[1]
    lang = sys.argv[2]
    #os.mkdir(query)
    wordDict = collocations(query, lang)
    out = open("%s-collocations.txt" % query, 'w')
    #getPageViews(j.keys(), lang, query)
    out.write(str(wordDict))
    out.close()
