from PyQt5.QtWidgets import*
import sys
from designer import Ui_MainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
import random
from datetime import datetime
import pandas as pd
import os

class mainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.buttonList = [self.ui.dataComB,self.ui.lightsB,self.ui.camB,self.ui.powerB]

        self.ui.dataComB.clicked.connect(self.buttons)
        self.ui.lightsB.clicked.connect(self.buttons)
        self.ui.camB.clicked.connect(self.buttons)
        self.ui.powerB.clicked.connect(self.buttons)
        self.ui.logButton.clicked.connect(self.openCsv)

        self.dataComİmages = [QPixmap("images/dataComOff.png"),QPixmap("images/dataComOn.png")]
        self.dataComOpen = False
        self.lightsİmages = [QPixmap("images/lightsOff.png"),QPixmap("images/lightsOn.png")]
        self.lightsOpen = False
        self.camİmages = [QPixmap("images/cameraOff.png"),QPixmap("images/cameraOn.png")]
        self.camOpen = False
        self.powerİmages = [QPixmap("images/powerSaveOff.png"),QPixmap("images/powerSaveOn.png")]
        self.powerOpen = False

        try:
            self.df = pd.read_csv("log.csv",encoding="utf-8-sig",sep=";")
        except:
            self.df = pd.DataFrame({"Time":[],"ButtonName":[],"Mode":[]})

    def buttons(self):
        for but in self.buttonList:
            but.setEnabled(False)

        button = self.sender()
        label = button.objectName()[:-1] + 'L'
        imageName = button.objectName()[:-1] + 'P'
        self.x = random.randint(3,9)
        self.findChild(QLabel,label).setText("veri göderiliyor.")
        self.runningT = QTimer()
        self.runningT.timeout.connect(lambda : self.buttonAnim(label,button.text(),imageName))
        self.runningT.start(250)

    def buttonAnim(self,_label,butText,imageName):
        label = self.findChild(QLabel,_label)
        if label.text()[-3:] != "...":
            label.setText(label.text()+'.')
        else:
            label.setText("veri göderiliyor.")
        self.x-=1
        if self.x==0:
            label.setText("")
            for but in self.buttonList:
                but.setEnabled(True)
            self.runningT.stop()
            self.isSucceed(butText,imageName)
        
    def isSucceed(self,butText,imageName):
        y = random.randint(0,3)
        if y != 0:
            try:
                self.itSucceed(imageName,butText)
            except PermissionError:
                msg = QMessageBox()
                msg.setWindowTitle("Command Error")
                msg.setText("Komut Gönderilemedi")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setInformativeText("arkada log.csv dosyası çalışıyor")
                x = msg.exec_()
        else:
            self.itNotSucceed(butText)

    def itSucceed(self,imageName,butText):
        image = self.findChild(QLabel,imageName)
        if imageName == "dataComP":
            self.dataComOpen = not self.dataComOpen
            self.writeCsvInfo(butText,self.dataComOpen)
            image.setPixmap(self.dataComİmages[self.dataComOpen])
        elif imageName == "lightsP":
            self.lightsOpen = not self.lightsOpen
            self.writeCsvInfo(butText,self.lightsOpen)
            image.setPixmap(self.lightsİmages[self.lightsOpen])
        elif imageName == "camP":
            self.camOpen = not self.camOpen
            self.writeCsvInfo(butText,self.camOpen)
            image.setPixmap(self.camİmages[self.camOpen])
        elif imageName == "powerP":
            self.powerOpen = not self.powerOpen
            self.writeCsvInfo(butText,self.powerOpen)
            image.setPixmap(self.powerİmages[self.powerOpen])
        
    def itNotSucceed(self,butText):
        msg = QMessageBox()
        msg.setWindowTitle("Command Error")
        msg.setText("Komut Gönderilemedi")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setInformativeText(str(butText).replace("\n"," ") + " komut isteği başarısız oldu!")
        x = msg.exec_()

    def writeCsvInfo(self,butText,isOpen):
        self.df.loc[len(self.df)] = pd.Series({'Time':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'ButtonName':str(butText).replace("\n"," "),'Mode':isOpen})
        self.df.to_csv("log.csv",encoding="utf-8-sig",index=False,sep=";")

    def openCsv(self):
        try:
            os.startfile("log.csv")
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Log Error")
            msg.setText("Log Klasörü Açılamadı")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setInformativeText("log.csv dosyası bulunamadı")
            x = msg.exec_()

app = QApplication(sys.argv)
win = mainWindow()
win.show()
sys.exit(app.exec_())