# coding=utf-8
'''
Created on 2020-5-30

@author: ZYM
'''

import os
import shutil
import zipfile
from xml.dom import minidom

'操作三星主题包的工具类'


class SamsungTheme:
    ERROR_UNINITIALIZED = "uninitialized please call construction method"
    ERROR_PARAMETER = "parameter is error,pleas check it"
    ERROR_NOTHING = "do nothing, please check parameter first"

    ZIP_FILE_NAME = ""
    CONFIG_FILE_NAME = "Properties.xml"
    IMAGE_FOLDER_NAME = ""
    mDocumentTree = minidom.Document()
    mRoot = None
    mPath = None

    # 类构造方法
    def __init__(self, path):
        if not os.path.exists(path):
            print "path is not exists"
            return

        if not os.path.isdir(path):
            print self.ERROR_PARAMETER
            return

        print "Sansung path:" + str(path)
        self.__delete_files__(path)

        tmp = os.path.join(path, self.ZIP_FILE_NAME)
        if not os.path.exists(tmp):
            print self.ERROR_PARAMETER
            return

        tmp = zipfile.ZipFile(tmp, "r")
        for f in tmp.namelist():
            tmp.extract(f, path)

        self.mPath = path
        tmp = os.path.join(path, self.CONFIG_FILE_NAME)
        self.mDocumentTree = minidom.parse(tmp)
        self.mRoot = self.mDocumentTree.documentElement

    def __delete_files__(self, path):
        tmp = os.path.join(path, self.CONFIG_FILE_NAME)
        if os.path.exists(tmp):
            os.remove(tmp)

        tmp = os.path.join(path, self.IMAGE_FOLDER_NAME)
        if os.path.exists(tmp):
            if not os.path.isdir(tmp):
                return

            shutil.rmtree(tmp)

    def set_theme_property(self, element, key, value):
        if self.mRoot is None:
            return self.ERROR_UNINITIALIZED

        print " Element:" + str(element) + " Key:" + str(key) + " Value:" + value
        elements = self.mRoot.getElementsByTagName(element)
        print str(elements)
        for node in elements:
            node.setAttribute(key, value)

    def set_theme_color(self, element, uid, value):
        if self.mRoot is None:
            return self.ERROR_UNINITIALIZED

        print " Element:" + str(element) + " Key:" + str(uid) + " Value:" + str(value)
        elements = self.mRoot.getElementsByTagName(element)
        print str(elements)
        for node in elements:
            if node.getAttribute('UID') == uid:
                print str(node.getAttribute('UID'))
                node.setAttribute(uid, value)

    def set_theme_bitmap(self, path, element, uid, name):
        if self.mRoot is None:
            return self.ERROR_UNINITIALIZED

        print "Path" + str(path) + " Element:" + str(element) + " Key:" + str(uid) + " Name:" + str(name)
        elements = self.mRoot.getElementsByTagName(element)
        print str(elements)
        for node in elements:
            if node.getAttribute('UID') == uid:
                print str(node.getAttribute('UID'))
                node.setAttribute(uid, name)
                des = os.path.join(self.mPath, self.IMAGE_FOLDER_NAME, name)
                # 复制图片文件到指定文件夹并重命名
                shutil.copy(path, des)
                return None
        return self.ERROR_NOTHING

