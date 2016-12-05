import datetime 
import time
import argparse
import sys
import netrc
import requests, os
from requests.auth import HTTPBasicAuth
# We don't want InsecureRequest warnings:
import requests
requests.packages.urllib3.disable_warnings()
import itertools, re, sys
from jira import JIRA



__version__ = "0.1"


    
def main(argv):

    
    parser = argparse.ArgumentParser(usage="""
    {1}    Version:{0}
    


 EXAMPLE: python script.py  -t some_txt

    """.format(__version__,sys.argv[0]))

    parser.add_argument('-t','--target', help='<Print something>')
    parser.add_argument('-v','--version', help='<Version>', action='store_true')
    
    args = parser.parse_args()
        
    
    if args.version:
        print 'Tool version: %s'  % __version__
        print "DEMO FIRDAY" 
        sys.exit(2)    
         
    tparam = args.target or ''

  
    # quick old-school way to check needed parameters
    if (tparam == ""):
        parser.print_help()
        sys.exit(2)
    
    print "---------------------------------------------------------"
    print "Parameter was: {0}".format(tparam)
    print "---------------------------------------------------------"
    user, PASSWORD = Autheticate()
    DoJIRAStuff(user,PASSWORD)
    
def Autheticate():
    host="http://jira7.almdemo.fi"
    credentials = netrc.netrc()
    auth = credentials.authenticators(host)
    if auth:
        user = auth[0]
        PASSWORD = auth[2]
        print "AUTH OK: {0} {1}".format(user,auth)
    else:
        print "ERROR: .netrc file problem (Server:{0} . EXITING!".format(host)
        sys.exit(1)

    link=host
    f = requests.get(link,auth=(user, PASSWORD))
         
    # CHECK WRONG AUTHENTICATION    
    header=str(f.headers)
    HeaderCheck = re.search( r"(.*?)(AUTHENTICATION_DENIED|AUTHENTICATION_FAILED)", header)
    if HeaderCheck:
        CurrentGroups=HeaderCheck.groups()
        print ("Group 1: %s" % CurrentGroups[0]) 
        print ("Group 2: %s" % CurrentGroups[1]) 
        print ("Header: %s" % header)         
        print "--> ERROR: Apparantly user authentication gone wrong. EXITING!"
        sys.exit(1)
    else:
        print "OK - HEADER: {0}".format(header)    
    print "---------------------------------------------------------"
    return user,PASSWORD
    
def DoJIRAStuff(user,PASSWORD):
 jira_server="http://jira7.almdemo.fi"
 try:
     print("Connecting to JIRA: %s" % jira_server)
     jira_options = {'server': jira_server}
     jira = JIRA(options=jira_options,basic_auth=(user,PASSWORD))
     print "JIRA OK"
 except Exception,e:
    print("Failed to connect to JIRA: %s" % e)
    
    
    
if __name__ == "__main__":
        main(sys.argv[1:])
        
        
        
        
        