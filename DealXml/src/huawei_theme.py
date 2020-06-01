# coding=utf-8
'''
Created on 2020-5-30

@author: ZYM
'''

import os
import shutil
import zipfile

from xml.etree.ElementTree import ElementTree

'操作三星主题包的工具类'


class HuaweiTheme:
    ERROR_PARAMETER = "parameter is error,please check it"

    ZIP_FILE_NAME = "zhut80_EMUI9.0_20200115_2310_BigTheme.hwt"
    CONFIG_FILE_NAME = "Properties.xml"
    IMAGE_FOLDER_NAME = ""
    ZIP_TMP_FOLDER_NAME = "tmp"
    DESCRIPTION_FILE_NAME = "description.xml"
    THEME_FILE_NAME = "theme.xml"

    mPath = None

    def __init__(self, path):
        if not os.path.exists(path):
            return self.ERROR_PARAMETER

        tmp = os.path.join(path, self.ZIP_TMP_FOLDER_NAME)
        print str(tmp)
        if os.path.exists(tmp):
            shutil.rmtree(tmp)

        os.makedirs(tmp)

        t_zip = os.path.join(path, self.ZIP_FILE_NAME)
        if not os.path.exists(t_zip):
            return self.ERROR_PARAMETER

        files = zipfile.ZipFile(t_zip, "r")
        for f in files.namelist():
            files.extract(f, tmp)

        self.mPath = path

    def __get_xml_list_tag__(self, path):
        if not os.path.exists(path):
            return str(path) + ":" + str(self.ERROR_PARAMETER)

        tree = ElementTree()
        tree.parse(path);
        result = {}
        for node in tree.iter():
            print str(node.tag) + ":" + str(node.text)
            result[node.tag] = node.text

        return result

    def __get_xml_list_attr__(self, path):
        if not os.path.exists(path):
            return str(path) + ":" + str(self.ERROR_PARAMETER)

        tree = ElementTree()
        tree.parse(path);
        result = {}
        for node in tree.iter():
            print str(node.get("name")) + ":" + str(node.text)
            result[node.get("name")] = node.text

        return result

    def get_description_info(self):
        if self.mPath is None:
            return self.ERROR_PARAMETER

        tmp = os.path.join(self.mPath, self.ZIP_TMP_FOLDER_NAME,self.DESCRIPTION_FILE_NAME)
        return self.__get_xml_list_tag__(tmp)

    def get_theme_info(self, name, tfolder = None):
        tmp = os.path.join(self.mPath, self.ZIP_TMP_FOLDER_NAME)
        if tfolder is not None:
            tmp = os.path.join(tmp, tfolder)

        tmp = os.path.join(tmp, name)
        if not os.path.exists(tmp):
            z_file = os.path.join(self.mPath, self.ZIP_TMP_FOLDER_NAME, name)
            tmp = os.path.join(self.mPath, self.ZIP_TMP_FOLDER_NAME, tfolder, name)
            if not os.path.exists(tmp):
                os.makedirs(tmp)

            if not os.path.exists(z_file):
                return str(z_file) + ":" + str(self.ERROR_PARAMETER)

            files = zipfile.ZipFile(z_file, "r")
            for f in files.namelist():
                files.extract(f, tmp)

            tmp = os.path.join(tmp, self.THEME_FILE_NAME)
            return self.__get_xml_list_attr__(tmp)

