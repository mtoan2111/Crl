from __future__ import print_function

import threading

from Queue import Queue
from threading import Thread, Lock
from decimal import Decimal

from bs4 import BeautifulSoup
from selenium import webdriver

from Product import Product

from selenium.common.exceptions import TimeoutException
from requests.exceptions import ConnectionError


task_queue = Queue()
product_queue = Queue()
task_product_queue = Queue()
out_queue = Queue()
out_sub_queue = Queue()
print_look = threading.Lock()
source = "https://shop.adidas.jp/item/?cateId=1&condition=4%245&gendId=m&limit=120&page="
pdt_source = "https://shop.adidas.jp"
paging = 0
MAX_SUB_THREAD = 2

def getContentMainPage():
  print ("-> Acquiring Main Page Content: ", end='')
  SuccessFLG = False
  while not SuccessFLG:
    try:
      driver = webdriver.Chrome()
      driver.get(source + str(1))
      html = driver.page_source
      soup = BeautifulSoup(html, "html.parser")
      driver.close()
      num_page = Decimal(soup.select("a.paging")[-1].text.strip())
      print (str(num_page) + " pages were acquired")
      SuccessFLG = True
      return Decimal(soup.select("a.paging")[-1].text.strip())
    except ConnectionError as cErr:
      print ("Error: Can't load this page ", end='')
      print (cErr)
      print ("Trying to reload this page")
      driver.refresh()
    except TimeoutException as tmout:
      print ("Error: Can't load this page ", end='')
      print (tmout)
      print ("Trying to reload this page")

def createTaskQueue():
  for i in range(1,paging + 1):
    task_queue.put(source + str(i))

def getNumProduct(i, q):
  sub_source = q.get()
  with print_look:
    print ("+ " + threading.currentThread().getName() + " -> Processing: " + sub_source)
  driver = webdriver.Chrome()
  driver.get(sub_source)
  html = driver.page_source
  soup = BeautifulSoup(html,"html.parser")
  driver.close()
  for item in soup.findAll("a",{"data-ga-event-category": "eec_productlist"}):
    out_queue.put_nowait(item['href'].encode("UTF-8"))
  q.task_done()
  with print_look:
    print (". " + threading.currentThread().getName() + " -> Done!")

def createProductLink(link):
  for product in link:
    product_queue.put(pdt_source + product)

def createTaskProductQueue():
  print ("-> Create Product Queue: ", end='')
  step = len(LstProduct)/MAX_SUB_THREAD
  for n in range(step,len(LstProduct),step):
    LstTemp = list()
    for m in range(n - step, n, 1):
      LstTemp.append(LstProduct[m])
    task_product_queue.put(LstTemp)
  print (str(task_product_queue.qsize()) + " elements in queue were created")

def getProductDetails(q):
  LstSubProduct = q.get()
  for i in LstSubProduct:
    with print_look:
      print ("+ " + threading.currentThread().getName() + "\t-> Now Processing: " + i, end= '')
    out_sub_queue.put(Product(i))
    with print_look:
      print ("\t-> Done!")
  q.task_done()

if __name__ == "__main__":
  paging = getContentMainPage()
  print("-> Starting")
  for i in range(paging):
    worker = Thread(target=getNumProduct, args=(i, task_queue))
    worker.setDaemon(True)
    worker.start()
  createTaskQueue()
  task_queue.join()
  LstProduct = list(set(out_queue.queue))
  createProductLink(LstProduct)
  with out_queue.mutex:
    out_queue.queue.clear()
  print ("-> Done: " + str(len(LstProduct)) + " products were acquired")
  createTaskProductQueue()
  for i in range(task_product_queue.qsize()):
    worker = Thread(target=getProductDetails, args=(task_product_queue,))
    worker.setDaemon(True)
    worker.start()
  task_product_queue.join()
  LstSubProduct = list(out_sub_queue.queue)
  for i in LstSubProduct:
    print (i.ProductName)


