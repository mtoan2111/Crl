from __future__ import print_function
import urllib as ul
import Queue as qu
import multiprocessing as mp
from bs4 import BeautifulSoup
from threading import Thread, Lock


class HTML:
  lstPageSource = list()
  source = "https://shop.adidas.jp/item/?cateId=1&condition=4%245&gendId=m&limit=120&page="

  def __init__(self):
    process = [mp.Process(target=self.getProduct, args=(i,self.output)) for i in range(15)]
    print ("starting")
    for p in process:
      p.start()
    for p in process:
      p.join(timeout=1)
      print (".", end='')
    print (".")
    print ("analyzing succeed")
    for p in process:
      print (p)
      print (self.output.get())
    result = [self.output.get() for p in process]
    print(result)

  output = mp.Queue()
  def getProduct(self, url, output):
    self.source += str(url)
    html = ul.urlopen(self.source).read()
    soup = BeautifulSoup(html,"html.parser")
    for item in soup.findAll("a",{"data-ga-event-category": "eec_productlist"}):
      self.output.put(item['href'])

test = HTML()
# url = "https://shop.adidas.jp/item/?gendId=m&condition=45&f=header"
# html = ul.urlopen(url).read()
# soup = BeautifulSoup(html, "html.parser")
# f = open("text",'w')
# for script in soup.findAll("script"):
#   script.extract()
# f.write(soup.encode("utf-8"))
# for itemcard in soup.findAll("a", {"class": "mod-link"}):
#   itemcard.extract()
#
# for item in soup.findAll("a", {"data-ga-event-category": "eec_productlist"}):
#   print (item['href'])
#   f.write(item.encode("utf-8"))

class GetDataContext(Thread):
  def __init__(self, queue):
    Thread.__init__(self)
    self.queue = queue

  def appendSet(self, s):
    s.append()