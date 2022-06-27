# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os,sys
import os.path
import csv
from datetime import datetime

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings("ignore", "Distutils was imported before Setuptools. This usage is discouraged and may exhibit undesirable behaviors or errors. Please use Setuptools' objects directly or at least import Setuptools first.",  UserWarning, "setuptools.distutils_patch")


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QDialog, QMessageBox, QVBoxLayout, QLabel, QComboBox, QCheckBox, QRadioButton, QGroupBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPixmap, QFont
#from objectdetection import objectdetection 
from posedetection import *
#import emotion_detection
import cv2

#global
working_image_path = ''
temp_show_location = 'temp.jpg'
temp = None
status = ''
ui = None
detected_keypoints = []
number_detected = 0
positives = []
negatives = []
tags = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
TP = 0
TN = 0
FP = 0
FN = 0
keypointsMapping = ['Nose', 'Neck', 'Right Shoulder', 'Right Elbow', 'Right Wrist', 'Left Shoulder', 'Left Elbow', 'Left Wrist', 'Right Hip', 'Right Knee', 'Right Ankle', 'Left Hip', 'Left Knee', 'Left Ankle', 'Right Eye', 'Left Eye', 'Right Ear', 'Left Ear']
results = []
new_picture = False

class Ui_OtherWindow(QDialog):

    def setupUi(self, OtherWindow):
        OtherWindow.setObjectName("OtherWindow")
        OtherWindow.setFixedSize(450,600)
        
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap('keypoints.png')
        pixmap_scaled_to_height = pixmap.scaled(300, 450, QtCore.Qt.KeepAspectRatio)
        item = QtWidgets.QGraphicsPixmapItem(pixmap_scaled_to_height)
        
        scene.addItem(item)
        
        self.centralwidget = QtWidgets.QWidget(OtherWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 471, 75))
        
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 90, 450, 500))
        self.graphicsView.setObjectName("graphicsView")

        self.graphicsView.setScene(scene)
        
        OtherWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(OtherWindow)
        self.statusbar.setObjectName("statusbar")
        OtherWindow.setStatusBar(self.statusbar)
        OtherWindow.setWindowIcon(QtGui.QIcon('icon.png'))

        self.retranslateUi(OtherWindow)
        QtCore.QMetaObject.connectSlotsByName(OtherWindow)

    def retranslateUi(self, OtherWindow):
        _translate = QtCore.QCoreApplication.translate
        OtherWindow.setWindowTitle(_translate("OtherWindow", "Keypoints Mapping"))
        self.label.setText(_translate("OtherWindow", "Nose – 0, Neck – 1, Right Shoulder – 2, Right Elbow – 3, Right Wrist – 4,\nLeft Shoulder – 5, Left Elbow – 6, Left Wrist – 7, Right Hip – 8,\nRight Knee – 9, Right Ankle – 10, Left Hip – 11, Left Knee – 12,\nLAnkle – 13, Right Eye – 14, Left Eye – 15, Right Ear – 16,Left Ear – 17"))

class Ui_AnalysisWindow(QDialog):

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_OtherWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, AnalysisWindow):
        AnalysisWindow.setObjectName("AnalysisWindow")
        AnalysisWindow.setFixedSize(950,800)

        global number_detected, positives, negatives, keypointsMapping, tags, TP, TN, FP, FN
        number_detected = 0
        for index in range(len(detected_keypoints)):
            if(len(detected_keypoints[index]) > 0):
                number_detected += 1
                positives.append(index)
                tags[index] = 'TP'
            else:
                negatives.append(index)
                tags[index] = 'TN'
        TP = number_detected
        TN = 18 - number_detected
        FP = 0
        FN = 0
        self.centralwidget = QtWidgets.QWidget(AnalysisWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(10, 10, 300, 30)
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(630, 10, 300, 500)
        self.label3.setFont(QFont('Sanserif', 11))
        self.label4 = QtWidgets.QLabel(self.centralwidget)
        self.label4.setGeometry(10, 50, 100, 30)
        self.label4.setText("Experiment ID: ")
        self.textbox = QLineEdit(self.centralwidget)
        self.textbox.setGeometry(100, 50, 35, 35)

        nameGroup = "groupBox"
        nameRadio = "radiobtn"
        numeration = 0
        for p in range(len(positives)):
            name1 = nameGroup + str(positives[p])
            self.name1 = QGroupBox(self.centralwidget)
            if(numeration>=10):
                self.name1.setGeometry(280, 100 + (numeration%10)*60, 250, 50)
            else:
                self.name1.setGeometry(10, 100 + numeration*60, 250, 50)
            self.name1.setTitle(keypointsMapping[positives[p]] + " (" + str(keypointsMapping.index(keypointsMapping[positives[p]])) + ") " + "is located correctly.")
            hboxLayout = QHBoxLayout()

            name2 = nameRadio + "yes" + str(positives[p]) 
            self.name2 = QRadioButton("True")
            self.name2.setChecked(True)
            hboxLayout.addWidget(self.name2)

            name3 = nameRadio + "no" + str(positives[p]) 
            self.name3 = QRadioButton("False")
            self.name3.setObjectName(str(positives[p]))
            self.name3.toggled.connect(lambda:self.radio_positive_pressed())
            hboxLayout.addWidget(self.name3)

            self.name1.setLayout(hboxLayout)
            numeration += 1
        
        positives = []

        for n in range(len(negatives)):
            name1 = nameGroup + str(negatives[n])
            self.name1 = QGroupBox(self.centralwidget)
            if(numeration>=10):
                self.name1.setGeometry(280, 100 + (numeration%10)*60, 250, 50)
            else:
                self.name1.setGeometry(10, 100 + (numeration)*60, 250, 50)
            self.name1.setTitle(keypointsMapping[negatives[n]] + " (" + str(keypointsMapping.index(keypointsMapping[negatives[n]])) + ") " + " is visible in the picture.")
            hboxLayout = QHBoxLayout()

            name2 = nameRadio + "yes" + str(negatives[n]) 
            self.name2 = QRadioButton("True")
            hboxLayout.addWidget(self.name2)

            name3 = nameRadio + "no" + str(negatives[n]) 
            self.name3 = QRadioButton("False")
            self.name3.setChecked(True)
            self.name3.setObjectName(str(negatives[n]))
            self.name3.toggled.connect(lambda:self.radio_negative_pressed())
            hboxLayout.addWidget(self.name3)

            self.name1.setLayout(hboxLayout)
            numeration += 1
        
        negatives = []

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 20, 131, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openWindow)

        AnalysisWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AnalysisWindow)
        self.statusbar.setObjectName("statusbar")
        AnalysisWindow.setStatusBar(self.statusbar)
        AnalysisWindow.setWindowIcon(QtGui.QIcon('icon.png'))

        self.label.setGeometry(QtCore.QRect(285, 100 + (numeration%10)*60, 150, 30))
        self.label.setText("Comment:")
        self.textbox2 = QLineEdit(self.centralwidget)
        self.textbox2.setGeometry(285, 100 + (numeration%10)*60 + 30, 250, 40)


        self.submit = QtWidgets.QPushButton(self.centralwidget)
        self.submit.setGeometry(QtCore.QRect(250, 710, 121, 41))
        self.submit.setObjectName("submit")

        self.submit.clicked.connect(self.submit_pressed)

        self.retranslateUi(AnalysisWindow)
        QtCore.QMetaObject.connectSlotsByName(AnalysisWindow)

    def retranslateUi(self, AnalysisWindow):
        _translate = QtCore.QCoreApplication.translate
        AnalysisWindow.setWindowTitle(_translate("AnalysisWindow", "Analysis"))
        self.pushButton.setText(_translate("MainWindow", "Show keypoints map"))
        self.submit.setText(_translate("AnalysisWindow", "Submit"))
        self.label2.setText("Using: " + str(len(detected_keypoints)) + " keypoint model\nNumber of detected keypoints: " + str(number_detected))

    #Create table
    def createTable(self, TP, TN, FP, FN):
        self.tableWidget = QTableWidget(self.centralwidget)
  
        #Row count
        self.tableWidget.setRowCount(3) 
  
        #Column count
        self.tableWidget.setColumnCount(3)

        self.tableWidget.setGeometry(630, 330, 259, 119)  
        self.tableWidget.setColumnWidth(1, 63)
        self.tableWidget.setColumnWidth(2, 63)
  
        self.tableWidget.setItem(0,0, QTableWidgetItem("Predicted\Actual"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("P"))
        self.tableWidget.setItem(0,2, QTableWidgetItem("N"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("P"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("TP = " + str(TP)))
        self.tableWidget.setItem(1,2, QTableWidgetItem("FP = " + str(FP)))
        self.tableWidget.setItem(2,0, QTableWidgetItem("N"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("FN = " + str(FN)))
        self.tableWidget.setItem(2,2, QTableWidgetItem("TN = " + str(TN)))
   
        
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)
        self.tableWidget.horizontalHeader().setVisible(False)
        #self.tableWidget.setHorizontalHeaderLabels(["HEADER 1","HEADER 2","HEADER 3"])
        self.tableWidget.show()

    def submit_pressed(self):
        accuracy = self.calculateAccuracy()
        precision = self.calculatePrecision()
        F1_score = self.calculateF1Score()
        recall = self.calculateRecall()
        comment = self.textbox2.text()
        experiment_id = self.textbox.text()
        global temp, tags, keypointsMapping, detected_keypoints, TP, FP, TN, FN
        self.label3.setText("Accuracy: " + str(round(accuracy,4)) + "\n" +"Precision: " + str(round(precision,4)) + "\n" + "F1-score: " + str(round(F1_score,4)) + "\n" + "Recall: " + str(round(recall,4)) + "\n\nConfusion matrix:\n")
        #primitivna tablica XD
        #---------------------------------------\n|       Actual       |   P    |    N   |\n---------------------------------------\n| Predicted |  P  | TP: " + str(TP) + "  FP: " + str(FP) + "\n                 |  N  | FN: " + str(FN) + "  TN: " + str(TN) + "  \n---------------------------------------
        self.createTable(TP, TN, FP, FN)
        pose_detection.connetDatabase(temp, accuracy, precision, F1_score, recall, detected_keypoints, tags, comment, experiment_id)

    #za "No" button-e
    def radio_positive_pressed(self):
        b = self.sender()
        index = int(b.objectName())
        global number_detected, tags, TP, FP, TN, FN
        if(b.isChecked()):
            FP += 1
            tags[index] = 'FP'
        else:
            FP -= 1
            tags[index] = 'TP'
        TP = number_detected - FP
        #self.label3.setText("TP: " + str(TP) + ", FP: " + str(FP) + ", TN: " + str(TN) + ", FN: " + str(FN))

    def radio_negative_pressed(self):
        b = self.sender()
        index = int(b.objectName())
        global number_detected, tags, TP, FP, TN, FN
        if(b.isChecked()):
            FN -= 1
            tags[index] = 'TN'
        else:
            FN += 1
            tags[index] = 'FN'
        TN = 18 - number_detected - FN
        #self.label3.setText("TP: " + str(TP) + ", FP: " + str(FP) + ", TN: " + str(TN) + ", FN: " + str(FN))

    # Accuracy
    def calculateAccuracy(self):
        global TP, TN, FP, FN
        return (TP + TN)/(TP + TN + FP + FN)

    # Precision, Positive Predictive Value
    def calculatePrecision(self):
        global TP, FP
        return TP/(TP + FP)

    # F1-score
    def calculateF1Score(self):
        global TP, FP, FN
        return 2*TP/(2*TP + FP + FN)

    # True Positive Rate, Recall
    def calculateRecall(self):
        global TP, FN 
        return TP/(TP + FN)


class Ui_ResultsWindow(QDialog):

    def setupUi(self, ResultsWindow):
        ResultsWindow.setObjectName("ResultsWindow")
        ResultsWindow.setFixedSize(1150,800)

        self.centralwidget = QtWidgets.QWidget(ResultsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(10, 10, 100, 30)
        self.label.setText("Experiment ID: ")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(10, 40, 100, 30)
        self.label2.setText("Image ID: ")
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(70, 120, 150, 30)
        self.label3.setFont(QFont('Sanserif', 9))
        
        self.textbox = QLineEdit(self.centralwidget)
        self.textbox.setGeometry(100, 10, 35, 25)
        self.textbox2 = QLineEdit(self.centralwidget)
        self.textbox2.setGeometry(100, 40, 35, 25)
        ResultsWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ResultsWindow)
        self.statusbar.setObjectName("statusbar")
        ResultsWindow.setStatusBar(self.statusbar)
        ResultsWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        self.fetch = QtWidgets.QPushButton(self.centralwidget)
        self.fetch.setGeometry(QtCore.QRect(150, 15, 91, 45))
        self.fetch.setObjectName("fetch")
        self.fetch.clicked.connect(self.fetch_from_db)
        self.downloadCSV = QtWidgets.QPushButton(self.centralwidget)
        self.downloadCSV.setGeometry(QtCore.QRect(385, 680, 150, 65))
        self.downloadCSV.setObjectName("downloadCSV")
        self.downloadCSV.setFont(QFont('Sanserif', 9))
        self.downloadCSV.setEnabled(False)
        self.downloadCSV.clicked.connect(self.download_as_CSV)

        self.downloadHTML = QtWidgets.QPushButton(self.centralwidget)
        self.downloadHTML.setGeometry(QtCore.QRect(600, 680, 150, 65))
        self.downloadHTML.setObjectName("downloadHTML")
        self.downloadHTML.setFont(QFont('Sanserif', 9))
        self.downloadHTML.setEnabled(False)
        self.downloadHTML.clicked.connect(self.download_as_HTML)

        self.retranslateUi(ResultsWindow)
        QtCore.QMetaObject.connectSlotsByName(ResultsWindow)

    def retranslateUi(self, ResultsWindow):
        _translate = QtCore.QCoreApplication.translate
        ResultsWindow.setWindowTitle(_translate("ResultsWindow", "Results"))
        self.fetch.setText(_translate("ResultsWindow", "Fetch"))
        self.downloadCSV.setText(_translate("ResultsWindow", "Export to CSV"))
        self.downloadHTML.setText(_translate("ResultsWindow", "Export to HTML"))

    #Create table
    def createResultsTable(self, results, averages):
        if(len(results) == 0):
            self.downloadCSV.setEnabled(False)
            self.downloadHTML.setEnabled(False)
            self.label3.setText("No results found.")
            self.resultsTable = QTableWidget(self.centralwidget)
            #Row count
            self.resultsTable.setRowCount(len(results)) 
            self.resultsTable.setGeometry(70, 150, 1000, 500)
            self.resultsTable.show() 
            return
        if(len(results) == 1):
            self.label3.setText(str(len(results)) + " row fetched:")
        else:
            self.label3.setText(str(len(results)) + " rows fetched:")
        self.resultsTable = QTableWidget(self.centralwidget)
        #Row count
        self.resultsTable.setRowCount(len(results)+2) 
        #Column count
        self.resultsTable.setColumnCount(8)

        self.resultsTable.setGeometry(70, 150, 1000, 500) 
        self.resultsTable.setColumnWidth(0, 75) 
        self.resultsTable.setColumnWidth(1, 160)
        self.resultsTable.setColumnWidth(2, 80)
        self.resultsTable.setColumnWidth(3, 80)
        self.resultsTable.setColumnWidth(4, 80)
        self.resultsTable.setColumnWidth(5, 80)
        self.resultsTable.setColumnWidth(6, 320)
        self.resultsTable.setColumnWidth(7, 115)
  
        self.resultsTable.setItem(0,0, QTableWidgetItem("Image ID"))
        self.resultsTable.setItem(0,1, QTableWidgetItem("Created at"))
        self.resultsTable.setItem(0,2, QTableWidgetItem("Accuracy"))
        self.resultsTable.setItem(0,3, QTableWidgetItem("Precision"))
        self.resultsTable.setItem(0,4, QTableWidgetItem("Recall"))
        self.resultsTable.setItem(0,5, QTableWidgetItem("F1-score"))
        self.resultsTable.setItem(0,6, QTableWidgetItem("Comment"))
        self.resultsTable.setItem(0,7, QTableWidgetItem("Experiment ID"))

        for i in range(len(results)):
            self.resultsTable.setItem(i+1,0, QTableWidgetItem(str(results[i][0])))
            #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            self.resultsTable.setItem(i+1,1, QTableWidgetItem(results[i][2].strftime("%d/%m/%Y %H:%M:%S")))
            if(results[i][7] is not None):
                self.resultsTable.setItem(i+1,6, QTableWidgetItem(results[i][7]))
            else:
                self.resultsTable.setItem(i+1,6, QTableWidgetItem(""))
            if(results[i][8] is not None):
                self.resultsTable.setItem(i+1,7, QTableWidgetItem(str(results[i][8])))
            else:
                self.resultsTable.setItem(i+1,7, QTableWidgetItem(""))

        for i in range(len(results)):
            for j in range(2,6,1):
                #float_as_str = "{:10.4f}".format(float_i_started_with)
                self.resultsTable.setItem(i+1,j, QTableWidgetItem("{:10.4f}".format(results[i][j+1])))
        font = QFont()
        font.setBold(True)
        for j in range(4):
            self.resultsTable.setItem(len(results)+1,j+2, QTableWidgetItem("{:10.2f}".format(averages[j])))
            self.resultsTable.item(len(results)+1, j+2).setFont(font)
        
        self.resultsTable.verticalHeader().setVisible(False)
        self.resultsTable.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)
        self.resultsTable.horizontalHeader().setVisible(False)
        #self.tableWidget.setHorizontalHeaderLabels(["HEADER 1","HEADER 2","HEADER 3"])
        self.resultsTable.show() 

    def fetch_from_db(self):
        experimentID = self.textbox.text()
        imageID = self.textbox2.text()
        if(len(experimentID) == 0 and len(imageID) == 0):
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No options selected.')
            error_dialog.exec_()
            return
        if (len(experimentID) != 0 and not experimentID.isdecimal() or len(imageID) != 0 and not imageID.isdecimal()):
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('ID must be type integer.')
            error_dialog.exec_()
            return
        self.downloadCSV.setEnabled(True)
        self.downloadHTML.setEnabled(True)
        self.label3.setText("")
        global results, averages
        returned = pose_detection.fetchFromDatabase(experimentID, imageID)
        results = returned[0] #array of tuples
        averages = returned[1][0] #AVG(accuracy), AVG(precision), AVG(recall), AVG(F1_score)
        self.createResultsTable(results, averages)

    def download_as_CSV(self):
        global results
        with open('results.csv', 'w', newline='') as csvfile:
            fieldnames = ['img_id', 'created_at', 'accuracy', 'precision', 'recall', 'F1_score', 'comment', 'experiment_id']
            thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            thewriter.writeheader()
            for i in range(len(results)):
                thewriter.writerow({'img_id':results[i][0], 'created_at':results[i][2].strftime("%d/%m/%Y %H:%M:%S"), 'accuracy':results[i][3], 'precision':results[i][4], 'recall':results[i][5], 'F1_score':results[i][6], 'comment':results[i][7], 'experiment_id':results[i][8]})
    
    def download_as_HTML(self):
        global results, averages
        table_content = ""
        for i in range(len(results)):
            comment = results[i][7]
            if(results[i][7] is None):
                comment = "" 
            experiment_id = results[i][8]
            if(results[i][8] is  None):
                experiment_id = ""
            table_content = table_content + """<tr>
                            <td>""" + str(results[i][0]) + """
                            <td>""" + results[i][2].strftime("%d/%m/%Y %H:%M:%S") + """</td>
                            <td>""" + str(results[i][3]) + """
                            <td>""" + str(results[i][4])+ """</td>
                            <td>""" + str(results[i][5]) + """
                            <td>""" + str(results[i][6])+ """</td>
                            <td>""" + comment + """
                            <td>""" + str(experiment_id)+ """</td>
                        </tr>"""
        #add averages in the last row
        table_content = table_content + """<tr>
                            <td></td>
                            <td></td>
                            <td><b>""" + "{:10.2f}".format(averages[0]) + """</b>
                            <td><b>""" + "{:10.2f}".format(averages[1]) + """</b></td>
                            <td><b>""" + "{:10.2f}".format(averages[2]) + """</b>
                            <td><b>""" + "{:10.2f}".format(averages[3]) + """</b></td>
                            <td></td>
                            <td></td>
                        </tr>"""

        html_str = """
        <html>
            <body>
                <table border=1>
                    <tr>
                        <th>Image ID</th>
                        <th>Created at</th>
                        <th>Accuracy</th>
                        <th>Precision</th>
                        <th>Recall</th>
                        <th>F1 score</th>
                        <th>Comment</th>
                        <th>Experiment ID</th>
                    </tr>""" + table_content + """</table>
            </body>
        </html>
        """

        Html_file= open("results.html","w")
        Html_file.write(html_str)
        Html_file.close()

class Ui_MainWindow(QDialog):

    def openAnalysis(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_AnalysisWindow()
        self.ui.setupUi(self.window)
        self.window.show()
    
    def openResults(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultsWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(990,585)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 10, 800, 550))
        self.graphicsView.setObjectName("graphicsView")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(825, 260, 131, 47))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.openAnalysis)
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(825, 200, 131, 47))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.pose_detection_action)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(835, 100, 111, 27))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.save_action)
        
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(825, 470, 141, 57))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.openResults)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(835, 40, 111, 27))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.open_action)
        
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(835, 70, 111, 27))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.reset_action)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pose Detection"))
        self.pushButton.setText(_translate("MainWindow", "Analyse Image"))
        self.pushButton_2.setText(_translate("MainWindow", "Pose detection"))
        self.pushButton_3.setText(_translate("MainWindow", "Get Results"))
        self.pushButton_3.setFont(QFont('Sanserif', 9))
        self.pushButton_4.setText(_translate("MainWindow", "Save Image"))
        self.pushButton_5.setText(_translate("MainWindow", "Select Image"))
        self.pushButton_6.setText(_translate("MainWindow", "Reset"))
    
    def showImage(self,image_path):
        global working_image_path
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap(image_path)
        pixmap_scaled_to_height = pixmap.scaled(791, 531, QtCore.Qt.KeepAspectRatio)
        item = QtWidgets.QGraphicsPixmapItem(pixmap_scaled_to_height)
        
        scene.addItem(item)
        
        self.graphicsView.setScene(scene)
        input_path_head,input_path_tail = os.path.split(working_image_path)
        h,w,c = temp.shape
        status = (input_path_tail+" :: "+str(w) + "x" + str(h))
        self.statusbar.showMessage(status)
    
    def pose_detection_action(self):
        global temp_show_location,working_image_path,temp, status
        if working_image_path == '':
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No image selected.')
            error_dialog.exec_()
        else:
            pose_cv2_obj = pose_detection.poseDetection(working_image_path)
            temp = pose_cv2_obj[0]
            global detected_keypoints
            detected_keypoints = pose_cv2_obj[1]
            self.pushButton.setEnabled(True) 
            cv2.imwrite(temp_show_location,temp)
            self.showImage(temp_show_location)
         
    def save_action(self):
        global temp_show_location
        if temp_show_location == '':
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No changes were made.')
            error_dialog.exec_()
        else:
            fd = File_Dialog()
            save_image_path = fd.saveFileDialog()
            if save_image_path == None or os.path.isdir(save_image_path):
                if save_image_path == None:
                    pass
                elif os.path.isdir(save_image_path):
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.showMessage('Invalid name/file type')
                    error_dialog.exec_()
                
            else:
                save = cv2.imread(temp_show_location)
                cv2.imwrite(save_image_path,save)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Success!")
                msg.setInformativeText("Image saved at: " + save_image_path)
                msg.setWindowTitle("Image saved!")
                msg.exec_()

    def open_action(self):
        global working_image_path,temp,temp_show_location, status
        fd = File_Dialog()
        working_image_path = fd.openFileNameDialog()
        if working_image_path == None:
            pass
        else:
            input_path_head,input_path_tail = os.path.split(working_image_path)
            temp = cv2.imread(working_image_path)
            h,w,c = temp.shape
            
            if os.path.exists(temp_show_location):
                os.remove(temp_show_location)
            
            status = (input_path_tail+" :: "+str(w) + "x" + str(h))
            self.showImage(working_image_path)
            self.statusbar.showMessage(status)
    
    def reset_action(self):
        global working_image_path,temp_show_location, status

        
        temp = cv2.imread(working_image_path)
        if(temp is None):
            return
        input_path_head,input_path_tail = os.path.split(working_image_path)
        h,w,c = temp.shape
        
        if os.path.exists(temp_show_location):
            os.remove(temp_show_location)
        
        status = (input_path_tail+" :: "+str(w) + "x" + str(h))
        self.showImage(working_image_path)
        self.statusbar.showMessage(status)
        self.pushButton.setEnabled(False)

    def show_keypoints_map_action(self):
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap('keypoints.png')
        pixmap_scaled_to_height = pixmap.scaled(591, 231, QtCore.Qt.KeepAspectRatio)
        item = QtWidgets.QGraphicsPixmapItem(pixmap_scaled_to_height)
        
        scene.addItem(item)
        
        self.graphicsView.setScene(scene)


class File_Dialog(QWidget):

    def __init__(self):
        super().__init__()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Pose Detection: Open image", "","Images (*.png *.bmp *.jpg *.jpeg)", options=options)
        head,tail = os.path.splitext(fileName)
        if tail in ['.jpg','.png','.bmp','.jpeg', '.JPG']:
            return(fileName)
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Invalid name/file type')
            error_dialog.exec_()
            return(None)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            return(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Pose detection: Save image","","Images (*.png *.bmp *.jpg *.jpeg)", options=options)
        head,tail = os.path.splitext(fileName)
        if tail in ['.jpg','.png','.bmp','.jpeg', '.JPG']:
            return(fileName)
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Invalid name/file type')
            error_dialog.exec_()
            return(None)
                     
def closeEvent():
    global temp_show_location
    if os.path.exists(temp_show_location):
        os.remove(temp_show_location)
def main():
    global working_image_path,temp,temps,ui,status
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(closeEvent)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
    
    status = ("No image selected.")

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.statusbar.showMessage(status)


    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()