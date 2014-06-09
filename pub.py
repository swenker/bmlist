__author__ = 'samsung'

"""distribute files to right place"""

import os.path
import shutil
import sys
from test import test_bmservice
from test import test_serviceconfig
from test import test_bookparser



class Publisher(object):
    """One publish process should bound to the specified env"""

    def __init__(self,envset):
        self.envset=envset
        self.project_root=""
        self.dst_base=self.project_root+"dist"
        self.dst_web=self.project_root+"dist/bmlist"

        self.src_config_dir=self.project_root+"conf/"+envset
        self.dst_config_dir=self.project_root+"%s/%s" %(self.dst_web,"conf")

        self.src_template_dir=self.project_root+"python/templates"
        self.dst_template_dir=self.project_root+"%s/%s" %(self.dst_web,"templates")

        self.src_web_dir=self.project_root+"bmlist"
        self.dst_web_dir=self.project_root+""+self.dst_web


    def unit_test(self):
        print "unit test started"
        test_bmservice.run_test()
        test_serviceconfig.run_test()
        test_bookparser.run_test()

        print "unit test completed"

    def test(self):
        self.unit_test()

    def clean(self):
        if os.path.exists(self.dst_base):
            shutil.rmtree(self.dst_base)
        print "dist folder deleted."

    def dist_config_files(self):

        if not os.path.isdir(self.src_config_dir) or not os.path.exists(self.src_config_dir):
            print "please check :%s" %(self.src_config_dir)
            return False
        else:
            shutil.copytree(self.src_config_dir,self.dst_config_dir)
            return True

    def dist_web(self):
        if not os.path.isdir(self.src_web_dir) or not os.path.exists(self.src_web_dir):
            print "please check :%s" %(self.src_web_dir)
            return False
        else:
            shutil.copytree(self.src_web_dir,self.dst_web_dir,ignore=shutil.ignore_patterns('*.pyc'))
            #shutil.copytree(self.src_template_dir,self.dst_template_dir)
            return True


    def publish(self):
        print "publish started......"
        self.clean()

        if self.dist_web():
            if self.dist_config_files():
               print "publish completed......"
            else:
                print "failed to dist config files"
        else:
            print "Failed to dist web"

if __name__=="__main__":

    envset="local"
    if len(sys.argv) < 2:
        print "env must be given"
        exit(0)

    envset=sys.argv[1]
    publisher = Publisher(envset)

    publisher.test()
    publisher.publish()



