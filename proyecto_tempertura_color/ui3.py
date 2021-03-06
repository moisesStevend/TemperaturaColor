from PyQt4 import QtCore, QtGui
import RPi.GPIO as GPIO
#import matplotlib.pyplot as plt
import io
import time
import picamera
import cv2
import numpy as np
import colour

def offRed():
    GPIO.output(ledPinRed1, GPIO.LOW)
    GPIO.output(ledPinRed2, GPIO.LOW)

def onRed():
    GPIO.output(ledPinRed1, GPIO.HIGH)
    GPIO.output(ledPinRed2, GPIO.HIGH)

def onBlue():
    GPIO.output(ledPinBlue1, GPIO.HIGH)
    GPIO.output(ledPinBlue2, GPIO.HIGH)
    
def offBlue():
    GPIO.output(ledPinBlue1, GPIO.LOW)
    GPIO.output(ledPinBlue2, GPIO.LOW)
    
ledPinRed1 = 18 #
ledPinRed2 = 12 #

ledPinBlue1 = 23 #
ledPinBlue2 = 24#

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

GPIO.setup(ledPinRed1, GPIO.OUT) # LED pin set as output
GPIO.setup(ledPinRed2, GPIO.OUT) # LED pin set as output
GPIO.setup(ledPinBlue1, GPIO.OUT) # LED pin set as output
GPIO.setup(ledPinBlue2, GPIO.OUT) # LED pin set as output

offRed()
offBlue()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
	def __init__(self):
		offRed()
		offBlue()
		self.color = None
		self.CCT = None
		
	def on_click(self):#red
		self.color = 'red'
		self.pushButton_4.setStyleSheet(_fromUtf8("background-color: rgb(255, 0, 0);"))
		offRed()
		offBlue()
		onRed()
		print(self.color)
	
	def on_click2(self):
		self.color = 'green'
		self.pushButton_4.setStyleSheet(_fromUtf8("background-color: rgb(0, 255, 0);"))
		print(self.color)
	
	def on_click3(self):
		self.color = 'blue'
		self.pushButton_4.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);"))
		offRed()
		offBlue()
		onBlue()
		print(self.color)
	
	def on_click4(self):#foto
		stream = io.BytesIO()
		with picamera.PiCamera() as camera:
			camera.start_preview()
			time.sleep(2)
			camera.capture(stream, format='jpeg')
		# Construct a numpy array from the stream
		data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
		# "Decode" the image from the array, preserving colour
		image = cv2.imdecode(data, 1)
		# OpenCV returns an array with data in BGR order. If you want RGB instead
		# use the following...
		image = image[:, :, ::-1]
		cv2.imwrite('original.png',image)
		
		pixmap = QtGui.QPixmap('./original.png').scaled(200, 180, QtCore.Qt.KeepAspectRatio)
		self.label_3.setPixmap(pixmap)
		
		image = image[150:190, 300:360]
		cv2.imwrite('escala.png',image)
		
		pixmap = QtGui.QPixmap('./escala.png').scaled(200, 180, QtCore.Qt.KeepAspectRatio)
		self.label_4.setPixmap(pixmap)
		
		###########################################################
		#Promedio de pixeles#######################################
		###########################################################
		r=image[:,:,0]
		g=image[:,:,1]
		b=image[:,:,2]

		rp = r.sum()/(r.shape[0]*r.shape[1])
		gp = g.sum()/(g.shape[0]*g.shape[1])
		bp = b.sum()/(b.shape[0]*b.shape[1])
		###########################################################
		#uso de la libreria colour-science para hallar los kelvin##
		############################################################
		RGB = np.array([rp,gp,bp])

		# Conversion to tristimulus values.
		XYZ = colour.sRGB_to_XYZ(RGB /255)

		# Conversion to chromaticity coordinates.
		xy = colour.XYZ_to_xy(XYZ)

		# Conversion to correlated colour temperature in K.
		CCT = colour.temperature.xy_to_CCT_Hernandez1999(xy)
		#rp,gp,bp
		self.CCT = CCT
		if self.CCT < 0:
			self.label_5.setText(_translate("MainWindow", "KELVIN OUT: "+str("intenta de nuevo"), None))
		self.label_5.setText(_translate("MainWindow", "KELVIN OUT: "+str(round(self.CCT)), None))
		
		offRed()
		offBlue()	
		self.pushButton_4.setStyleSheet(_fromUtf8("background-color: rgb(29, 29, 29);"))
		print(self.CCT)
			
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(732, 505)
		MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(159, 159, 159);"))
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.pushButton = QtGui.QPushButton(self.centralwidget)
		self.pushButton.setGeometry(QtCore.QRect(60, 70, 151, 61))
		self.pushButton.setStyleSheet(_fromUtf8("font: italic 20pt \"Ubuntu\";\n"
"background-color: rgb(255, 0, 0);"))
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.pushButton.clicked.connect(self.on_click)
        
		self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_2.setGeometry(QtCore.QRect(60, 170, 151, 61))
		self.pushButton_2.setStyleSheet(_fromUtf8("font: italic 20pt \"Ubuntu\";\n"
"background-color: rgb(0, 255, 0);"))
		self.pushButton_2.clicked.connect(self.on_click2)

		self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
		self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_3.setGeometry(QtCore.QRect(60, 290, 151, 61))
		self.pushButton_3.setStyleSheet(_fromUtf8("font: italic 20pt \"Ubuntu\";\n"
"background-color: rgb(0, 0, 255);"))
		self.pushButton_3.clicked.connect(self.on_click3)
		
		self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
		self.verticalSlider = QtGui.QSlider(self.centralwidget)
		self.verticalSlider.setGeometry(QtCore.QRect(20, 60, 21, 81))
		self.verticalSlider.setStyleSheet(_fromUtf8("gridline-color: rgb(255, 255, 255);"))
		self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
		self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
		self.verticalSlider_2 = QtGui.QSlider(self.centralwidget)
		self.verticalSlider_2.setGeometry(QtCore.QRect(20, 160, 21, 81))
		self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
		self.verticalSlider_2.setObjectName(_fromUtf8("verticalSlider_2"))
		self.verticalSlider_3 = QtGui.QSlider(self.centralwidget)
		self.verticalSlider_3.setGeometry(QtCore.QRect(20, 280, 21, 81))
		self.verticalSlider_3.setOrientation(QtCore.Qt.Vertical)
		self.verticalSlider_3.setObjectName(_fromUtf8("verticalSlider_3"))
		self.label = QtGui.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(260, 30, 211, 21))
		self.label.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);\n"
"font: italic 14pt \"Ubuntu\";"))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(490, 30, 211, 21))
		self.label_2.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);\n"
"font: italic 14pt \"Ubuntu\";"))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_3 = QtGui.QLabel(self.centralwidget)
		self.label_3.setGeometry(QtCore.QRect(260, 70, 201, 181))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QtGui.QLabel(self.centralwidget)
		self.label_4.setGeometry(QtCore.QRect(490, 70, 201, 181))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_4.clicked.connect(self.on_click4)
		
		self.pushButton_4.setGeometry(QtCore.QRect(260, 340, 151, 71))
		self.pushButton_4.setStyleSheet(_fromUtf8("background-color: rgb(29, 29, 29);"))
		self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
		self.label_5 = QtGui.QLabel(self.centralwidget)
		self.label_5.setGeometry(QtCore.QRect(475, 346, 191, 61))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.pushButton.setToolTip(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        
		self.pushButton.setText(_translate("MainWindow", "RED", None))
		self.pushButton_2.setText(_translate("MainWindow", "GREEN", None))
		self.pushButton_3.setText(_translate("MainWindow", "BLUE", None))
        
		self.label.setText(_translate("MainWindow", "FOTO ORIGINAL", None))
		self.label_2.setText(_translate("MainWindow", "FOTO SEGMENTADA", None))
		self.label_3.setText(_translate("MainWindow", "", None))
		self.label_4.setText(_translate("MainWindow", "", None))
		self.pushButton_4.setText(_translate("MainWindow", "FOTO", None))
		self.label_5.setText(_translate("MainWindow", "KELVIN OUT", None))
		
		#exit_action = QtGui.QAction(MainWindow)
		#exit_action.triggered.connect(self.close)
	
	def closeEvent(self, event):
		print("exit")
		offRed()
		offBlue()		
		

#import COLOR_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    offRed()
    offBlue()
    sys.exit(app.exec_())

