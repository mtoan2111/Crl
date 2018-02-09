from __future__ import print_function

from decimal import Decimal
from bs4 import BeautifulSoup
from selenium import webdriver
from googletrans import Translator

class Product:
  ProductName = ''
  ProductId = 0
  ProductImgs = list()
  ProductPrice = 0
  ProductBrand = ''
  ProductSize = list()
  ProductGender = ''
  soup = BeautifulSoup
  ProductLink = ""
  def __init__(self, s):
    self.ProductLink = s
    self.getProductId()
    print ("-> Starting Analysis Product: " + self.ProductId)
    self.getContentProduct()
    self.getProductImg()
    self.getProductName()
    self.getProductPrice()
    self.getProductSize()
    self.getProductGender()
    self.getProductBrand()

  def getProductId(self):
    print ("-> Acquiring Product ID: ", end='')
    self.ProductId = self.ProductLink.split("/")[-2]
    print (self.ProductId)

  def getContentProduct(self):
    print ("-> Acquiring Product Content Page: ", end='')
    driver = webdriver.Chrome()
    driver.get("https://shop.adidas.jp" + self.ProductLink)
    html = driver.page_source
    self.soup = BeautifulSoup(html, "html.parser")
    for s in self.soup.findAll("script"):
      s.extract()
    f = open ("product.txt","w")
    f.write(self.soup.encode("UTF-8"))
    f.close()
    print ("Done!")

  def getProductImg(self):
    print ("-> Acquiring Product Images: ", end='')
    for s in self.soup.findAll("div",{"class" : "thumbnails"}):
      # print (type (s))
      for m in s.findAll("img"):
        if str(m["src"]).find(self.ProductId) != -1:
          self.ProductImgs.append(str(m["src"]))
    print (str(len(self.ProductImgs)) +" images were acquired!")

  def getProductName(self):
    print ("-> Acquiring Product Name: ", end='')
    self.ProductName = Translator().translate(self.soup.select("h1#itemName_h1")[0].text.encode("UTF-8").strip()).text.encode("UTF-8")
    print (self.ProductName)

  def getProductPrice(self):
    print ("-> Acquiring Product Price: ", end='')
    price = self.soup.select("p.sale")[0].text.encode("UTF-8").strip().replace(",","")
    print (price + " -> ", end='')
    self.ProductPrice = (Decimal(price[2:]) * 220) + 200000
    print ("VND" + str(self.ProductPrice))

  def getProductSize(self):
    print ("-> Acquiring Available Product Size: ", end='')
    for s in self.soup.findAll("li", {"class" : "sold_store"}):
      self.ProductSize.append(s.findAll("p")[0].text)
    print(str(len(self.ProductSize)) + " available sizes were acquired!")

  def getProductGender(self):
    print ("-> Acquiring Product Gender: ", end='')
    self.ProductGender = Translator().translate(self.soup.select("span.gender")[0].text.encode("UTF-8").strip()).text.encode("UTF-8")[:-1]
    print (self.ProductGender)

  def getProductBrand(self):
    print ("-> Acquiring Product Brand: ", end='')
    self.ProductBrand = self.soup.select("h2#brand111")[0].findAll("span", {"class" : "adih_l"})[0].text.encode("UTF-8").strip()
    print (self.ProductBrand)

td = Product("/products/S82443/")

