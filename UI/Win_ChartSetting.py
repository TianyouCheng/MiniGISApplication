# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Win_ChartSetting.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Win_Chart(object):
    def setupUi(self, Win_Chart):
        Win_Chart.setObjectName("Win_Chart")
        Win_Chart.resize(456, 263)
        self.bt_OK = QtWidgets.QPushButton(Win_Chart)
        self.bt_OK.setGeometry(QtCore.QRect(110, 160, 81, 51))
        self.bt_OK.setObjectName("bt_OK")
        self.bt_Cancel = QtWidgets.QPushButton(Win_Chart)
        self.bt_Cancel.setGeometry(QtCore.QRect(250, 160, 81, 51))
        self.bt_Cancel.setObjectName("bt_Cancel")
        self.label_2 = QtWidgets.QLabel(Win_Chart)
        self.label_2.setGeometry(QtCore.QRect(90, 50, 132, 20))
        self.label_2.setObjectName("label_2")
        self.comboBox_2 = QtWidgets.QComboBox(Win_Chart)
        self.comboBox_2.setGeometry(QtCore.QRect(230, 50, 131, 20))
        self.comboBox_2.setObjectName("comboBox_2")
        self.widget = QtWidgets.QWidget(Win_Chart)
        self.widget.setGeometry(QtCore.QRect(90, 90, 271, 22))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)

        self.retranslateUi(Win_Chart)
        QtCore.QMetaObject.connectSlotsByName(Win_Chart)

    def retranslateUi(self, Win_Chart):
        _translate = QtCore.QCoreApplication.translate
        Win_Chart.setWindowTitle(_translate("Win_Chart", "ChartSettings"))
        self.bt_OK.setText(_translate("Win_Chart", "确定"))
        self.bt_Cancel.setText(_translate("Win_Chart", "取消"))
        self.label_2.setText(_translate("Win_Chart", "标识字段"))
        self.label.setText(_translate("Win_Chart", "统计字段"))