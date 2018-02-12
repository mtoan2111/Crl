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

  def Attack(self):
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
          print (Err)
    else:
      self.cur = self.cnx.cursor()
      self.cur.execute("show database;")
      for row in self.cur.fetchall():
        print (row)
    finally:
      if self.cur:
        self.cur.close()
      if self.cnx:
        self.cnx.close()

