from __future__ import print_function

from HTML_Parsing import HTML_Parsing
from AttackDB import AttackDB
from Product import Product

_LstProductCurrent = list()
_LstProductDB = dict()
if __name__ == "__main__":
 _LstProduct = HTML_Parsing().parsingHTML()
 _LstProductDB = AttackDB().getListProductId()
 print ([i.ProductId for i in _LstProduct])
 print (_LstProductDB)
 print ([x for x in _LstProduct if x in _LstProductDB])
 # for productHTML in _LstProduct:
 #   if productHTML.ProductId in _LstProductDB:
 #     print ("Existed")

 # for product in _LstProduct:
 #  AttackDB().insertRowToDB(product)
