#!/usr/bin/python

from jnpr.junos import Device 
from jnpr.junos.exception import ConnectTimeoutError, ConnectAuthError
import sys

def connect(hostname, username, password):
    dev = Device(hostname, user=username, password=password) 
    try: 
	   dev.open() 
    except ConnectTimeoutError: 
	   print "Connection Timeout Error. Device: ", hostname
	   sys.exit(1)
    except ConnectAuthError:
	   print "Connection Refuse. Device: ", hostname
	   sys.exit(1)	
    print(dev.facts)
    dev.close()

def main():
    args = sys.argv[1:]
    if not args:
       print "usage: [hostname] [user] [password] ";
       sys.exit(1)
    else:
       connect(args[0],args[1],args[2]) 

if __name__ == '__main__':
	main()
