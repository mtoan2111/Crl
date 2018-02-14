from __future__ import print_function

import threading
import time

from Queue import Queue
from threading import Thread, Lock
from decimal import Decimal

from bs4 import BeautifulSoup
from selenium import webdriver

from Product import Product

from selenium.common.exceptions import TimeoutException
from requests.exceptions import ConnectionError

class HTML_Parsing:
  def __init__(self):
    self._TaskPagingQueue = Queue()
    self._ProductQueue = Queue()
    self._TaskProductQueue = Queue()
    self._OutPagingQueue = Queue()
    self._OutProductQueue = Queue()
    self._PrintLook = Lock()
    self._LstProduct = list()
    self._MainSource = "https://shop.adidas.jp/item/?cateId=1&condition=4%245&gendId=m&limit=40&page="
    self._ProductSource = "https://shop.adidas.jp"
    self._NumOfPaging = 0
    self._MAX_SUB_THREAD = 4

  def parsingHTML(self):
    return self.__parsingHTML()

  def __getContentMainPage(self):
    print ("-> Acquiring Main Page Content: ", end='')
    _SuccessFLG = False
    while not _SuccessFLG:
      try:
        _driver = webdriver.Chrome()
        _driver.get(self._MainSource + str(1))
        _html = _driver.page_source
        _soup = BeautifulSoup(_html, "html.parser")
        _driver.close()
        _num_page = Decimal(_soup.select("a.paging")[-1].text.strip())
        print (str(_num_page) + " pages were acquired")
        _SuccessFLG = True
        return Decimal(_soup.select("a.paging")[-1].text.strip())
      except ConnectionError as Err:
        print ("\t-> Error: Can't load this page ", end='')
        print (Err)
        print ("\t-> Trying to reload ...")
      except TimeoutException as tmout:
        print ("\t-> Error: Can't load this page ", end='')
        print (tmout)
        print ("\t-> Trying to reload ...")

  def __createTaskQueue(self):
    [self._TaskPagingQueue.put(self._MainSource + str(i))
     for i in range(1,self._NumOfPaging + 1)]

  def __getNumProduct(self, i, q):
    _ProductSource = q.get()
    with self._PrintLook:
      print ("+ " + threading.currentThread().getName() + " -> Processing: " + _ProductSource)
    _driver = webdriver.Chrome()
    _driver.get(_ProductSource)
    _html = _driver.page_source
    _soup = BeautifulSoup(_html,"html.parser")
    _driver.close()
    [self._OutPagingQueue.put_nowait(item['href'].encode("UTF-8"))
                                     for item in _soup.findAll("a",{
                                     "data-ga-event-category": "eec_productlist"})]
    q.task_done()
    time.sleep(1)
    with self._PrintLook:
      print (". " + threading.currentThread().getName() + " -> Done!")

  def __createProductLink(self, link):
      [self._ProductQueue.put(self._ProductSource + link[i])
       for i in range(5)]

  def __createTaskProductQueue(self):
    print ("-> Create Product Queue: ", end='')
    step = len(self._LstProduct)/self._MAX_SUB_THREAD
    [self._TaskProductQueue.put([self._LstProduct[m] for m in range(n - step, n, 1)])
                                for n in range(step, len(self._LstProduct), step)]
    print (str(self._TaskProductQueue.qsize()) + " elements in queue were created")

  def __getProductDetails(self, q):
    LstSubProduct = q.get()
    for i in LstSubProduct:
      with self._PrintLook:
        print ("+ " + threading.currentThread().getName() + "\t-> Now Processing: " + i, end='')
      self._OutProductQueue.put(Product().getProductDetailsFromHTML(i))
      time.sleep(1)
      with self._PrintLook:
        print ("\t-> Done!")
    q.task_done()

  def __parsingHTML(self):
    self._NumOfPaging = self.__getContentMainPage()
    if __name__ == "__main__":
      print("-> Starting")
    for i in range(self._NumOfPaging):
      worker = Thread(target=self.__getNumProduct, args=(i, self._TaskPagingQueue))
      worker.setDaemon(True)
      worker.start()
    self.__createTaskQueue()
    self._TaskPagingQueue.join()
    self._LstProduct = list(set(self._OutPagingQueue.queue))
    self.__createProductLink(self._LstProduct)
    with self._OutPagingQueue.mutex:
      self._OutPagingQueue.queue.clear()
    print ("-> Done: " + str(len(self._LstProduct)) + " products were acquired")
    self.__createTaskProductQueue()
    for i in range(self._TaskProductQueue.qsize()):
      worker = Thread(target=self.__getProductDetails, args=(self._TaskProductQueue,))
      worker.setDaemon(True)
      worker.start()
    self._TaskProductQueue.join()
    _LstSubProduct = list(self._OutProductQueue.queue)
    return _LstSubProduct

if __name__ == "__main__":
  print (HTML_Parsing().parsingHTML()[0].ProductId)

