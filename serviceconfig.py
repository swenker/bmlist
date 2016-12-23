__author__ = 'wenju'

import logging.config
from ConfigParser import ConfigParser
import os.path

class BmConfig():
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

        self.book_provider_url=configparser.get("web","book_provider_url")

    def  getlogger(self,loggername="BmlistService"):
        return logging.getLogger(loggername)

# bmconfig = BmConfig("conf")
bmconfig = BmConfig("conf/local")
logger=bmconfig.getlogger()
bmconfig.getlogger().info("Service Config loaded successfully..")