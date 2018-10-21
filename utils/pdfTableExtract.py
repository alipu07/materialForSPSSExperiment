from bs4 import BeautifulSoup as bs
import os
import numpy as np

import argparse
ap = argparse.ArgumentParser()
ap.add_argument('-e','--expname',default='3',help='experiment name')
ap.add_argument('-t','--table',type=str,default='1',help='data table name')
args = vars(ap.parse_args())

os.chdir(os.path.join('experiments', f'e{args["expname"]}'))
fhdlr = open(f'table{args["expname"]}_{args["table"]}.html',encoding='utf-8')
txtraw = fhdlr.read()
fhdlr.close()
htmlraw = bs(txtraw,'html.parser')
cells = htmlraw.find_all("div", class_="textLayer")
cellsContents = [e.find_all("div") for e in cells]

# reduce contents
def combineArr(a):
    rst = []
    for e in a:
        rst = rst+e
    return rst
cellsContents = combineArr(cellsContents)


# for e in cells[:1]:
#     style = styleAttributeExtract(e)
#     location = (pxRemove(style['left']),pxRemove(style['top']))
#     content = e.string
#     print(f'{content} @ {location}')    
    
class cell:
    def __init__(self,htmltxt):
        self.htmltxt = htmltxt
        self.string = htmltxt.string
        self.attrs = attribute(htmltxt)
        self.location = self.attrs.getLocation()
    def __str__(self):
        return self.string
    def __repr__(self):
        return self.string
    def getX(self):
        return self.location[0]
    def getY(self):
        return self.location[1]
    
    
class attribute:
    def __init__(self,attrTxt):
        self.attrs = self.styleAttributeExtract(attrTxt)

    def __pxRemove(self,txt):
        num = txt[:-2]
        return float(num)

    def styleAttributeExtract(self,styleText):
        style = styleText["style"].split(";")
        styleDict = {}
        for e in style:
            if ":" in e:
                keyvaluePair = [val.strip() for val in e.split(":")]
                styleDict[keyvaluePair[0]]=keyvaluePair[1]
        return styleDict

    def getAttr(self,attrName):
        if "px" in self.attrs[attrName]:
            return self.__pxRemove(self.attrs[attrName])
        else:
            return self.attrs[attrName]
    def getLocation(self):
        return (self.getAttr('left'),self.getAttr('top'))


class table:
    def __init__(self,cells):
        self.cells = cells
        self.rowNum=0
        self.colNum = 0
        self.cursorY = 0
        for c in self.cells:
            if not c.getY()==self.cursorY:
            # 当出现分页的时候新一行的Y会比上一行小，所以原来的c.getY()==self.cursorY会出错
                self.rowNum = self.rowNum + 1
                self.cursorY = c.getY()
            if self.rowNum == 1:
                self.colNum = self.colNum + 1
        assert self.rowNum*self.colNum==len(self.cells), print(f'col:{self.colNum},row:{self.rowNum}, len:{len(self.cells)}')
        self.cellContent = [str(cell) for cell in cells]
        self.tableNp = np.array(self.cells).reshape(self.rowNum,self.colNum)
    def csvOutput(self,sep):
        outputTxt = ""
        assert(self.rowNum>0)
        for row in self.tableNp:
            outputTxt += sep.join([str(e) for e in row])
            outputTxt += "\n"
        return outputTxt
    def getTableNp(self):
        return self.tableNp

cellsContents = [cell(e) for e in cellsContents]
tbl = table(cellsContents)

fhdlr = open(f'table{args["expname"]}_{args["table"]}.csv',mode='w')
fhdlr.write(tbl.csvOutput(','))
fhdlr.close()