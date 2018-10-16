from bs4 import BeautifulSoup as bs
import os
import numpy as np
os.chdir(os.path.join('experiments', 'e1'))
fhdlr = open('table2_1.html',encoding='utf-8')
txtraw = fhdlr.read()
fhdlr.close()
htmlraw = bs(txtraw,'lxml')
cells = htmlraw.find_all("div", class_="textLayer")[0].contents
cells = [e for e in cells if e.name=='div']

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

cells = [cell(e) for e in cells]

class table:
    def __init__(self,cells):
        self.cells = cells
        self.rowNum=0
        self.colNum = 0
        self.cursorY = 0
        for c in self.cells:
            if c.getY()>self.cursorY:
                self.rowNum = self.rowNum + 1
                self.cursorY = c.getY()
            if self.rowNum == 1:
                self.colNum = self.colNum + 1
        assert(self.rowNum*self.colNum==len(self.cells))
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

tbl = table(cells)

fhdlr = open('table2_1.csv',mode='w')
fhdlr.write(tbl.csvOutput(','))
fhdlr.close()