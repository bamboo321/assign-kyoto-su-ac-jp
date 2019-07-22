import requests
import re
from bs4 import BeautifulSoup
import dateutil.parser

class webpage:
    def __init__(self):
        self.updateDate = None

        self.ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)" \
                "AppleWebKit/537.36 (KHTML, like Gecko)" \
                "Chrome/75.0.3770.142 Safari/537.36"
        self.url = "https://assign.kyoto-su.ac.jp/statistics/"


    def requestPage(self):
        resp = requests.get(self.url, headers={"User-Agent": self.ua})
        self.bs4Obj = BeautifulSoup(resp.content, 'lxml')


    def returnUpdateDateAndLabData(self):
        li = [self.fetchUpdateDate(), self.fetchLabNameAndPoints()]
        return li


    def fetchUpdateDate(self):
        title = self.bs4Obj.find_all(id='title').pop(1).text
        m = re.search(':.*\)', title)

        self.updateDate = m.group(0)[2:-1]
        self.updateDate = dateutil.parser.parse(self.updateDate)

        return self.updateDate


    def fetchLabNameAndPoints(self):
        tr = self.bs4Obj.find_all('tr')
        del tr[0]

        labName = []
        pointslist = {}

        for line in tr:
            n = line.find('th').text
            p = line.find_all('td')
            labName.append(n)

        for line in tr:
            n = line.find('th').text
            p = line.find_all('td')

            for i in p:
                if not i.text == "":
                    if n in pointslist:
                        pointslist[n].append(i.text)
                    else:
                        pointslist[n] = []
                        pointslist[n].append(i.text)
                else:
                    if n in pointslist:
                        pointslist[n].append('0')
                    else:
                        pointslist[n] = []
                        pointslist[n].append('0')

        return pointslist

        #for key in pointslist:
        #    print(key, pointslist[key])
