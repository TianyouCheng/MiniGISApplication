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
        self.EditStatus=False

        # 绑定信号与槽函数
        self.slot_connect()

        # 创建画布
        # canvas.size()这个取出来的size不对，是（100，500）,实际是（879，500）
        canvas=QtGui.QPixmap(QtCore.QSize(879, 500))
        canvas.fill(QColor('white'))
        self.label.setPixmap(canvas)

        # 绘图函数
        self.draw_something()


# region TabelView控件  需要整理
        #https://zhuanlan.zhihu.com/p/34532247
        #https://github.com/PyQt5/PyQt/tree/master/QTreeWidget
        # 目前实现了删除单行，看需不需要删除多行。
        self.id=1
        font = QFont('微软雅黑', 20)
        font.setBold(True)  # 设置字体加粗
        # self.tableWidget.horizontalHeader().setFont(font)  # 设置表头字体

        # self.tableWidget.setFrameShape(QFrame.NoFrame)  ##设置无表格的外框
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只可以单选，可以使用ExtendedSelection进行多选
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置 不可选择单个单元格，只可选择一行。
        self.tableWidget.setColumnCount(5)  ##设置表格一共有五列
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置第五列宽度自动调整，充满屏幕
        # 设置表头
        self.tableWidget.setHorizontalHeaderLabels(
            ['序号', '姓名', '年龄', '地址','成绩'])
        self.lines=[]

        # TREEVIEW
        pitem1=QTreeWidgetItem(self.treeWidget,['Layers'])
        citem1=QTreeWidgetItem(pitem1,['Mountain'])
        citem11 = QTreeWidgetItem(citem1, ['Mountain Symbol'])
        citem11.setIcon(0,QIcon('./UI/icon1.png'))
        citem2 = QTreeWidgetItem(pitem1, ['Street'])
        citem22 = QTreeWidgetItem(citem2, ['Street Symbol'])
        citem22.setIcon(0, QIcon('./UI/icon1.png'))
        citem3 = QTreeWidgetItem(pitem1, ['Water'])
        citem33 = QTreeWidgetItem(citem3, ['Water Symbol'])
        citem33.setIcon(0, QIcon('./UI/icon1.png'))
        citem4 = QTreeWidgetItem(pitem1, ['City'])
        citem44 = QTreeWidgetItem(citem4, ['City Symbol'])
        citem44.setIcon(0, QIcon('./UI/icon1.png'))
        citem1.setCheckState(0, Qt.Checked)
        citem2.setCheckState(0, Qt.Checked)
        citem3.setCheckState(0, Qt.Checked)
        citem4.setCheckState(0, Qt.Checked)
        self.treeWidget.header().setVisible(False)
        self.treeWidget.expandAll()


    def TabelViewAdd(self):
        # Todo 优化2 添加数据
        row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row + 1)
        id = str(self.id)
        name = 'Ana'
        score = str(random.randint(50, 99))
        age=str(random.randint(18, 30))
        add = 'America'
        self.tableWidget.setItem(row, 0, QTableWidgetItem(id))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(name))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(age))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(add))
        self.tableWidget.setItem(row, 4, QTableWidgetItem(score))
        self.id += 1
        self.lines.append([id, name, age, add, score])

    def TabelViewDel(self):
        # TODO 优化3 删除当前选中的数据
        selected_items=self.tableWidget.selectedItems()
        if len(selected_items)==0:
            return
        self.tableWidget.removeRow(self.tableWidget.indexFromItem(selected_items[0]).row())
# endregion

# region TreeView控件  需要整理




    # region 功能函数
    # 绑定信号与槽函数
    def slot_connect(self):
        self.tsButtonEdit.clicked.connect(self.bt_edit_clicked)
        # TabelView相关
        self.pushButtonAdd.clicked.connect(self.TabelViewAdd)
        self.pushButtonDel.clicked.connect(self.TabelViewDel)

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
        self.EditStatus=not(self.EditStatus)
        if self.EditStatus:self.tsButtonEdit.setText("正在编辑")
        elif not self.EditStatus:self.tsButtonEdit.setText("编辑模式")
    # endregion




class GifSplashScreen(QSplashScreen):


    def __init__(self, *args, **kwargs):
        super(GifSplashScreen, self).__init__(*args, **kwargs)
        self.movie = QMovie('./UI/img.jpg')
        self.movie.frameChanged.connect(self.onFrameChanged)
        self.movie.start()


    def onFrameChanged(self, _):
        self.setPixmap(self.movie.currentPixmap())


    def finish(self, widget):
        self.movie.stop()
        super(GifSplashScreen, self).finish(widget)




class BusyWindow(QWidget):


    def __init__(self, *args, **kwargs):
        super(BusyWindow, self).__init__(*args, **kwargs)
        # 模拟耗时操作，一般来说耗时的加载数据应该放到线程
        for i in range(2):
            sleep(1)
            splash.showMessage('加载进度: 100%', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
            QApplication.instance().processEvents()


        splash.showMessage('初始化完成', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
        splash.finish(self)
# 作为主窗体运行
if __name__=='__main__':
    myapp=QApplication(sys.argv)

    # 启动界面设置
    cgitb.enable(format='text')

    global splash
    splash=GifSplashScreen()
    splash.show()
    w = BusyWindow()
    # w.show()

    splash.showMessage('等待创建界面', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)

    myDlg=Main_exe()
    myDlg.show()
    sys.exit(myapp.exec_())


