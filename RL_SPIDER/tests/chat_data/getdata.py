# C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER\tests\chat_data
# C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER
# https://github.com/saurabhjadhav1911/RL.git
# C:\Users\Public\RL\ABC\ABC
# C:\Users\vaibhav\Documents\Python\RL\RL_SPIDER

import bs4 as bs
try:
    import urllib2 as ur
except:
    import urllib.request as ur
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
import traceback

class UrlTree():
	"""docstring for UrlTree"""
	def __init__(self, url):
		self.url=url
		self.childs = {}
		self.data=None

	def put(self,index,data):
		if (len(index) > 1):
			if index[0] in self.childs:
				self.childs[index[0]].put(index[1:],data[1:])
			else:
				self.childs[index[0]]=UrlTree(index[0])
				self.childs[index[0]].put(index[1:],data[1:])
		else:
			if index[0] in self.childs:
				self.childs[index[0]].data=data[0]
			else:
				self.childs[index[0]]=UrlTree(index[0])
				self.childs[index[0]].data=data[0]
	def print_tree(self,n=0):
		g=""
		for i in range(n):
			g+="	" 
		print(g+self.url)
		for i in self.childs.keys():
			self.childs[i].print(n+1)

	def get():
		pass
		
	def savedata():
		pass

class WebScraperClient(QWebPage):

    def __init__(self, url=None):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.url = "https://www.quora.com/topic/Graduate-Aptitude-Test-in-Engineering-GATE" if url is None else url
        #self.url = "https://www.google.co.in" if url is None else url
        self.urltree=UrlTree(self.url,data)
        try:
            self.page = self.load_saved_page(self.url)
            print('loaded saved page')
        except Exception as e:
            exc_traceback = traceback.format_exc()
            print(exc_traceback)
            self.loadFinished.connect(self.on_page_load)

            self.mainFrame().load(QUrl(self.url))
            self.app.exec_()
            self.page = self.get_active_page()

            self.save_page(self.page, self.url)
        self.soup=self.get_soup(self.page)

    def load_branches(self,urls):
    	pass
    def on_page_load(self):
        self.app.quit()
        return None

    def get_soup(self, page=None):
        page = self.page if page is None else page
        soup = bs.BeautifulSoup(page, 'lxml')
        return soup

    def get_active_page(self):
        source = self.mainFrame().toHtml()
        page = source.toUtf8().data()
        return page

    def save_page(self, page, page_url):
        page_url = page_url.replace('/', '-')
        page_url = page_url.replace(':', '-')
        with open("WebPages/" + page_url + ".html", "w") as f:
            f.write(page)
        print('{} page saved'.format(page_url))

    def load_saved_page(self, page_url):
        page_url = page_url.replace('/', '-')
        page_url = page_url.replace(':', '-')
        with open("WebPages/" + page_url + ".html", "r") as f:
            page = f.read()
        return page

    def get_elements(self, soup=None):
        soup = self.soup if soup is None else soup
        return [element for element in soup.find_all('span', class_='question_text')],[element for element in soup.find_all('span', class_='')]

    def get_urls(self, soup=None):
        soup = self.soup if soup is None else soup
        return [element for element in soup.find_all('a', class_='question_link')]



def main():
    # print(dir(WebScraperClient))
    wb = WebScraperClient()
    for el in wb.get_urls():
    	print(el['href'])

if __name__ == '__main__':
    main()
