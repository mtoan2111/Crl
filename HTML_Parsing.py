from __future__ import print_function
import urllib as ul
import threading
from Queue import Queue
from bs4 import BeautifulSoup
from threading import Thread, Lock

task_queue = Queue()
product_queue = Queue()
out_queue = Queue()
print_look = threading.Lock()
source = "https://shop.adidas.jp/item/?cateId=1&condition=4%245&gendId=m&limit=120&page="
pdt_source = "https://shop.adidas.jp"

def createTaskQueue():
  for i in range(1,16):
    task_queue.put(source + str(i))

def getProduct():
  with print_look:
    print (".", end='')
  html = ul.urlopen(source).read()
  soup = BeautifulSoup(html,"html.parser")
  for item in soup.findAll("a",{"data-ga-event-category": "eec_productlist"}):
    out_queue.put_nowait(item['href'])
  task_queue.task_done()
  with print_look:
    print (".", end='')

def createProductLink(link):
  for product in link:
    product_queue.put(pdt_source + product)

if __name__ == "__main__":
  print("starting")
  for i in range(15):
    worker = Thread(target=getProduct)
    worker.setDaemon(True)
    worker.start()
  createTaskQueue()
  task_queue.join()
  print ("Done")
  LstProduct = list(set(out_queue.queue))
  createProductLink(LstProduct)
  while not product_queue.empty():
    print (product_queue.get())