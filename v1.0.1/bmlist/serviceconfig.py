__author__ = 'samsung'

import logging.config
from ConfigParser import ConfigParser
import os.path

class BmConfig():
    #_instance =
    def __init__(self,confpath):

        conffile=confpath+"/bmlist.cfg"
        #print os.path.abspath(conffile)
        if not os.path.exists( os.path.abspath(conffile)):
            #guess it. it takes effect for test mostly
            confpath += "/local"
            print "------------------"
            print "Attention:[%s] does not exist,the following path will be used:\n[%s]" %(os.path.abspath(conffile),os.path.abspath(confpath))
            print "------------------"

        logging.config.fileConfig(confpath+"/log.cfg")

        configparser=ConfigParser()
        configparser.read(confpath+"/bmlist.cfg")
        self.configparser=configparser

        self.dbn=configparser.get('db','dbn','mysql')
        self.host=configparser.get('db','host','localhost')
        self.db=configparser.get('db','db','bmlist')
        self.user=configparser.get('db','user','bmlist')
        self.passwd=configparser.get('db','passwd','bmlist1')

        self.book_provider_url=configparser.get("web","book_provider_url")

    def  getlogger(self,loggername="BmService"):
        return logging.getLogger(loggername)

bmconfig = BmConfig("conf")
bmconfig.getlogger().info("Service Config loaded successfully..")