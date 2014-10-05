import re

from collections import OrderedDict
from html.parser import HTMLParser

from wikicurses import formats

ENDPAR, STARTPAR, ENDH = range(3)

def parseExtract(html):
    parser = _ExtractHTMLParser()
    parser.feed(html)
    return parser.sections

def parseFeature(html):
    parser = _FeatureHTMLParser()
    parser.feed(html)
    return parser.text

class _ExtractHTMLParser(HTMLParser):
    cursection = ''
    inh = 0
    format = 0

    def __init__(self):
        self.sections = OrderedDict({'':[]})
        super().__init__(self)

    def add_text(self, text):
        if text == ENDPAR:
            if self.format&formats.blockquote:
                return
            text = '\n\n'
        elif text == STARTPAR:
            if self.format&formats.blockquote:
                text = '\n> '
            else:
                return
        elif text == ENDH:
            text = '\n'
        elif not text.strip():
            return

        tformat = self.format

        if self.inh == 2:
            self.cursection = text
            self.sections[text] = []
            return
        elif self.inh > 2:
            tformat = 'h'
        self.sections[self.cursection].append((tformat, text))

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            #Remove previous section if empty
            if not self.sections[self.cursection]:
                del self.sections[self.cursection]
            self.cursection = ''
        if re.fullmatch("h[2-6]", tag):
            self.inh = int(tag[1:])
        elif tag == 'p':
            self.add_text(STARTPAR)
        elif tag == 'li':
            self.add_text("- ")
        elif tag in (i.name for i in formats):
            self.format|=formats[tag]

    def handle_endtag(self, tag):
        if re.fullmatch("h[2-6]", tag):
            self.inh = 0
            self.add_text(ENDH)
        elif tag == 'p':
            self.add_text(ENDPAR)
        elif tag in (i.name for i in formats):
            self.format&=~formats[tag]
        if tag == 'blockquote':
            self.add_text(ENDPAR)

    def handle_data(self, data):
        self.add_text(re.sub('\n+', '\n', data))


class _FeatureHTMLParser(HTMLParser):
    text = ''
    def handle_data(self, data):
        self.text += data
