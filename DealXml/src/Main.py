#coding=utf-8
'''
Created on 2020-5-30

@author: ZYM
'''

import os,sys
import xlrd
import zipfile
from xml.etree.ElementTree import ElementTree,Element
from xml.dom import minidom

import Sansung

def ReadExcelData(path, sheetIndex):
    if os.path.exists(path):
        print "huawei config is exists"
        try:
            data = xlrd.open_workbook(path)
            table = data.sheets()[sheetIndex]
            nrows = table.nrows
            ncols = table.ncols
            print str(nrows) + "  " + str(ncols)
            list = []
            firstData = table.row_values(0);
            for i in range(1, nrows):
                rValues = table.row_values(i)
                values = {}
                for j in range(0, ncols):
                    values[firstData[j]] = rValues[j]

                print str(values)
                list.append(values)

            return list
        except Exception, e:
            print str(e)
    else:
        print "huawei config is not exists"


def ExtractZipFile(path, name):
    filePath = path + "/" + name;
    if os.path.exists(filePath):
        print filePath + " is exists"
        tmpFile = zipfile.ZipFile(filePath, "r")
        for file in tmpFile.namelist():
            tmpFile.extract(file, os.getcwd() + "/tmp")
    else:
        print filePath + " is not exists"


def ParseXmlFile(path):
    if not os.path.exists(path):
        print path + " is not exist"
        return

    print "start parse " + path
    tree = ElementTree()
    tree.parse(path);
    map = {}
    for node in tree.iter():
        print str(node.tag) + ":" + str(node.text)
        map[node.tag] = node.text

    return map


def OpenXmlByDom(path, element, key, value, uid=None):
    print "Path:" + str(path) + " Element:" + str(element) + " Key:" + str(key) + " Value:" + value
    if not os.path.exists(path):
        print path + " is not exist"
        return

    print "find note by:" + path
    dom = minidom.Document()
    dom = minidom.parse(path)
    root = dom.documentElement
    elements = root.getElementsByTagName(element)
    print str(elements)
    for node in elements:
        if uid is None:
            node.setAttribute(key, value);
        else:
            if(node.getAttribute('UID')==uid):
                print str(node.getAttribute('UID'))
                node.setAttribute(key, value);

    try:
        with open(path, 'w') as fh:
            # 4.writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
            # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
            dom.writexml(fh, encoding='UTF-8')
            print('OK')
    except Exception as err:
        print('错误：{err}'.format(err=err))



def dealDescriptionXml(format, map, newConfig):
    for i in range(len(format)):
        key = format[i].get("Key")
        huawei = format[i].get("Huawei")
        value = map.get(huawei)
        if(format[i].get("Trim") == 1):
            value = value.replace(" ", "")

        sub = format[i].get("Sub")
        if(sub > 0):
            print str(sub)
            value = value[int(sub):]

        value = format[i].get("Prefix") + value
        element = format[i].get("Element")
        OpenXmlByDom(newConfig, element, key, value)




def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    tmpPath = os.getcwd() + "/tmp"
    if not os.path.exists(tmpPath):
        os.makedirs(tmpPath)

    print "当前执行根目录为：" + os.getcwd()
    #读取圈梁配置文件 也就是说那些文件需要使用，不使用的文件不需要配置
    configPath = os.getcwd() + "/huawei_config.xlsx"
    mainData = ReadExcelData(configPath, 0)
    print str(mainData)

    zipFile = os.getcwd() + "/data"
    zipName = mainData[0].get("filename")
    ExtractZipFile(zipFile, zipName);

    xmlPath = tmpPath + "/" + mainData[1].get("filename")
    map = ParseXmlFile(xmlPath)
    print str(map)

    newConfig = os.getcwd() + "/Properties.xml"
    format = ReadExcelData(configPath, int(mainData[1].get("index")))
    print str(format)
    dealDescriptionXml(format, map, newConfig)

    sansung = Sansung(configPath)




if __name__=="__main__":
    main()
