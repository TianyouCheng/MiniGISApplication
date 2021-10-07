import os,sys,random,cgitb
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#region 引入窗体及函数
from UI import *
from Function import *
from unit_test import create_map
#endregion

# 主窗体操作
class Main_exe(QMainWindow,Ui_MainWindow):
    def __init__(self):
        # 创建窗体
        super(Main_exe,self).__init__()
        self.setupUi(self)
        # 初始化属性窗体
        initAttr(self)

        # 属性
        self.EditStatus=False # 是否启用编辑
        self.LayerIndex = 1 # 每层的id
        self.mouseDrag = False # 标题栏拖动标识
        self.mouseLeftPress = False     # 鼠标左键是否处于按下状态
        self.mousePressLoc = QPoint()   # 鼠标按下时的位置（相对画布）
        self.mouseLastLoc = QPoint()    # 上一时刻鼠标的位置（用于处理鼠标移动事件）
        self.StyleOn=False # 是否启用样式表
        self.IsAttr=False # 当前界面是否为属性窗体
        self.map = create_map()    # 当前地图
        self.tool = MapTool.Null    # 当前使用的工具（鼠标状态）
        self.bufferRadius = 5       # 点选时缓冲区半径（像素）
        self.zoomRatio = 1.5        # 鼠标滚轮、放大缩小时的缩放比例

        # 自定义标题栏设置
        self.bt_min.clicked.connect(lambda: self.setWindowState(Qt.WindowMinimized))
        # TODO: 最大化disabled
        self.bt_close.clicked.connect(self.close)


        # 鼠标悬停在按钮上显示信息
        self.tsButtonNew.setToolTip('新建')
        self.tsButtonOpen.setToolTip('打开')
        self.tsButtonSave.setToolTip('保存')
        self.tsButtonOperateNone.setToolTip('鼠标指针')
        self.tsButtonPan.setToolTip('漫游')
        self.tsButtonZoomIn.setToolTip('放大')
        self.tsButtonZoomOut.setToolTip('缩小')
        self.tsButtonZoomScale.setToolTip('全屏显示')
        self.tsButtonNewLayer.setToolTip('创建新图层')
        self.tsButtonSelect.setToolTip('选择要素')
        self.tsButtonEdit.setToolTip('编辑模式')


        # 绑定信号与槽函数
        self.slot_connect()

        # 创建画布
        # canvas.size()这个取出来的size不对，是（100，500）,实际是（879，500）
        # 实验后，发现好多控件的.size方法，取出来的都不对。原因可能是在这个初始化函数里，控件还没完成初始化
        canvas = QtGui.QPixmap(QtCore.QSize(1000, self.Drawlabel.size().height()))
        canvas.fill(QColor('white'))
        self.Drawlabel.setPixmap(canvas)
        # 已经渲染好的地理底图（若在编辑、选择几何体模式可直接在底图上覆盖绘制）
        self.basePixmap = QPixmap(canvas)
        # 固定窗口大小
        self.setFixedSize(self.width(), self.height())

        # 设置qss样式
        if self.StyleOn:
            self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口无边框
            with open('./UI/style.qss') as f1:
                qss=f1.read()
            self.setStyleSheet(qss)
            # self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section{background-color:rgb(255,255,255,0.3);font:10pt '宋体';color: white;}")
            self.tableWidget.horizontalHeader().setVisible(False)
            self.tableWidget.verticalHeader().setVisible(False)
            with open('./UI/Scrollbar.qss') as f2:
                qss=f2.read()
            self.tableWidget.verticalScrollBar().setStyleSheet(qss)
        else:
            defaultUI(self)

        # 设置TabelView,必须设置有几列
        TableView_Init(self,5)

        # 设置TreeView
        TreeView_Init(self)
        TreeViewUpdateList(self.treeWidget, self.map, self.StyleOn)

    # region 功能函数
    # 重写鼠标点击事件
    def mousePressEvent(self, event):
        Titlerect = self.widget.rect()
        if event.pos() in Titlerect:
            self.mouseDrag=True
        self.move_DragPosition=event.globalPos()-self.pos()

        # 处理点击画布时发生的事件
        canvas_pos = self.ConvertCor(event)
        if self.Drawlabel.rect().contains(canvas_pos):
            if event.button() == Qt.MouseButton.LeftButton:
                self.mouseLeftPress = True
                self.mousePressLoc.setX(canvas_pos.x())
                self.mousePressLoc.setY(canvas_pos.y())
                self.mouseLastLoc.setX(canvas_pos.x())
                self.mouseLastLoc.setY(canvas_pos.y())
            LabelMousePress(self, event)

        event.accept()

    # 重写鼠标松开事件
    def mouseReleaseEvent(self, event):
        self.mouseDrag = False
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouseLeftPress = False

        # 处理鼠标在画布时发生的事件
        LabelMouseRelease(self, event)

    # 绑定信号与槽函数
    def slot_connect(self):
        self.tsButtonOperateNone.clicked.connect(self.bt_operateNone_clicked)
        self.tsButtonPan.clicked.connect(self.bt_pan_clicked)
        self.tsButtonZoomIn.clicked.connect(self.bt_zoomIn_clicked)
        self.tsButtonZoomOut.clicked.connect(self.bt_zoomOut_clicked)
        self.tsButtonZoomScale.clicked.connect(self.bt_zoomScale_clicked)
        self.tsButtonSelect.clicked.connect(self.bt_select_clicked)
        self.tsButtonEdit.clicked.connect(self.bt_edit_clicked)
        self.tsButtonNewLayer.clicked.connect(self.bt_newlayer_clicked)
        self.Drawlabel.resizeEvent = self.labelResizeEvent
        self.tsButtonAttr.clicked.connect(lambda:Switch(self,self.IsAttr,self.StyleOn))

    # 坐标转换，将事件E的坐标转换到画布坐标上
    def ConvertCor(self,e):
        point = e.globalPos()
        point = self.Drawlabel.mapFromGlobal(point)
        return point

    # 重写鼠标移动事件
    def mouseMoveEvent(self, e):
        # 移动标题栏操作
        if self.mouseDrag:
            self.move(e.globalPos()-self.move_DragPosition)
            e.accept()
        # 处理在画布移动时发生的事件
        canvas_pos = self.ConvertCor(e)
        if self.Drawlabel.rect().contains(canvas_pos):
            LabelMouseMove(self, e)

        painter = QtGui.QPainter(self.Drawlabel.pixmap())
        # painter.setPen(QtGui.QColor('white'))
        if self.EditStatus:
            painter.drawPoint(canvas_pos.x(), canvas_pos.y())
            painter.end()
            self.update()

        self.mouseLastLoc.setX(canvas_pos.x())
        self.mouseLastLoc.setY(canvas_pos.y())

    # 鼠标滚轮事件
    def wheelEvent(self, e):
        canvas_pos = self.ConvertCor(e)
        if self.Drawlabel.rect().contains(canvas_pos):
            LabelMouseWheel(self, e)

    # endregion

    # region 信号与槽函数
    def bt_operateNone_clicked(self):
        '''按下“鼠标指针”按钮'''
        self.tool = MapTool.Null

    def bt_pan_clicked(self):
        '''按下“漫游”按钮'''
        self.tool = MapTool.Pan

    def bt_zoomIn_clicked(self):
        '''按下“放大”按钮'''
        self.tool = MapTool.ZoomIn

    def bt_zoomOut_clicked(self):
        '''按下“缩小”按钮'''
        self.tool = MapTool.ZoomOut

    def bt_zoomScale_clicked(self):
        '''按下“全屏显示”按钮'''
        self.map.FullScreen(self.Drawlabel.width(), self.Drawlabel.height())
        Refresh(self, QCursor.pos())

    def bt_select_clicked(self):
        '''按下“选择要素”按钮'''
        self.tool = MapTool.Select

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
                # txttype = self.treeWidget.currentItem().child(0).text(0)
                # msgBox.setText(u"\n您现在编辑的是：\n" + txtname + txttype + "对象图层。\n")
                msgBox.setText(u"\n您现在编辑的是：\n" + txtname + "图层。\n")
                msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
                # 隐藏ok按钮
                msgBox.addButton(QMessageBox.Ok)
                # 模态对话框
                msgBox.exec_()
                self.tsButtonEdit.setStyleSheet('border-image:url(UI/icon/edit_p.png)')
                self.treeWidget.setEnabled(False)
                map_ = self.map
                map_.layers[map_.selectedLayer].selectedItems.clear()
                Refresh(self, QCursor.pos(), use_base=True)

            elif not self.EditStatus:
                self.tsButtonEdit.setStyleSheet('border-image:url(UI/icon/edit.png)')
                self.treeWidget.setEnabled(True)

    def bt_newlayer_clicked(self):
        self.Winnewlayer=WinNewLayer()
        # 设置Combox
        self.Winnewlayer.comboBox.setItemIcon(0,QIcon('./UI/images/Point.png'))
        self.Winnewlayer.comboBox.setItemIcon(1, QIcon('./UI/images/Line.png'))
        self.Winnewlayer.comboBox.setItemIcon(2, QIcon('./UI/images/Polygon.png'))
        self.Winnewlayer.show()
        self.Winnewlayer.bt_OK.clicked.connect(lambda:NewLayer(self))
        self.Winnewlayer.bt_Cancel.clicked.connect(self.Winnewlayer.close)
        # txt=self.treeWidget.currentItem().text(0)

    def labelResizeEvent(self, a0: QtGui.QResizeEvent):
        '''画布大小改变'''
        super(QLabel, self.Drawlabel).resizeEvent(a0)
        canvas = QtGui.QPixmap(a0.size())
        canvas.fill(QColor('white'))
        self.Drawlabel.setPixmap(canvas)
        Refresh(self, QCursor.pos())

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


