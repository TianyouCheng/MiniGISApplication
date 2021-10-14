'''
设置属性窗体
'''

from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QTableWidget,QSizePolicy,QTableWidgetItem,QHeaderView,QComboBox,QColorDialog
from PyQt5.QtGui import QBrush, QColor,QIcon
from PyQt5.QtCore import QRect,QPropertyAnimation,QPoint,QEasingCurve,QCoreApplication,Qt

def setAttr(self):

    # 分别设置表项 背景颜色 下拉框 文字
    _translate = QCoreApplication.translate
    if self.StyleOn:
        self.bt_Apply.setStyleSheet('color:white;background-color:rgb(255,255,255,0.3);')

    # Item轮廓颜色
    bt=QPushButton('')
    bt.setStyleSheet('QPushButton{margin:3px 55px 3px 0px;background-color:red}')
    bt.clicked.connect(lambda:selectcolor(self,0))
    self.AttrtableWidget.setCellWidget(0,1,bt)

    # Item轮廓样式
    combo=QComboBox()
    if self.StyleOn:
        combo.setStyleSheet('QComboBox{color:white;}QComboBox QAbstractItemView{color:white;background:rgb(255,255,255,0.6)} ')
    combo.addItem(QIcon("./UI/images/Line_G.png"),'直线')
    combo.addItems(['实线','虚线'])
    self.AttrtableWidget.setCellWidget(1,1,combo)

    # Item轮廓宽度
    item = self.AttrtableWidget.item(2, 1)
    item.setText(_translate("Form", "3"))

    # Item符号颜色
    bt = QPushButton('')
    bt.setStyleSheet('QPushButton{margin:3px 55px 3px 0px;background-color:rgb(0,255,0);}')
    bt.clicked.connect(lambda: selectcolor(self,3))
    self.AttrtableWidget.setCellWidget(3, 1, bt)


    # Item可见性
    combo = QComboBox()
    if self.StyleOn:
        combo.setStyleSheet('QComboBox{color:white;}QComboBox QAbstractItemView{color:white;background:rgb(255,255,255,0.6)} ')
    combo.addItems(['是', '否'])
    self.AttrtableWidget.setCellWidget(5, 1, combo)


    # Item绑定字段
    combo = QComboBox()
    if self.StyleOn:
        combo.setStyleSheet('QComboBox{color:white;}QComboBox QAbstractItemView{color:white;background:rgb(255,255,255,0.6)} ')
    combo.addItems(['ID', '设置动态添加'])
    self.AttrtableWidget.setCellWidget(6, 1, combo)


    # Item水平偏移
    item = self.AttrtableWidget.item(7, 1)
    item.setText(_translate("Form", "3"))


    # Item垂直偏移
    item = self.AttrtableWidget.item(8, 1)
    item.setText(_translate("Form", "3"))


    # Item字体大小
    item = self.AttrtableWidget.item(9, 1)
    item.setText(_translate("Form", "3"))


    # Item字体颜色
    item = self.AttrtableWidget.item(10, 1)
    item.setText(_translate("Form", "3"))


# 颜色对话框
def selectcolor(self,row):
    col=QColorDialog.getColor()

    # 新建一个button替换
    bt = QPushButton('')
    bt.setStyleSheet('QPushButton{margin:3px 55px 3px 0px;background-color:%s}'%col.name())
    bt.clicked.connect(lambda: selectcolor(self,row))
    self.AttrtableWidget.setCellWidget(row, 1, bt)
