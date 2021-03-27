from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.exceptions import *
from sqlalchemy.exc import OperationalError
from configparser import ConfigParser
import os

config = ConfigParser()
config.read('config.ini')
print(config)
class DbInstance:
  __instance = None
  def __init__(self, conn_str):
    self.engine = create_engine(conn_str, echo=False, pool_pre_ping=True, pool_recycle=5)
    self.Base = declarative_base()
    self.Session = sessionmaker(bind=self.engine);
    self.__session = self.Session()

  @staticmethod
  def getInstance():
    if DbInstance.__instance is None:
      connStr = os.getenv("DB_URL", None)
      print(connStr)
      connStr = config.get('Default', 'connection_string', fallback='mysql+pymysql://root:newpass123@172.17.0.1/srm') if connStr is None else connStr
      print('connect to db: ', connStr)
      DbInstance.__instance = DbInstance(connStr)
    return DbInstance.__instance

  def session(self):
    return self.__session

  def newSession(self):
    print('reset session')
    try:
      self.__session.close()
      conn = self.engine.connect()
      conn.close();
      self.__session =  self.Session()
    except OperationalError as e:
      raise BadRequest("Error %s" % e.orig)
