import urllib3
from bs4 import BeautifulSoup

nips_proceedings = "https://papers.nips.cc"
base = "https://papers.nips.cc"

http = urllib3.PoolManager()

def getYears():
    response = http.request('GET', nips_proceedings)
    soup = BeautifulSoup(response.data.decode('utf-8'), "html5lib")
    years = soup.select("div.main.wrapper.clearfix > ul > li > a")
    return list(map(lambda x: base + x['href'], years))

def getPapers(url):
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf-8'), "html5lib")
    years = soup.select("div.main.wrapper.clearfix > ul > li")
    return list(map(mapPaper, years))

def mapPaper(elem):
    children = elem.select('a')
    paper = children[0].getText()
    authors = []
    for i in range(1,len(children)):
        child = children[i]
        authors.append(child.getText())
    data = {'paper' : paper, 'authors' : authors}
    return data