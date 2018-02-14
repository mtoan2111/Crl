from __future__ import print_function

from HTML_Parsing import HTML_Parsing
from AttackDB import AttackDB
from Product import Product

_LstProductCurrent = list()
_LstProductDB = dict()
_LstProductNew = list()
_LstProductOld = list()
if __name__ == "__main__":
  _DB = AttackDB()
  _LstProduct = HTML_Parsing().parsingHTML()
  _LstProductDB = _DB.getListProductId()
  # _LstProductNew = [product for product in _LstProduct if product.ProductId not in _LstProductDB]
  for product in _LstProduct:
    if product.ProductId not in _LstProductDB:
      _LstProductNew.append(product)
    else:
      _LstProductOld.append(product)
  if len(_LstProductNew) > 0:
    print ("-> Have " + str(len(_LstProductNew)) + " new items")
    for _product in _LstProductNew:
      print ("-> " + _product.ProductId + "\t -> Inserting: ", end='')
      if _DB.insertRowToDB(_product):
        print ("Done!")
  else:
    print ("-> Doesn't have any new items")
  if len(_LstProductOld) > 0:
    print("-> Checking "+ str(len(_LstProductOld)) + " old item(s) to get new details.")
    # -*- Compare old product -*-
    for _product in _LstProductOld:
      _TmpProduct = _DB.getProductDetail(_product.ProductId)
      if not _TmpProduct.equal(_product):
        # -*- If have new stuffs -*-
        _DB.updateRowToDB(_product)
      else:
        print (str(_product.ProductId) + " doesn't have any new details")
  _DB.deattackDB()

