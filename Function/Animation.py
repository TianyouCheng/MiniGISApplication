'''
属性窗体切换动画
'''

from PyQt5.QtWidgets import QWidget,QPushButton,QLabel
# from PyQt5.QtGui import *
from PyQt5.QtCore import QRect,QPropertyAnimation,QPoint,QEasingCurve,QCoreApplication

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
    self.Attrlabel_Symbol = QLabel(self.Attributewidget)
    self.Attrlabel_Symbol.setGeometry(QRect(20, 60, 54, 12))
    self.Attrlabel_Symbol.setObjectName("Attrlabel_Symbol")
    self.Attrlabel_Soutliecolor = QLabel(self.Attributewidget)
    self.Attrlabel_Soutliecolor.setGeometry(QRect(30, 90, 81, 16))
    self.Attrlabel_Soutliecolor.setObjectName("Attrlabel_Soutliecolor")
    self.Attrlabel_Soutlinestyle = QLabel(self.Attributewidget)
    self.Attrlabel_Soutlinestyle.setGeometry(QRect(30, 120, 81, 16))
    self.Attrlabel_Soutlinestyle.setObjectName("Attrlabel_Soutlinestyle")
    self.Attrlabel_Soutlinewidth = QLabel(self.Attributewidget)
    self.Attrlabel_Soutlinewidth.setGeometry(QRect(30, 150, 81, 16))
    self.Attrlabel_Soutlinewidth.setObjectName("Attrlabel_Soutlinewidth")
    self.Attrlabel_Ssymbolcoor = QLabel(self.Attributewidget)
    self.Attrlabel_Ssymbolcoor.setGeometry(QRect(30, 180, 81, 16))
    self.Attrlabel_Ssymbolcoor.setObjectName("Attrlabel_Ssymbolcoor")
    self.Attrlabel_Mark = QLabel(self.Attributewidget)
    self.Attrlabel_Mark.setGeometry(QRect(20, 210, 81, 16))
    self.Attrlabel_Mark.setObjectName("Attrlabel_Mark")
    self.Attrlabel_Mvisible = QLabel(self.Attributewidget)
    self.Attrlabel_Mvisible.setGeometry(QRect(30, 240, 81, 16))
    self.Attrlabel_Mvisible.setObjectName("Attrlabel_Mvisible")
    self.Attrlabel_Mfield =QLabel(self.Attributewidget)
    self.Attrlabel_Mfield.setGeometry(QRect(30, 270, 81, 16))
    self.Attrlabel_Mfield.setObjectName("Attrlabel_Mfield")
    self.Attrlabel_Mxoffset = QLabel(self.Attributewidget)
    self.Attrlabel_Mxoffset.setGeometry(QRect(30, 300, 81, 16))
    self.Attrlabel_Mxoffset.setObjectName("Attrlabel_Mxoffset")
    self.Attrlabel_Myoffset = QLabel(self.Attributewidget)
    self.Attrlabel_Myoffset.setGeometry(QRect(30, 330, 81, 16))
    self.Attrlabel_Myoffset.setObjectName("Attrlabel_Myoffset")
    self.Attrlabel_Msymbolcolor = QLabel(self.Attributewidget)
    self.Attrlabel_Msymbolcolor.setGeometry(QRect(30, 360, 81, 16))
    self.Attrlabel_Msymbolcolor.setObjectName("Attrlabel_Msymbolcolor")
    self.Attrlabel_Msize = QLabel(self.Attributewidget)
    self.Attrlabel_Msize.setGeometry(QRect(30, 390, 81, 16))
    self.Attrlabel_Msize.setObjectName("Attrlabel_Msize")
    self.Attrlabel_Mcolor = QLabel(self.Attributewidget)
    self.Attrlabel_Mcolor.setGeometry(QRect(30, 420, 81, 16))
    self.Attrlabel_Mcolor.setObjectName("Attrlabel_Mcolor")
    _translate = QCoreApplication.translate
    self.Attrlabel_Symbol.setText(_translate("Form", "符号"))
    self.Attrlabel_Soutliecolor.setText(_translate("Form", "OutlineColor"))
    self.Attrlabel_Soutlinestyle.setText(_translate("Form", "OutlineStyle"))
    self.Attrlabel_Soutlinewidth.setText(_translate("Form", "OutlineWidth"))
    self.Attrlabel_Ssymbolcoor.setText(_translate("Form", "SymbolColor"))
    self.Attrlabel_Mark.setText(_translate("Form", "注记"))
    self.Attrlabel_Mvisible.setText(_translate("Form", "可见性"))
    self.Attrlabel_Mfield.setText(_translate("Form", "绑定字段"))
    self.Attrlabel_Mxoffset.setText(_translate("Form", "水平偏移"))
    self.Attrlabel_Myoffset.setText(_translate("Form", "垂直偏移"))
    self.Attrlabel_Msymbolcolor.setText(_translate("Form", "SymbolColor"))
    self.Attrlabel_Msize.setText(_translate("Form", "字体大小"))
    self.Attrlabel_Mcolor.setText(_translate("Form", "字体颜色"))

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

