import os,sys,random,cgitb
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from osgeo import gdal
from osgeo import ogr

#region 引入窗体及函数
from UI import *
from Function import *
from unit_test import create_map
import dbm_test
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
        self.mouseDrag = False # 标题栏拖动标识
        self.mouseLeftPress = False     # 鼠标左键是否处于按下状态
        self.mousePressLoc = QPoint()   # 鼠标按下时的位置（相对画布）
        self.mouseLastLoc = QPoint()    # 上一时刻鼠标的位置（用于处理鼠标移动事件）
        self.StyleOn=False    # 是否启用样式表
        self.IsAttr=False # 当前界面是否为属性窗体
        self.dbm = DBM()
        self.map = dbm_test.create_map(self.dbm)    # 当前地图
        # self.map = create_map()
        self.tool = MapTool.Null    # 当前使用的工具（鼠标状态）
        self.bufferRadius = 5       # 点选时缓冲区半径（像素）
        self.zoomRatio = 1.5        # 鼠标滚轮、放大缩小时的缩放比例
        self.StyleList=[0]*15           # 属性样式表
        self.CurEditLayer = None        #当前编辑的图层
        self.IsOperStacked=False      # 判断鼠标图标是否展开
        self.IsEditStacked = False  # 判断鼠标图标是否展开

        # 初始化属性窗体
        initAttr(self)
        # 设置属性窗体
        setAttr(self)
        # 叠起控件
        if self.StyleOn:
            EditStack(self)
            OperateStack(self)


        # 自定义标题栏设置
        self.bt_min.clicked.connect(lambda: self.setWindowState(Qt.WindowMinimized))
        # TODO: 最大化disabled
        self.bt_close.clicked.connect(self.close)

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
            initHover(self)
            # self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section{background-color:rgb(255,255,255,0.3);font:10pt '宋体';color: white;}")

            self.tableWidget.verticalHeader().setVisible(False)
            with open('./UI/Scrollbar.qss') as f2:
                qss=f2.read()
            self.tableWidget.verticalScrollBar().setStyleSheet(qss)
        else:
            defaultUI(self)

        RefreshCanvas(self)
        # 设置TabelView,必须设置有几列
        TableView_Init(self,5)
        TableUpdate(self)

        # 设置TreeView
        TreeView_Init(self)
        TreeViewUpdateList(self)

    # region 功能函数
    # 重写鼠标点击事件
    def mousePressEvent(self, event):
        # 在自定义样式中设置移动窗体
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
        # self.Drawlabel.resizeEvent = self.labelResizeEvent
        self.tsButtonAttr.clicked.connect(lambda:Switch(self,self.IsAttr,self.StyleOn))
        self.tsButtonImportshp.clicked.connect(self.bt_import_shp_clicked)
        self.tsButtonExportshp.clicked.connect(self.bt_export_shp_clicked)
        self.tsButtonSave.clicked.connect(self.bt_save_to_dbm)
        self.tsButtonOpen.clicked.connect(self.bt_open_from_dbm)
        self.tsButtonAddAttr.clicked.connect(self.bt_addattr_clicked)
        self.tsButtonDel.clicked.connect(self.bt_del_clicked)
        self.tsButtonSelectByAttr.clicked.connect(self.bt_selectbyattr_clicked)

    # 坐标转换，将事件E的坐标转换到画布坐标上
    def ConvertCor(self,e):
        point = e.globalPos()
        point = self.Drawlabel.mapFromGlobal(point)
        return point

    # 重写鼠标移动事件
    def mouseMoveEvent(self, e):
        canvas_pos = self.ConvertCor(e)
        # 移动标题栏操作
        if self.mouseDrag:
            self.move(e.globalPos()-self.move_DragPosition)
            e.accept()
        # 处理在画布移动时发生的事件

        if self.Drawlabel.rect().contains(canvas_pos):
            LabelMouseMove(self, e)
        '''
        painter = QtGui.QPainter(self.Drawlabel.pixmap())
        
        # painter.setPen(QtGui.QColor('white'))
        
        if self.EditStatus:
            if self.tool == MapTool.AddGeometry:
                if self.type == PointD:
                    painter.drawArc(QRect(canvas_pos.x() - 1, canvas_pos.y() - 1, 2, 2), 0, 360 * 16)
                    painter.end()
                elif self.type == Polyline:
                    painter.
            elif self.tool == MapTool.EditGeometry:
                pass
            self.update()
        '''
        self.mouseLastLoc.setX(canvas_pos.x())
        self.mouseLastLoc.setY(canvas_pos.y())

        # 状态栏显示信息。事件驱动问题已解决，可以在鼠标移动时接收事件
        # TODO: 考虑删除状态栏用label代替，HJJ建议显示地理坐标
        geo_p = self.map.ScreenToGeo(PointD(canvas_pos.x(),canvas_pos.y()),
                                     (self.Drawlabel.width(), self.Drawlabel.height()))
        self.statusBar.showMessage('x: {:.6g},  y: {:.6g}'.format(geo_p.X, geo_p.Y))

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
        cursor = QCursor()
        self.Drawlabel.setCursor(cursor)
        if self.StyleOn:
            OperateStack(self)

    def bt_pan_clicked(self):
        '''按下“漫游”按钮'''
        self.tool = MapTool.Pan
        pixmap=QPixmap(r'./UI/icon/cursor_pan.png').scaled(30,30)
        cursor=QCursor(pixmap)
        self.Drawlabel.setCursor(cursor)

    def bt_zoomIn_clicked(self):
        '''按下“放大”按钮'''
        self.tool = MapTool.ZoomIn
        pixmap = QPixmap(r'./UI/icon/cursor_zomout.png').scaled(30, 30)
        cursor = QCursor(pixmap)
        self.Drawlabel.setCursor(cursor)

    def bt_zoomOut_clicked(self):
        '''按下“缩小”按钮'''
        self.tool = MapTool.ZoomOut
        pixmap = QPixmap(r'./UI/icon/cursor_zomin.png').scaled(30, 30)
        cursor = QCursor(pixmap)
        self.Drawlabel.setCursor(cursor)

    def bt_zoomScale_clicked(self):
        '''按下“全屏显示”按钮'''
        self.map.FullScreen(self.Drawlabel.width(), self.Drawlabel.height())
        RefreshCanvas(self)

    def bt_select_clicked(self):
        '''按下“选择要素”按钮'''
        self.tool = MapTool.Select
        self.Drawlabel.setCursor(QCursor())

    def bt_edit_clicked(self):
        if self.StyleOn:
            EditStack(self)
        node=self.treeWidget.currentItem()
        if not node:
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
                # self.tsButtonEdit.setStyleSheet('border-image:url(UI/icon/edit_p.png)')
                self.treeWidget.setEnabled(False)
                map_ = self.map
                map_.layers[map_.selectedLayer].selectedItems.clear()
                RefreshCanvas(self, use_base=True)

            else:
                # self.tsButtonEdit.setStyleSheet('border-image:url(UI/icon/edit.png)')
                self.treeWidget.setEnabled(True)
    def bt_del_clicked(self):
        if not self.EditStatus:
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n请先进入编辑状态。\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
        elif self.MapTool != MapTool.ditGeometry:
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n目前为创建要素状态，请先切换到编辑要素状态\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
        elif len(self.CurEditLayer.selectedItems) == 0:
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n请先选择要删除的对象\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
        else:
            pass
    def bt_open_from_dbm(self):
        self.WinDBLoad = WinDBLoad()
        # 设置Table
        self.WinDBLoad.DBL_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.WinDBLoad.show()
        # 设置OK键函数
        self.WinDBLoad.DBLoad_OK.clicked.connect(self.bt_open_from_dbm_ok)
        self.WinDBLoad.DBLoad_Cancel.clicked.connect(self.WinDBLoad.close)


        layer_info_from_dbm=self.dbm.get_layers_info()
        layer_count=len(layer_info_from_dbm)
        layer_tablewidget=self.WinDBLoad.DBL_tableWidget
        layer_tablewidget.setRowCount(layer_count)
        layer_tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        for row in range(layer_count):
            layer_name=layer_info_from_dbm[row][0]
            layer_type=layer_info_from_dbm[row][2]
            layer_tablewidget.setItem(row,0,QTableWidgetItem(layer_name))
            layer_tablewidget.setItem(row,1,QTableWidgetItem(layer_type))

    def bt_open_from_dbm_ok(self):
        cur_row=self.WinDBLoad.DBL_tableWidget.currentRow()
        cur_item=self.WinDBLoad.DBL_tableWidget.item(cur_row,0)
        layer_name=cur_item.text()
        new_layer=self.dbm.load_layer(layer_name)
        self.map.AddLayer(new_layer)
        # 刷新树视图和刷新画布
        TreeViewUpdateList(self)
        RefreshCanvas(self)
        
        self.WinDBLoad.close()

    def bt_open_from_dbm_delete(self):
        cur_row=self.WinDBLoad.DBL_tableWidget.currentRow()
        cur_item=self.WinDBLoad.DBL_tableWidget.item(cur_row,0)
        layer_name=cur_item.text()
        self.dbm.delete_layer(layer_name)
        for layer in self.map.layers:
            if layer.name == layer_name:
                layer.saved_in_dbm=False
        self.WinDBLoad.DBL_tableWidget.removeRow(cur_row)
        

    def bt_save_to_dbm(self):
        node=self.treeWidget.currentItem()
        if not node:
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n请先选择要编辑的图层。\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
        else:
            self.dbm.add_layer_from_memory(self.map.layers[self.map.selectedLayer])
            self.map.layers[self.map.selectedLayer].saved_in_dbm=True
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n保存成功\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()

    def bt_newlayer_clicked(self):
        self.Winnewlayer=WinNewLayer()
        # 设置Combox
        self.Winnewlayer.comboBox.setItemIcon(0, QIcon('./UI/images/Point.png'))
        self.Winnewlayer.comboBox.setItemIcon(1, QIcon('./UI/images/Line.png'))
        self.Winnewlayer.comboBox.setItemIcon(2, QIcon('./UI/images/Polygon.png'))
        self.Winnewlayer.show()
        self.Winnewlayer.bt_OK.clicked.connect(lambda:NewLayer(self))
        self.Winnewlayer.bt_Cancel.clicked.connect(self.Winnewlayer.close)
        # txt=self.treeWidget.currentItem().text(0)

    def bt_import_shp_clicked(self):
        ofd = QFileDialog.getOpenFileName(self, '选择shapefile文件', './', 'ALL(*.*);;Shapefile文件(*.shp)')
        driver = ogr.GetDriverByName('ESRI Shapefile')
        data_source = driver.Open(ofd, 0)
        if data_source is None:
            msgBox = QMessageBox()
            msgBox.setText("未找到符合要求的shp文件")
            msgBox.addButton(QMessageBox.Ok)
            msgBox.exec_()
            return
        ori_layer = data_source.GetLayer(0)
        type_dict = {ogr.wkbPoint: PointD, ogr.wkbLineString: Polyline, ogr.wkbPolygon: Polygon, ogr.wkbMultiPolygon : MultiPolygon,
                     ogr.wkbMultiLineString : MultiPolyline}
        layer_name = ofd.split('/')[-1].split('.')[0]
        geo_type = type_dict[ori_layer.GetGeomType()]
        # spatial_ref = ori_layer.GetSpatialRef()
        new_layer = Layer(geo_type, layer_name)
        new_layer.import_from_shplayer(ori_layer)

    def bt_export_shp_clicked(self):
        sfd = QFileDialog.getSaveFileName(self, "导出shapefile文件", './', 'Shapefile文件(*.shp)')
        self.map_.layers[self.map_.selectedLayer].export_to_shplayer(sfd)
    # def labelResizeEvent(self, a0: QtGui.QResizeEvent):
        '''画布大小改变'''
        # super(QLabel, self.Drawlabel).resizeEvent(a0)
        # canvas = QtGui.QPixmap(a0.size())
        # canvas.fill(QColor('white'))
        # self.Drawlabel.setPixmap(canvas)
        # Refresh(self, QCursor.pos())

    def bt_addattr_clicked(self):
        self.WinNewAttr = WinNewAttr()
        self.WinNewAttr.show()
        # 设置OK键函数
        self.WinNewAttr.pushButto_OK.clicked.connect(lambda: addAttr(self))
        self.WinNewAttr.pushButto_Cancel.clicked.connect(self.WinNewAttr.close)

    def bt_selectbyattr_clicked(self):
        self.WinSelect=WinSelectByAttr()
        self.WinSelect.show()
        # 设置OK键函数
        self.WinSelect.bt_OK.clicked.connect(self.WinSelect.close)
        self.WinSelect.bt_Cancel.clicked.connect(self.WinSelect.close)

    def treeViewItemChanged(self, item, column):
        '''图层的可见性改变'''
        treeCheckedChange(item, column, self)

    def treeViewCurrentItemChanged(self, current, previous):
        '''改变选择图层'''
        treeCurrentItemChanged(current, self)

    def tableSelectionChanged(self):
        '''属性表中选择几何体变化'''
        TableSelectionChanged(self)

    def tableItemChanged(self,item):
        TableItemChanged(self,item)

    # endregion


# region 子窗体
class WinNewLayer(QWidget,Ui_Win_NewLayer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class WinDBLoad(QWidget,Ui_Win_DBLoad):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class WinNewAttr(QWidget, Ui_Win_NewAttr):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class WinSelectByAttr(QWidget, Ui_Win_SelectByAttr):
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


