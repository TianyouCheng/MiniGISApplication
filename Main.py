import os,sys,random,cgitb
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from time import sleep

#region 引入窗体及函数
from UI import *
from Function import *
#endregion

# 主窗体操作
class Main_exe(QMainWindow,Ui_MainWindow):
    def __init__(self):
        # 创建窗体
        super(Main_exe,self).__init__()
        self.setupUi(self)

        # 属性
        self.EditStatus=False # 是否启用编辑
        self.LayerIndex = 1 # 每层的id

        # 绑定信号与槽函数
        self.slot_connect()

        # 创建画布
        # canvas.size()这个取出来的size不对，是（100，500）,实际是（879，500）
        canvas=QtGui.QPixmap(QtCore.QSize(879, 500))
        canvas.fill(QColor('white'))
        self.label.setPixmap(canvas)

        # 绘图函数
        self.draw_something()

        # 设置TabelView,必须设置有几列
        TableView_Init(self,5)

        # 设置TreeView
        TreeView_Init(self)




    # region 功能函数
    # 绑定信号与槽函数
    def slot_connect(self):
        self.tsButtonEdit.clicked.connect(self.bt_edit_clicked)
        self.tsButtonNewLayer.clicked.connect(self.bt_newlayer_clicked)

    # 坐标转换，将事件E的坐标转换到画布坐标上
    def ConvertCor(self,e):
        point = e.globalPos()
        point = self.label.mapFromGlobal(point)
        return point

    # 绘图
    def draw_something(self,object='null'):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)
        '''
       def draw(painter,object=None,list=[]):
        判断传入几何体的类型并绘制全部或list中的部分; 适用于所有自定义的几何类
       :param painter: 画笔
       :param object: 几何体对象
       :param list: 对于多线和多面，具体绘制哪些（可选）; 传索引不是传序号（即从0开始）
       :return: None
       '''
        draw(painter,PointD(50,50))
        painter.end()

    def mouseMoveEvent(self, e):
        painter = QtGui.QPainter(self.label.pixmap())
        # painter.setPen(QtGui.QColor('white'))
        point=self.ConvertCor(e)
        if self.EditStatus:
            painter.drawPoint(point.x(), point.y())
            painter.end()
            self.update()
    # endregion

    # region 信号与槽函数
    def bt_edit_clicked(self):
        node=self.treeWidget.currentItem()
        if not(node):
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n请先选择要编辑的图层。\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
        else:
            self.EditStatus=not(self.EditStatus)
            if self.EditStatus:
                msgBox = QMessageBox()
                msgBox.setWindowTitle(u'提示')
                txtname = self.treeWidget.currentItem().text(0)
                txttype = self.treeWidget.currentItem().child(0).text(0)
                msgBox.setText(u"\n您现在编辑的是：\n" + txtname + txttype + "对象图层。\n")
                msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
                # 隐藏ok按钮
                msgBox.addButton(QMessageBox.Ok)
                # 模态对话框
                msgBox.exec_()
                self.tsButtonEdit.setText("正在编辑")

            elif not self.EditStatus:self.tsButtonEdit.setText("编辑模式")

    def bt_newlayer_clicked(self):
        self.Winnewlayer=WinNewLayer()
        # 设置Combox
        self.Winnewlayer.comboBox.setItemIcon(0,QIcon('./UI/Point.png'))
        self.Winnewlayer.comboBox.setItemIcon(1, QIcon('./UI/Line.png'))
        self.Winnewlayer.comboBox.setItemIcon(2, QIcon('./UI/Polygon.png'))
        self.Winnewlayer.show()
        self.Winnewlayer.bt_OK.clicked.connect(self.NewLayer)
        self.Winnewlayer.bt_Cancel.clicked.connect(self.Winnewlayer.close)
        # txt=self.treeWidget.currentItem().text(0)


    def NewLayer(self):
        txtName=self.Winnewlayer.lineEdit.text()
        txtType=self.Winnewlayer.comboBox.currentText()
        item=self.treeWidget.findItems('Layers',Qt.MatchStartsWith)[0]
        NewL=QTreeWidgetItem(item, [txtName])
        if txtType=='点':
            NewLchild=QTreeWidgetItem(NewL,[txtType])
            NewLchild.setIcon(0,QIcon('./UI/Point.png'))
            NewLchild.setFlags(NewLchild.flags() & ~Qt.ItemIsSelectable)
        elif txtType=='线':
            NewLchild=QTreeWidgetItem(NewL,[txtType])
            NewLchild.setIcon(0,QIcon('./UI/Line.png'))
            NewLchild.setFlags(NewLchild.flags() & ~Qt.ItemIsSelectable)
        elif txtType=='面':
            NewLchild=QTreeWidgetItem(NewL,[txtType])
            NewLchild.setIcon(0,QIcon('./UI/Polygon.png'))
            NewLchild.setFlags(NewLchild.flags() & ~Qt.ItemIsSelectable)
        self.treeWidget.expandAll()

        self.Winnewlayer.close()
    # endregion


# region 子窗体
class WinNewLayer(QWidget,Ui_Win_NewLayer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# endregion

# 作为主窗体运行
if __name__=='__main__':
    myapp=QApplication(sys.argv)

    # 启动界面设置
    cgitb.enable(format='text')

    myDlg=Main_exe()
    myDlg.show()
    sys.exit(myapp.exec_())


