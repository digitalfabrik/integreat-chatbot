import json
from io import StringIO
from html.parser import HTMLParser

class HTMLRemover(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = HTMLRemover()
    s.feed(html)
    return s.get_data()


f = open("test-data/munchen-de-pages.json", "r")
data = json.load(f)

for page in data:
    filename = "test-data/munchen-de/" + str(page.get('id')) + ".txt"
    new_file = open(filename, "w")
    new_file.write(page.get("title") + ".\n")
    new_file.write(strip_tags(page.get("content")))
