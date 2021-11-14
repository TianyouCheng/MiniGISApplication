'''
设置属性窗体
'''

from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QTableWidget,QSizePolicy,QTableWidgetItem,QHeaderView,QComboBox,QColorDialog
from PyQt5.QtGui import QBrush, QColor,QIcon,QPainter,QFont
from PyQt5.QtCore import QRect,QPropertyAnimation,QPoint,QEasingCurve,QCoreApplication,Qt
from .Op_DrawLabel import RefreshCanvas
import copy

def setAttr(self):
    # TODO:设置缺省样式，黑色太难看
    # 规则：点和线使用轮廓颜色设置
    # 分别设置表项 背景颜色 下拉框 文字
    _translate = QCoreApplication.translate
    if self.StyleOn:
        self.bt_Apply.setStyleSheet('color:white;background-color:rgb(255,255,255,0.3);')
    self.bt_Apply.setFont(QFont("Microsoft YaHei", 12))
    self.bt_Apply.clicked.connect(lambda:FeatureStyle(self))

    # Item轮廓颜色
    bt=QPushButton('')
    bt.setStyleSheet('QPushButton{margin:3px 55px 3px 0px;background-color:#f5f500}')
    bt.clicked.connect(lambda:selectcolor(self,0))
    self.StyleList[0] ='black'
    self.AttrtableWidget.setCellWidget(0,1,bt)


    # Item轮廓样式
    combo=QComboBox()
    if self.StyleOn:
        combo.setStyleSheet('QComboBox{color:white;}QComboBox QAbstractItemView{color:white;background:rgb(255,255,255,0.6)} ')
    combo.addItem(QIcon("./UI/images/SolidLine.png"),'实线')
    combo.addItem(QIcon("./UI/images/DashLine.png"), '划线')
    combo.addItem(QIcon("./UI/images/DashDotLine.png"), '点划线')
    combo.addItem(QIcon("./UI/images/DotLine.png"), '点线')
    combo.addItem(QIcon("./UI/images/DashDotDotLine.png"), '点点线')
    combo.setFont(QFont("Microsoft YaHei", 11))
    self.AttrtableWidget.setCellWidget(1,1,combo)

    # Item轮廓宽度
    item = self.AttrtableWidget.item(2, 1)
    item.setText(_translate("Form", "1.5"))
    self.StyleList[2] = 1.5

    # Item填充颜色
    bt = QPushButton('')
    bt.setStyleSheet('QPushButton{margin:3px 55px 3px 0px;background-color:#6edda4;}')
    bt.clicked.connect(lambda: selectcolor(self,3))
    self.StyleList[3] = 'black'
    self.AttrtableWidget.setCellWidget(3, 1, bt)


    # Item可见性
    combo = QComboBox()
    if self.StyleOn:
        combo.setStyleSheet('QComboBox{color:white;}QComboBox QAbstractItemView{color:white;background:rgb(255,255,255,0.6)} ')
    combo.addItems(['否', '是'])
    combo.setFont(QFont("Microsoft YaHei", 11))
    self.AttrtableWidget.setCellWidget(5, 1, combo)


    # Item绑定字段
    combo = QComboBox()
    if self.StyleOn:
        combo.setStyleSheet('QComboBox{color:white;}QComboBox QAbstractItemView{color:white;background:rgb(255,255,255,0.6)} ')
    RefreshAttr(self)


    # Item水平偏移
    item = self.AttrtableWidget.item(7, 1)
    item.setText(_translate("Form", "0"))


    # Item垂直偏移
    item = self.AttrtableWidget.item(8, 1)
    item.setText(_translate("Form", "0"))


    # Item字体大小
    item = self.AttrtableWidget.item(9, 1)
    item.setText(_translate("Form", "10"))


    # Item字体颜色
    bt = QPushButton('')
    bt.setStyleSheet('QPushButton{margin:3px 55px 3px 0px;background-color:#000000;}')
    bt.clicked.connect(lambda: selectcolor(self,10))
    self.StyleList[10] = 'black'
    self.AttrtableWidget.setCellWidget(10, 1, bt)


# 颜色对话框
def selectcolor(self,row):
    col=QColorDialog.getColor()
    self.StyleList[row] =col.name()
    # 新建一个button替换
    bt = QPushButton('')
    bt.setStyleSheet('QPushButton{margin:3px 55px 3px 0px;background-color:%s}'%col.name())
    bt.clicked.connect(lambda: selectcolor(self,row))
    self.AttrtableWidget.setCellWidget(row, 1, bt)


def is_number(s):
    '''判断字符串是否为数字'''
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def FeatureStyle(self):
    '''为要素绘制符号和注记'''

    # 获取“轮廓宽度”
    item = self.AttrtableWidget.item(2, 1)
    if is_number(item.text()):
        self.StyleList[2]=float(item.text())
    else:
        raise TypeError('数值类型错误')
    # 获取“轮廓样式”的索引
    self.StyleList[1]=int(self.AttrtableWidget.cellWidget(1,1).currentIndex())
    # 获取“可见性”的索引self.StyleList[5]
    self.StyleList[5] = int(self.AttrtableWidget.cellWidget(5, 1).currentIndex())
    # 获取“绑定字段”
    self.StyleList[6]=self.AttrtableWidget.cellWidget(6, 1).currentText()
    # 获取“水平偏移”
    item = self.AttrtableWidget.item(7, 1)
    if is_number(item.text()):
        self.StyleList[7]=int(item.text())
    else:
        raise TypeError('数值类型错误')
    # 获取“垂直偏移”
    item = self.AttrtableWidget.item(8, 1)
    if is_number(item.text()):
        self.StyleList[8]=int(item.text())
    else:
        raise TypeError('数值类型错误')
    # 获取“字体大小”
    item = self.AttrtableWidget.item(9, 1)
    if is_number(item.text()):
        self.StyleList[9]=int(item.text())
    else:
        raise TypeError('数值类型错误')
    # 重绘地图
    SetStyleList(self,self.StyleList)
    RefreshCanvas(self)

def RefreshAttr(main_exe):
    '''
    动态获取绑定字段
    :param main_exe: 主窗体
    :param ind: 当前选择层index
    :return: None
    '''
    combo = QComboBox()
    combo.setFont(QFont("Microsoft YaHei", 11))
    ind=main_exe.map.selectedLayer
    if main_exe.StyleOn:
        combo.setStyleSheet('QComboBox{color:white;}QComboBox QAbstractItemView{color:white;background:rgb(255,255,255,0.6)} ')
    if ind==-1:
        combo.addItems([''])
    else:
        layer = main_exe.map.layers[ind]
        combo.addItems(layer.table.columns)
    main_exe.AttrtableWidget.setCellWidget(6, 1, combo)

def SetStyleList(main_exe,stylelist):
    # 赋样式表
    map_ = main_exe.map
    for geometry in map_.layers[map_.selectedLayer].geometries:
        selected = set(map_.layers[map_.selectedLayer].selectedItems)
        
        if geometry.ID in selected:
            geometry.StyleList = copy.deepcopy(stylelist)
            main_exe.dbm.update_style(map_.layers[map_.selectedLayer],geometry.ID,stylelist)