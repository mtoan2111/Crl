from __future__ import print_function

import urllib as ul
import threading

from Queue import Queue
from bs4 import BeautifulSoup
from threading import Thread, Lock
from selenium import webdriver
from decimal import Decimal

task_queue = Queue()
product_queue = Queue()
out_queue = Queue()
print_look = threading.Lock()
source = "https://shop.adidas.jp/item/?cateId=1&condition=4%245&gendId=m&limit=120&page="
pdt_source = "https://shop.adidas.jp"
paging = 0

def getContentMainPage():
  print ("-> Acquiring Main Page Content: ", end='')
  driver = webdriver.Chrome()
  driver.get(source + str(1))
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  num_page = Decimal(soup.select("a.paging")[-1].text.strip())
  print (str(num_page) + " pages were acquired")
  return Decimal(soup.select("a.paging")[-1].text.strip())


def createTaskQueue():
  for i in range(1,paging + 1):
    task_queue.put(source + str(i))

def getProduct(i, q):
  sub_source = q.get()
  with print_look:
    print ("+ " + threading.currentThread().getName() + " -> Processing: " + sub_source)
  driver = webdriver.Chrome()
  driver.get(sub_source)
  html = driver.page_source
  soup = BeautifulSoup(html,"html.parser")
  for item in soup.findAll("a",{"data-ga-event-category": "eec_productlist"}):
    out_queue.put_nowait(item['href'])
  task_queue.task_done()
  with print_look:
    print ("/ " + threading.currentThread().getName() + " -> Done!")

def createProductLink(link):
  for product in link:
    product_queue.put(pdt_source + product)

if __name__ == "__main__":
  paging = getContentMainPage()
  print("-> Starting")
  for i in range(paging):
    worker = Thread(target=getProduct, args=(i, task_queue))
    worker.setDaemon(True)
    worker.start()
  createTaskQueue()
  task_queue.join()
  LstProduct = list(set(out_queue.queue))
  createProductLink(LstProduct)
  with out_queue.mutex:
    out_queue.queue.clear()
  print ("-> Done: " + str(len(LstProduct)) + " products were acquired")
