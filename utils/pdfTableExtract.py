from bs4 import BeautifulSoup as bs
import os
os.chdir(os.path.join('experiments', 'e1'))
fhdlr = open('table2_1.html',encoding='utf-8')
txtraw = fhdlr.read()
htmlraw = bs(txtraw,'lxml')
cells = htmlraw.find_all("div", class_="textLayer")[0].contents
cells = [e for e in cells if e.name=='div']

def styleAttributeExtract(styleText):
    pass


    

    
