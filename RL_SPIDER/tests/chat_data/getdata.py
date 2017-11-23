#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER
#https://github.com/saurabhjadhav1911/RL.git
#C:\Users\Public\RL\ABC\ABC
#C:\Users\vaibhav\Documents\Python\RL\RL_SPIDER

import bs4 as bs
try:
    import urllib2 as ur
except:
    import urllib.request as ur
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage

class WebScraper():
	"""docstring for WebScraper"""
	def __init__(self, url=None):
		self.url="https://www.quora.com/" or url
		self.soup=self.get_page(self.url)

	def get_page(self,url=None):
		url=url or self.url
		page=ur.urlopen(url)
		soup=bs.BeautifulSoup(page,'lxml')
		return soup

	def get_elements(self,soup=None):
		soup=soup or self.soup
		return [element for element in soup.find_all('span',class_='question_text')]

class WebScraperClient(QWebPage):

    def __init__(self,url=None):
        self.app=QApplication(sys.argv)
        QWebPage.__init__(self)
        self.url="https://www.quora.com/topic/Graduate-Aptitude-Test-in-Engineering-GATE" or url
        
        try:
        	self.page=self.load_saved_page(self.url):
        	print('loaded saved page')
        except:
	        self.loadFinished.connect(self.on_page_load)
	        
	        self.mainFrame().load(QUrl(self.url))
	        self.app.exec_()
	        self.page=self.get_active_page()
	        self.save_page(self.page,self.url)
        #self.soup=self.get_active_page()

    def on_page_load(self):
        self.app.quit()

	def get_page(self,url):
		page=ur.urlopen(url)
		soup=bs.BeautifulSoup(page,'lxml')
		return soup

	def get_active_page(self):
		source=self.mainFrame().toHtml()
		page=source.toUtf8().data()
		return page

	def save_page(self,page,page_url):
		with open("WebPages/"+page_url+".html","w") as f:
			f.write(page)
		print('page saved')
	
	def load_saved_page(self,page_url):
		with open("WebPages/"+page_url+".html","r") as f:
			page=f.read(page)
		return page

    def get_elements(self):
        return self.soup#[element.text for element in self.soup.find_all('span',class_='question_text')]

def main():
	wb=WebScraperClient(url="https://www.google.co.in/")
	
	soup=bs.BeautifulSoup(page,'lxml')
	sp=soup.find('p')
	print(sp.text)

if __name__ == '__main__':
	main()