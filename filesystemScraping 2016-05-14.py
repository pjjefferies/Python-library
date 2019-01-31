# -*- coding: utf-8 -*-
"""
Created on Sat May 14 21:58:01 2016

@author: PaulJ
Derived from "http://stackoverflow.com/questions/12610456/getting-a-file-system-listing-python"
"""

def getTree(rootDir):
        tree = {}
        for path, dirs, files in os.walk(source):
            tree[path] = []
            for file in files:
                tree[path].append(file)
        return tree



def print_file_tree(tree):
    # Prepare tree
    dir_list = tree.keys()
    dir_list.sort()

    for directory in dir_list:
        print directory
        for f in tree[directory]:
            print f