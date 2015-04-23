from urllib import FancyURLopener
import re
import posixpath
import urlparse
import sys
from PyQt4.uic.uiparser import QtGui, os

from openpyxl import load_workbook

from imageh import *


class MyOpener(FancyURLopener, object):
    version = "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"

class WebViewCreator(QtGui.QDialog):
    ruta = ""
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui =Ui_Dialog()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"),self.readExcel)
        QtCore.QObject.connect(self.ui.toolButton,QtCore.SIGNAL("clicked()"),self.getruta)

    def getruta(self):
        ruote = QtGui.QFileDialog(self)
        self.ruta = ruote.getOpenFileName()
        self.ruta = str(self.ruta)
        ruote.close()
        self.ui.lineEdit.setText(self.ruta)

    def hunt(self,search):
        number = self.ui.lineEdit_2.text()
        number = int(number)
        myopener = MyOpener()
        page = myopener.open('https://www.google.es/search?q='+search+'&espv=2&biw=1366&bih=599&tbm=isch&source=lnt&tbs=isz:ex,iszw:600,iszh:400#q='+search+'&tbs=isz:ex,iszw:600,iszh:400,itp:photo,sur:fc&tbm=isch')
        html = page.read()
        i =1
        for match in re.finditer(r'<a href="http://www\.google\.es/imgres\?imgurl=(.*?)&amp;imgrefurl', html, re.IGNORECASE | re.DOTALL | re.MULTILINE):
             path = urlparse.urlsplit(match.group(1)).path
             filename = "images/"+search+str(i)+".jpg"
             if i <= number :
                 filename = posixpath.join(os.getcwd(),filename)
                 print filename
                 myopener.retrieve(match.group(1), filename)
                 i += 1
    def readExcel(self):
        print self.ruta
        wb = load_workbook(filename=self.ruta, read_only=True)
        ws = wb['Sheet1'] # ws is now an IterableWorksheet

        for row in ws.rows:
            for cell in row:
                a= cell.value
                self.hunt(a)

if __name__ == "__main__":
    app=QtGui.QApplication(sys.argv)
    myapp=WebViewCreator()
    myapp.show()
    sys.exit(app.exec_())
