#coding=utf-8
'''
Created on 2020-5-30

@author: ZYM
'''

import os
from xml.dom import minidom

class Samsung:
    '操作三星主题包的工具类'
    mDocumentTree = minidom.Document()
    mRoot = 0;

    #类构造方法
    def __init__(self, path):
        if not os.path.exists(path):
            print "path is not exists"
            return

        print "Sansung path:" + str(path)
        self.mDocumentTree = minidom.parse(path)
        self.mRoot = self.mDocumentTree.documentElement


    def setPropery(self, element, key, value):
        if self.mRoot is 0:
            return;