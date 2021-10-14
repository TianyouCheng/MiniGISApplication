'''
属性窗体切换动画
'''

from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QTableWidget,QSizePolicy,QTableWidgetItem,QHeaderView,QComboBox
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QRect,QPropertyAnimation,QPoint,QEasingCurve,QCoreApplication,Qt

def initAttr(self):
    '''UI里的test文件用于属性窗体的编写，编写完成后记得删除'''
    self.Attributewidget = QWidget(self.centralwidget)
    self.Attributewidget.setGeometry(QRect(-300, 232, 200, 594))
    self.Attributewidget.setObjectName("Attributewidget")
    self.Attributewidget.setStyleSheet("background-color:transparent;")
    # self.bt_test = QPushButton(self.Attributewidget)
    # self.bt_test.setGeometry(QRect(5,5,80,80))
    # self.bt_test.setText("我是按钮")
    # self.bt_test.setObjectName("bt_test")
    # self.bt_test.setStyleSheet("background-color:white;")

    self.AttrtableWidget = QTableWidget(self.Attributewidget)
    self.AttrtableWidget.setGeometry(QRect(20, 40, 159, 360))
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AttrtableWidget.sizePolicy().hasHeightForWidth())
    self.AttrtableWidget.setSizePolicy(sizePolicy)
    self.AttrtableWidget.setLineWidth(1)
    self.AttrtableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    self.AttrtableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    self.AttrtableWidget.setShowGrid(False)
    self.AttrtableWidget.setObjectName("AttrtableWidget")
    self.AttrtableWidget.setStyleSheet("border: 0px")
    self.AttrtableWidget.setColumnCount(2)
    self.AttrtableWidget.setRowCount(11)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(0, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(1, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(2, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(3, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(4, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(5, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(6, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(7, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(8, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(9, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(10, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setHorizontalHeaderItem(0, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setHorizontalHeaderItem(1, item)
    self.bt_Apply = QPushButton(self.Attributewidget)
    self.bt_Apply.setGeometry(QRect(50, 440, 101, 91))
    self.bt_Apply.setObjectName("bt_Apply")

    for i in range(self.AttrtableWidget.rowCount()):
        item=QTableWidgetItem()
        item.setFlags(Qt.ItemFlag(0))
        item.setFlags(Qt.ItemIsEnabled)
        item.setForeground(QBrush(QColor(255, 255, 255)))
        self.AttrtableWidget.setItem(i, 0, item)


        item = QTableWidgetItem()
        # 设置项的可编辑属性
        if i not in [2,7,8,9,10]:
            item.setFlags(Qt.ItemFlag(0))
            item.setFlags(Qt.ItemIsEnabled)
        item.setForeground(QBrush(QColor(255, 255, 255)))
        self.AttrtableWidget.setItem(i, 1, item)

    self.AttrtableWidget.horizontalHeader().setVisible(False)
    self.AttrtableWidget.verticalHeader().setVisible(False)
    item = self.AttrtableWidget.verticalHeaderItem(0)
    _translate = QCoreApplication.translate
    item.setText(_translate("Form", "OutlineColor"))
    item = self.AttrtableWidget.verticalHeaderItem(1)
    item.setText(_translate("Form", "OutlineStyle"))
    item = self.AttrtableWidget.verticalHeaderItem(2)
    item.setText(_translate("Form", "OutlineWidth"))
    item = self.AttrtableWidget.verticalHeaderItem(3)
    item.setText(_translate("Form", "SymbolColor"))
    item = self.AttrtableWidget.verticalHeaderItem(4)
    item.setText(_translate("Form", "注记"))
    item = self.AttrtableWidget.verticalHeaderItem(5)
    item.setText(_translate("Form", "可见性"))
    item = self.AttrtableWidget.verticalHeaderItem(6)
    item.setText(_translate("Form", "绑定字段"))
    item = self.AttrtableWidget.verticalHeaderItem(7)
    item.setText(_translate("Form", "水平偏移"))
    item = self.AttrtableWidget.verticalHeaderItem(8)
    item.setText(_translate("Form", "垂直偏移"))
    item = self.AttrtableWidget.verticalHeaderItem(9)
    item.setText(_translate("Form", "SymbolColor"))
    item = self.AttrtableWidget.verticalHeaderItem(10)
    item.setText(_translate("Form", "字体颜色"))
    item = self.AttrtableWidget.horizontalHeaderItem(0)
    item.setText(_translate("Form", "新建列"))
    item = self.AttrtableWidget.horizontalHeaderItem(1)
    item.setText(_translate("Form", "符号"))
    __sortingEnabled = self.AttrtableWidget.isSortingEnabled()
    self.AttrtableWidget.setSortingEnabled(False)
    item = self.AttrtableWidget.item(0, 0)
    item.setText(_translate("Form", "轮廓颜色"))
    item = self.AttrtableWidget.item(1, 0)
    item.setText(_translate("Form", "轮廓样式"))
    item = self.AttrtableWidget.item(2, 0)
    item.setText(_translate("Form", "轮廓宽度"))
    item = self.AttrtableWidget.item(3, 0)
    item.setText(_translate("Form", "符号颜色"))
    item = self.AttrtableWidget.item(5, 0)
    item.setText(_translate("Form", "可见性"))
    item = self.AttrtableWidget.item(6, 0)
    item.setText(_translate("Form", "绑定字段"))
    item = self.AttrtableWidget.item(7, 0)
    item.setText(_translate("Form", "水平偏移"))
    item = self.AttrtableWidget.item(8, 0)
    item.setText(_translate("Form", "垂直偏移"))
    item = self.AttrtableWidget.item(9, 0)
    item.setText(_translate("Form", "字体大小"))
    item = self.AttrtableWidget.item(10, 0)
    item.setText(_translate("Form", "字体颜色"))
    self.AttrtableWidget.setSortingEnabled(__sortingEnabled)
    self.AttrtableWidget.setColumnWidth(0, 70)
    self.AttrtableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    self.bt_Apply.setText(_translate("Form", "应用"))









def Switch(self, IsAttr, StyleOn):
    '''
    :param self: 调用主窗体各控件
    :param IsAttr: 判断当前是否为属性窗体
    :param StyleOn: 样式
    :return: None
    '''
    if not IsAttr:
        if StyleOn:
            with open('./UI/style_p.qss') as f2:
                qss = f2.read()
            self.setStyleSheet(qss)

        # 设置移动动画。move的参数是移动到的地址
        self.animition_Tree_off=QPropertyAnimation(self.treeWidget,b'pos')
        self.animition_Tree_off.setEasingCurve(QEasingCurve.InExpo)
        self.animition_Tree_off.setDuration(300)
        self.animition_Tree_off.setStartValue(QPoint(0, 0))
        self.animition_Tree_off.setEndValue(QPoint(-300, 0))
        self.animition_Tree_off.start()
        self.animition_Attr_On=QPropertyAnimation(self.Attributewidget,b'pos')
        self.animition_Attr_On.setEasingCurve(QEasingCurve.InExpo)
        self.animition_Attr_On.setDuration(300)
        self.animition_Attr_On.setStartValue(QPoint(-300, 232))
        self.animition_Attr_On.setEndValue(QPoint(1, 232))
        self.animition_Attr_On.start()
        self.IsAttr=True
    else:
        if StyleOn:
            with open('./UI/style.qss') as f2:
                qss = f2.read()
            self.setStyleSheet(qss)

        self.animition_Tree_on=QPropertyAnimation(self.treeWidget,b'pos')
        self.animition_Tree_on.setEasingCurve(QEasingCurve.InExpo)
        self.animition_Tree_on.setDuration(300)
        self.animition_Tree_on.setStartValue(QPoint(-300,0))
        self.animition_Tree_on.setEndValue(QPoint(0,0))
        self.animition_Tree_on.start()
        self.animition_Attr_Off=QPropertyAnimation(self.Attributewidget,b'pos')
        self.animition_Attr_Off.setEasingCurve(QEasingCurve.InExpo)
        self.animition_Attr_Off.setDuration(300)
        self.animition_Attr_Off.setStartValue(QPoint(1, 232))
        self.animition_Attr_Off.setEndValue(QPoint(-300, 232))
        self.animition_Attr_Off.start()
        self.IsAttr=False

