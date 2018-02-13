from __future__ import print_function

import mysql.connector as sql

from mysql.connector import errorcode as errcd


class AttackDB:
  def __init__(self):
    self._config = {
      "user"      :  "root",
      "password"  :  "123123",
      "host"      :  "127.0.0.1",
      "database"  :  "hostore"
    }
    self._cnx = self._cur = None
    self.__attackDB()
  @property
  def cnx(self):
    return self._cnx

  @cnx.setter
  def cnx(self, value):
    if self._cnx != value:
      self._cnx = value

  @property
  def cur(self):
    return self._cur

  @cur.setter
  def cur(self, value):
    if self._cur != value:
      self._cur = value

  def __attackDB(self):
    try:
      self.cnx = sql.connect(**self._config)
    except sql.Error as Err:
      if Err.errno == errcd.ER_ACCESS_DENIED_ERROR:
        if __name__ == "__main__":
          print ("-> Error: Somethings is wrong. Check Usrname/Password once again")
      elif Err.errno == errcd.ER_BAD_DB_ERROR:
        if __name__ == "__main__":
          print ("Database doesn't exist")
      else:
        if __name__ == "__main__":
          print("* Error: \t", end='')
          print(Err)
    else:
      self.cur = self.cnx.cursor(prepared=True)

  def insertDB(self, product):
    self.__addProduct(product)
    self.__addProductImgs(product)
    self.__addProductSizes(product)
    self.__addProductCategory(product)
    self.__addProductURL(product)
    try:
      self.cnx.commit()
      self.__deattackDB()
    except sql.Error as Err:
      print ("* Error: \t",end='')
      print (Err)

  def __addProduct(self, _product):
    try:
      if  __name__ == "__main__":
        print ("-> Inserting Product: ", end= '')
      _Product = """INSERT INTO Product
                    (P_ID, P_Name, P_Gender, P_Price, P_SoldOut)
                    VALUE (?, ?, ?, ?, ?)"""
      _Product_data = (_product.ProductId,
                       _product.ProductName,
                       _product.ProductGender,
                       _product.ProductPrice,
                       _product.ProductSoldOut)
      self.cur.execute (_Product, _Product_data)
      if __name__ == "__main__":
        print ("Done!")
    except sql.Error as Err:
      print ("* Error: \t",end='')
      print (Err)

  def __addProductImgs(self, _product):
    try:
      if __name__ == "__main__":
        print ("-> Inserting Product Images ", end='')
      _Imgs ="""INSERT INTO ProductImgs
                (P_ID, P_IMG)
                VALUE (?, ?)"""
      for img in _product.ProductImgs:
        _ProductImg = (_product.ProductId, img)
        self.cur.execute (_Imgs, _ProductImg)
      if __name__ == "__main__":
        print ("Done!")
    except sql.Error as Err:
      print ("* Error: \t",end='')
      print (Err)

  def __addProductSizes(self, _product):
    try:
      if __name__ == "__main__":
        print ("-> Inserting Product Sizes ", end='')
      _Sizes = """INSERT INTO ProductSizes
                  (P_ID, P_Size)
                  VALUE (?, ?)"""
      for size in _product.ProductSizes:
        _ProductSize = (_product.ProductId, size)
        self.cur.execute(_Sizes,_ProductSize)
      if __name__ == "__main__":
        print ("Done!")
    except sql.Error as Err:
      print ("* Error: \t",end='')
      print (Err)

  def __addProductCategory(self, _product):
    try:
      if __name__ == "__main__":
        print ("-> Inserting Product Category ", end='')
      _Cate ="""INSERT INTO ProductCategory
                (P_ID, P_CAT)
                VALUE (?, ?)"""
      for cat in _product.ProductBrand:
        _ProductCate =(_product.ProductId, cat)
        self.cur.execute(_Cate, _ProductCate)
      if __name__ == "__main__":
        print ("Done!")
    except sql.Error as Err:
      print ("* Error: \t",end='')
      print (Err)

  def __addProductURL(self, _product):
    try:
      if __name__ == "__main__":
        print ("-> Inserting Product URL", end='')
        _URL = """INSERT INTO ProductURL
                  (P_ID, P_URL)
                  VALUE (?, ?)"""
        _ProductURL = (_product.ProductId, _product.ProductURL)
        self.cur.execute(_URL,_ProductURL)
    except sql.Error as Err:
      print ("* Error: \t",end='')
      print (Err)

  def __deattackDB(self):
    try:
      if self.cur:
        self.cur.close()
      if self.cnx:
        self.cnx.close()
    except sql.Error as Err:
      print ("* Error: \t",end='')
      print (Err)

  def __rowExist(self):
    result = False
    return result

  def __updateDB(self, product):
    try:

      """Do somethings... (haven't finished)"""

      self.__deattackDB()
    except sql.Error as Err:
      print("* Error: \t", end='')
      print(Err)


