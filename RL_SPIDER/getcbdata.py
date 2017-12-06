import urllib.request
from bs4 import BeautifulSoup
import time
page = urllib.request.urlopen("https://www.quora.com/topic/Graduate-Aptitude-Test-in-Engineering-GATE")

soup = BeautifulSoup(page, 'lxml')

question=[line.text for line in soup.find_all('span',class_='question_text')]
answers=[line.text for line in soup.find_all('span',class_='question_text')]

print(question)
