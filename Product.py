from __future__ import print_function

import hashlib

from copy import deepcopy
from decimal import Decimal
from requests.exceptions import ConnectionError

from bs4 import BeautifulSoup
from selenium import webdriver
from googletrans import Translator

from selenium.common.exceptions import TimeoutException


class Product(object):

  def __init__(self):
    self._ProductName = ''
    self._ProductId = ''
    self._ProductBrand = list()
    self._ProductGender = ''
    self._ProductLink = ''
    self._ProductImgs = list()
    self._ProductPrice = .0
    self._ProductSizes = list()
    self._ProductSoldOut = False
    self._ProductURL = ''
    self.soup = BeautifulSoup

  @property
  def ProductName(self):
    return self._ProductName

  @ProductName.setter
  def ProductName(self, value):
    if self._ProductName != value:
      self._ProductName = value

  @property
  def ProductId(self):
    return self._ProductId

  @ProductId.setter
  def ProductId(self, value):
    if self._ProductId != value:
      self._ProductId = value

  @property
  def ProductBrand(self):
    return self._ProductBrand

  @ProductBrand.setter
  def ProductBrand(self, value):
    if self._ProductBrand != value:
      self._ProductBrand = value

  @property
  def ProductGender(self):
    return self._ProductGender

  @ProductGender.setter
  def ProductGender(self, value):
    if self._ProductGender != value:
      self._ProductGender = value

  @property
  def ProductLink(self):
    return self._ProductLink

  @ProductLink.setter
  def ProductLink(self, value):
    if self._ProductLink != value:
      self._ProductLink = value

  @property
  def ProductImgs(self):
    return self._ProductImgs

  @ProductImgs.setter
  def ProductImgs(self, value):
    if self.ProductImgs != value:
      self._ProductImgs = deepcopy(value)

  @property
  def ProductPrice(self):
    return self._ProductPrice

  @ProductPrice.setter
  def ProductPrice(self, value):
    if self._ProductPrice != value:
      self._ProductPrice = value

  @property
  def ProductSizes(self):
    return self._ProductSizes

  @ProductSizes.setter
  def ProductSizes(self, value):
    if self._ProductSizes != value:
      self._ProductSizes = value

  @property
  def ProductSoldOut(self):
    return self._ProductSoldOut

  @ProductSoldOut.setter
  def ProductSoldOut(self, value):
    if self._ProductSoldOut != value:
      self._ProductSoldOut = value

  @property
  def ProductURL(self):
    return self._ProductURL

  @ProductURL.setter
  def ProductURL(self, value):
    if self._ProductURL != value:
      self._ProductURL = value

  def getProductDetailsFromHTML(self,s):
    self.ProductLink = s
    self.__getProductId()
    self.__getProductURL()
    if __name__ == "__main__":
      print("-> Starting Analysis Product: " + self.ProductId)
    self.__getContentProduct()
    self.__getProductImg()
    self.__getProductName()
    self.__getProductPrice()
    self.__getProductSize()
    self.__getProductGender()
    self.__getProductBrand()
    return self

  def __getProductId(self):
    if __name__ == "__main__":
      print ("-> Acquiring Product ID: ", end='')
    try:
      self.ProductId = self.ProductLink.split("/")[-2].encode("UTF-8")
      if __name__ == "__main__":
        print (self.ProductId)
    except IndexError as e:
      print ("\t-> Error: Can't get Id of product ", end='')
      print (e)

  def __getProductURL(self):
    if __name__ == "__main__":
      print("-> Calculating Product URL: ", end='')
    try:
      self.ProductURL = hashlib.md5(self.ProductId).hexdigest()[:8]
      if __name__ == "__main__":
        print (self.ProductURL)
    except IndexError as e:
      print ("\t-> Can't calculate product url")

  def __getContentProduct(self):
    if __name__ == "__main__":
      print ("-> Acquiring Product Content Page: ", end='')
    SuccessFLGS = False
    while not SuccessFLGS:
      try:
        driver = webdriver.Chrome()
        driver.get("https://shop.adidas.jp" + self.ProductLink)
        html = driver.page_source
        self.soup = BeautifulSoup(html, "html.parser")
        driver.close()
        for s in self.soup.findAll("script"):
          s.extract()
        # f = open ("product.txt", "w")
        # f.write(self.soup.encode("UTF-8"))
        # f.close()
        SuccessFLGS = True
        if __name__ == "__main__":
          print ("Done!")
      except ConnectionError as e:
        print ("\t-> Error: Can't open the page ", end='')
        print (e)
      except TimeoutException as tmout:
        print ("\t-> Error: Can't load this page ", end='')
        print (tmout)
        print ("Trying to reload ...")

  def __getProductImg(self):
    if __name__ == "__main__":
      print ("-> Acquiring Product Images: ", end='')
    try:
      for s in self.soup.findAll("div",{"class" : "thumbnails"}):
      # print (type (s))
        for m in s.findAll("img"):
          if str(m["src"]).find(self.ProductId) != -1:
            self.ProductImgs.append(str(m["src"]).replace("s-","z-").split("/")[-1])
      if __name__ == "__main__":
        print(str(len(self.ProductImgs)) + " images were acquired!")
    except IndexError as e:
      print ("\t-> Error: Can't get images of product ", end='')
      print (e)

  def __getProductName(self):
    if __name__ == "__main__":
      print ("-> Acquiring Product Name: ", end='')
    try:
      _name = Translator().translate(self.soup.select("h1#itemName_h1")[0].text.strip())
      s_name = _name.text.split(u'\u3010')
      if len(s_name) > 1:
        for i in range(1, len(s_name)):
          self.ProductBrand.append(s_name[i][:-1].encode("UTF-8"))
      else:
        s_name = _name.text.split(" [")
        if len(s_name) > 1:
          for i in range(1, len(s_name)):
            self.ProductBrand.append(s_name[i][:-1].encode("UTF-8"))
      self.ProductName = s_name[0].encode("UTF-8")
      if __name__ == "__main__":
        print(self.ProductName)
    except IndexError as e:
      print ("\t-> Error: Can't get name of product: " + self.ProductId + " ", end='')
      print (e)
    except ConnectionError as e:
      print ("\t-> Error: Can't connect to server ", end='')
      print (e)

  def __getProductPrice(self):
    if __name__ == "__main__":
      print ("-> Acquiring Product Price: ", end='')
    try:
      price = self.soup.findAll("p", {"class": "sale"})[0].text.encode("UTF-8").strip().replace(",","")
      if __name__ == "__main__":
        print (price + " -> ", end='')
      self.ProductPrice = (Decimal(price[2:]) * 220) + 200000
      if __name__ == "__main__":
        print("VND" + str(self.ProductPrice))
    except IndexError as e:
      print ("\t-> Error: Can't get price of product ", end='')
      print (e)

  def __getProductSize(self):
    if __name__ == "__main__":
      print ("-> Acquiring Available Product Size: ", end='')
    try:
      for s in self.soup.findAll("li", {"class" : "sold_out"}):
        s.extract()
      for s in self.soup.findAll("li", {"class" : "js-select_size"}):
        self.ProductSizes.append(s.findAll("p")[0].text.encode("UTF-8").strip())
      if len(self.ProductSizes) == 0:
        self.ProductSoldOut = True
      if __name__ == "__main__":
        print(str(len(self.ProductSizes)) + " available sizes were acquired!")
    except IndexError as e:
      print ("\t-> Error: Can't get size of product ", end='')
      print (e)

  def __getProductGender(self):
    if __name__ == "__main__":
      print ("-> Acquiring Product Gender: ", end='')
    try:
      getGender = self.soup.select("span.gender")
      if len(getGender) > 0:
        self.ProductGender = Translator().translate(getGender[0].text.encode("UTF-8").strip()).text.encode("UTF-8")[:-1]
      else:
        self.ProductGender = "unisex"
      if __name__ == "__main__":
        print(self.ProductGender)
    except IndexError as e:
      print ("\t-> Error: Can't get gender of product ", end='')
      print (e)

  def __getProductBrand(self):
    if __name__ == "__main__":
      print ("-> Acquiring Product Brand: ", end='')
    try:
      LstSpan = (self.soup.findAll("span", {"class" : "adih_l"}))
      if len(LstSpan) == 2:
        self.ProductBrand.append(self.soup.findAll("span", {"class" : "adih_l"})[0].text.encode("UTF-8").strip())
      else:
        self.ProductBrand.append(self.soup.findAll("span", {"class" : "adih_l"})[1].text.encode("UTF-8").strip())
      if __name__ == "__main__":
        print(self.ProductBrand)
    except IndexError as e:
      print ("\t-> Error: Can't get brand of product ", end='')
      print (e)

  def equal(self,_other):
    _equal = False
    if self.ProductId == _other.ProductId:
      _equal = True
      return _equal
    if self.ProductGender == _other.ProductGender:
      _equal = True
      return _equal
    if self.ProductURL == _other.ProductURL:
      _equal = True
      return _equal
    if self.ProductBrand == _other.ProductBrand:
      _equal = True
      return _equal
    if self.ProductName == _other.ProductName:
      _equal = True
      return _equal
    if self.ProductPrice == _other.ProductPrice:
      _equal = True
      return _equal
    if self.ProductLink == _other.ProductLink:
      _equal = True
      return _equal
    if self.ProductSizes == _other.ProductSizes:
      _equal = True
      return _equal
    if self.ProductImgs == _other.ProductImgs:
      _equal = True
      return _equal
    if self.ProductBrand == _other.ProductBrand:
      _equal = True
      return _equal
    return _equal

# Product().getProductDetailsFromHTML("/products/")