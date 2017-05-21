#!/usr/bin/python

import Queue
import threading
import os
import urllib2


threads =10

#target = raw_input("Give me a target (URL): ")"http://localhost/" # URL of installed webapp or just server address
target = raw_input("Give me a target (URL): ")
#directory = "/var/www/html/" # Path to the installation in your system or web root directory
directory = raw_input("Give me a path to desired directory: ")
permissions = raw_input("Do you want me to find only stuff with X permissions? (y/n) ")
filters = [".jpg",".gif",".png",".css",".js", ".svg"] # Unwelcome extensions

os.chdir(directory)

web_paths = Queue.Queue()

for r,d,f in os.walk("."):
    for files in f:
        remote_path = "%s/%s" % (r,files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if permissions == "n" and os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)
# Searching for files with executable permissions
        if permissions == "y" and os.path.splitext(files)[1] not in filters and os.access(files, os.X_OK):
            web_paths.put(remote_path)

def remote_check():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)

        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content = response.read()
            length = len(content)

            if length >= 1:
                print "\033[1;32;40m OK [%d]\033[1;m => %s ; content-length: \033[1;31m%s\033[1;m" % (response.code,path,length)
                response.close()

        except urllib2.HTTPError as error:
            #print "Failed %s" % error.code
            pass

for i in range(threads):
    print "\033[1;33mSpawning thread: %d\033[1;m" % i
    t = threading.Thread(target=remote_check)
    t.start()
