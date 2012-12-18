import re

HLINK_RE = re.compile('\[\[([^\]]+)\]\]', re.UNICODE | re.MULTILINE)
REF_LINK_RE = re.compile('\<ref\>([^\<]+)\</ref\>', re.UNICODE | re.MULTILINE)
REF_TEXT_RE = re.compile('\{\{([^\}]+)\}\}', re.UNICODE | re.MULTILINE)
WEBSITE_RE = re.compile('(http://[\w+\-:\.]*/[^\s]*)', re.UNICODE | re.MULTILINE)
SECTION_RE = re.compile('^=+([^=]+)=+\s*$', re.UNICODE | re.MULTILINE)
HEADINGS_RE = re.compile('^;(.*)\s*$', re.UNICODE | re.MULTILINE)
CATEGORY_RE = re.compile('Category:(.*)', re.UNICODE | re.MULTILINE)
HEAD_RE = re.compile('^(;)', re.UNICODE | re.MULTILINE)
SUBSECTION_RE = re.compile('^(:)', re.UNICODE | re.MULTILINE)
REF_BEGIN_RE = re.compile('(\<ref[^\>]*\>)', re.UNICODE | re.MULTILINE)
REF_END_RE = re.compile('(\</ref\>)', re.UNICODE | re.MULTILINE)
ITALICS_RE = re.compile('\'{2,4}([^\']+)\'{2,4}', re.UNICODE | re.MULTILINE)
BOLD_QUOTES_RE = re.compile('(\'{2,4})', re.UNICODE | re.MULTILINE)


class wikiParser(object):
    def __init__(self, text):
        self.text = self.getText(text)
        self.category = []
        self.links = self.getWikiLinks(text)
        self.references = self.getReferences(text)
        self.websiteRef = self.getWebsites(text)
        self.sections = self.getSections(text)
        self.headers = self.getHeaders(text)
        self.bold = self.getBoldWords(text)

    def getBoldWords(self, text):
        return re.findall(ITALICS_RE, text)

    def getWikiLinks(self, text):
        links = re.findall(HLINK_RE, text)
        linkList = []
        for l in links:
            category = re.findall(CATEGORY_RE, l)
            if category:
                self.category.append(category)
            parts = l.split('|')
            if len(parts) > 1:
                linkTuple = (parts[0].strip(), parts[1].strip())
            else:
                linkTuple = (parts[0].strip(), parts[0].strip())
            linkList.append(linkTuple)
        return linkList

    def getReferences(self, text):
        return {'linksRef': re.findall(REF_LINK_RE, text),
                'textRef': re.findall(REF_TEXT_RE, text)}

    def getWebsites(self, text):
        return re.findall(WEBSITE_RE, text)

    def getSections(self, text):
        return re.findall(SECTION_RE, text)

    def getHeaders(self, text):
        return re.findall(HEADINGS_RE, text)

    def getText(self, text):
        plainText = re.sub(REF_TEXT_RE, '', text)
        plainText = re.sub('=+', '', plainText)
        plainText = re.sub('\[|\]', '', plainText)
        plainText = re.sub(REF_LINK_RE, '', plainText)
        plainText = re.sub(HEAD_RE, '', plainText)
        plainText = re.sub(SUBSECTION_RE, '', plainText)
        plainText = re.sub(REF_BEGIN_RE, '', plainText)
        plainText = re.sub(REF_END_RE, '', plainText)
        plainText = re.sub(BOLD_QUOTES_RE, '', plainText)
        return plainText

if __name__ == "__main__":
    wikiText = open('wikiMarkup.example')
    a = wikiParser(wikiText.read())
    out = open('parsedWiki', 'w')
    out.write(a.text)
    out.close()
