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
#from Function.Op_DrawLabel import LabelMouseDoubleClick
import dbm_test
#endregion

# 主窗体操作
class Main_exe(QMainWindow,Ui_MainWindow):
    def __init__(self):
        # 创建窗体
        super(Main_exe,self).__init__()
        self.setupUi(self)
        

        # 属性
        self.EditStatus = False # 是否启用编辑
        self.LayerIndex = 1 # 每层的id
        self.mouseDrag = False # 标题栏拖动标识
        self.mouseLeftPress = False     # 鼠标左键是否处于按下状态
        self.mousePressLoc = QPoint()   # 鼠标按下时的位置（相对画布）
        self.mouseLastLoc = QPoint()    # 上一时刻鼠标的位置（用于处理鼠标移动事件）
        self.StyleOn = True    # 是否启用样式表
        self.IsAttr = False # 当前界面是否为属性窗体
        self.dbm = DBM()
        self.map = dbm_test.create_map(self.dbm)    # 当前地图
        # self.map = create_map()
        self.tool = MapTool.Null    # 当前使用的工具（鼠标状态）
        self.bufferRadius = 5       # 点选时缓冲区半径（像素）
        self.zoomRatio = 1.5        # 鼠标滚轮、放大缩小时的缩放比例
        self.StyleList = [0]*15           # 属性样式表
        self.CurEditLayer = None        #当前编辑的图层
        self.IsOperStacked = False      # 判断鼠标图标是否展开
        self.IsEditStacked = False  # 判断鼠标图标是否展开
        self.NeedSave = False      #是否需要保存
        self.IsChart = False         # 当前界面是否为表格窗体
        self.IsMap = False  # 当前界面是否为表格窗体
        self.EditNode = None      #当前移动节点

        # 初始化属性窗体
        initAttr(self)
        # 初始化表格窗体
        initChart(self)
        initWebmap(self)
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

    # 关闭窗体事件，DBM线程顺便关了
    def closeEvent(self, *args, **kwargs):
        super(Main_exe, self).closeEvent(*args, **kwargs)
        if self.dbm:
            self.dbm.closed = True

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
        self.tsButtonAttr.clicked.connect(self.bt_Attr_clicked)
        self.tsButtonImportshp.clicked.connect(self.bt_import_shp_clicked)
        self.tsButtonExportshp.clicked.connect(self.bt_export_shp_clicked)
        self.tsButtonNew.clicked.connect(self.bt_new_click)
        self.tsButtonSave.clicked.connect(self.bt_save_to_dbm)
        self.tsButtonOpen.clicked.connect(self.bt_open_from_dbm)
        self.tsButtonAddAttr.clicked.connect(self.bt_addattr_clicked)
        self.tsButtonDel.clicked.connect(self.bt_del_clicked)
        self.tsButtonSelectByAttr.clicked.connect(self.bt_selectbyattr_clicked)
        self.tsButtonChart.clicked.connect(self.bt_setchart_clicked)
        self.tsButtonAddFeature.clicked.connect(self.bt_addfeature_clicked)
        self.tsButtonEditFeature.clicked.connect(self.bt_editfeature_clicked)
        self.tsButtonMap.clicked.connect(self.bt_setmap_clicked)

    # 坐标转换，将事件E的坐标转换到画布坐标上
    def ConvertCor(self,e):
        point = e.globalPos()
        point = self.Drawlabel.mapFromGlobal(point)
        return point

    def mouseDoubleClickEvent(self, e):
        canvas_pos = self.ConvertCor(e)
        self.mouseDrag = False
        if self.EditStatus and self.tool == MapTool.AddGeometry and self.Drawlabel.rect().contains(canvas_pos):
            LabelMouseDoubleClick(self, e)

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
        def set_enable(status):
            '''设置一系列控件不可操作、恢复操作'''
            self.treeWidget.setEnabled(status)
            self.tsButtonNew.setEnabled(status)
            self.tsButtonOpen.setEnabled(status)
            self.tsButtonImportshp.setEnabled(status)
            self.tsButtonExportshp.setEnabled(status)
            self.tsButtonNewLayer.setEnabled(status)

        node=self.treeWidget.currentItem()
        if (not node) or not node.parent():
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u'提示')
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(u"\n请先选择要编辑的图层。\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
        else:
            if self.StyleOn:
                EditStack(self)
            self.EditStatus=not(self.EditStatus)
            if self.EditStatus:
                msgBox = QMessageBox()
                msgBox.setWindowTitle(u'提示')
                msgBox.setIcon(QMessageBox.Information)
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
                set_enable(False)
                map_ = self.map
                self.CurEditLayer = map_.layers[map_.selectedLayer]
                #map_.layers[map_.selectedLayer].selectedItems.clear()
                self.tableWidget.setEditTriggers(QAbstractItemView.SelectedClicked |
                                                 QAbstractItemView.DoubleClicked)
                TableUpdate(self)
                RefreshCanvas(self, use_base=True)

            else:
                # self.tsButtonEdit.setStyleSheet('border-image:url(UI/icon/edit.png)')
                if self.tool in (MapTool.AddGeometry, MapTool.EditGeometry):
                    self.tool = MapTool.Null
                self.CurEditLayer.edited_geometry.clear()
                self.CurEditLayer.selectedItems.clear()
                self.CurEditLayer = None
                set_enable(True)
                self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                RefreshCanvas(self, use_base=True)

    def bt_addfeature_clicked(self):
        if self.EditStatus:
            self.tool = MapTool.AddGeometry
            self.Drawlabel.setCursor(QCursor())
            self.NeedSave = False
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u'提示')
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(u"\n请先进入编辑状态。\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()

    def bt_editfeature_clicked(self):
        if self.EditStatus:
            self.tool = MapTool.EditGeometry
            self.Drawlabel.setCursor(QCursor())
            self.NeedSave = False
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n请先进入编辑状态。\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
    def bt_del_clicked(self):
        if not self.EditStatus:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n请先进入编辑状态。\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
        elif len(self.CurEditLayer.selectedItems) == 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n请先选择要删除的对象\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
        else:
            LabelDeleteItem(self)

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
        RefreshAttr(self)
        TreeViewUpdateList(self)
        TableUpdate(self)
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
        node = self.map.selectedLayer
        if node == -1:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n请先选择要保存的图层。\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
        else:
            self.dbm.add_layer_from_memory(self.map.layers[self.map.selectedLayer])
            self.map.layers[self.map.selectedLayer].saved_in_dbm=True
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
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
        self.Winnewlayer.comboBox.setItemIcon(3, QIcon('./UI/images/Line.png'))
        self.Winnewlayer.comboBox.setItemIcon(4, QIcon('./UI/images/Polygon.png'))
        self.Winnewlayer.show()
        self.Winnewlayer.bt_OK.clicked.connect(lambda:NewLayer(self))
        self.Winnewlayer.bt_Cancel.clicked.connect(self.Winnewlayer.close)
        # txt=self.treeWidget.currentItem().text(0)

    def bt_Attr_clicked(self):
        Switch(self, self.IsAttr, self.StyleOn)

    def bt_import_shp_clicked(self):
        ofd, filt = QFileDialog.getOpenFileName(self, '选择shapefile文件', './', 'Shapefile文件(*.shp);;ALL(*.*)')
        driver = ogr.GetDriverByName('ESRI Shapefile')
        data_source = driver.Open(ofd, 0)
        if data_source is None:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("未找到符合要求的shp文件")
            msgBox.addButton(QMessageBox.Ok)
            msgBox.exec_()
            return
        ori_layer = data_source.GetLayer(0)
        type_dict = {ogr.wkbPoint: PointD, ogr.wkbLineString: Polyline, ogr.wkbPolygon: Polygon, ogr.wkbMultiPolygon : MultiPolygon,
                     ogr.wkbMultiLineString : MultiPolyline}
        layer_name = ofd.split('/')[-1].split('.')[0]
        geo_type = ori_layer.GetGeomType()
        # 这里要遍历每个几何体的原因是：虽然图层中描述为“Poly~”，但其实有Multi~，需确定是否为Multi
        feat = ori_layer.GetNextFeature()
        while feat:
            geom = feat.GetGeometryRef()
            test_type = geom.GetGeometryType()
            if test_type > geo_type:
                geo_type = test_type
                break
            feat = ori_layer.GetNextFeature()
        ori_layer.ResetReading()
        # spatial_ref = ori_layer.GetSpatialRef()
        new_layer = Layer(type_dict[geo_type], layer_name)
        new_layer.import_from_shplayer(ori_layer)
        data_source.Release()
        self.map.AddLayer(new_layer, self.map.selectedLayer if self.map.selectedLayer != -1 else 0)
        if len(self.map.layers) == 1:
            self.map.FullScreen(self.Drawlabel.width(), self.Drawlabel.height())
        TreeViewUpdateList(self)
        TableUpdate(self)
        RefreshCanvas(self)

    def bt_export_shp_clicked(self):
        node = self.map.selectedLayer
        if node == -1:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle(u'提示')
            msgBox.setText(u"\n请先选择要保存的图层。\n")
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            # 隐藏ok按钮
            msgBox.addButton(QMessageBox.Ok)
            # 模态对话框
            msgBox.exec_()
        else:
            sfd = QFileDialog.getSaveFileName(self, "导出shapefile文件", './', 'Shapefile文件(*.shp)')[0]
            self.map.layers[node].export_to_shplayer(sfd)
    # def labelResizeEvent(self, a0: QtGui.QResizeEvent):
        '''画布大小改变'''
        # super(QLabel, self.Drawlabel).resizeEvent(a0)
        # canvas = QtGui.QPixmap(a0.size())
        # canvas.fill(QColor('white'))
        # self.Drawlabel.setPixmap(canvas)
        # Refresh(self, QCursor.pos())

    def bt_new_click(self):
        '''这个按钮指的是放弃原来的地图，新建地图'''
        def ok_click():
            self.map = Map()
            TreeViewUpdateList(self)
            TableUpdate(self)
            RefreshCanvas(self)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setWindowTitle('创建新地图')
        msgBox.setText('\n确定放弃目前的地图和所有图层、创建新地图吗？\n未保存的信息将会丢失。\n')
        msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
        ok = msgBox.addButton(QMessageBox.Ok)
        ok.clicked.connect(ok_click)
        msgBox.addButton(QMessageBox.Cancel)
        msgBox.exec_()

    def bt_addattr_clicked(self):
        self.WinNewAttr = WinNewAttr()
        self.WinNewAttr.show()
        # 设置OK键函数
        self.WinNewAttr.pushButto_OK.clicked.connect(lambda: addAttr(self))
        self.WinNewAttr.pushButto_Cancel.clicked.connect(self.WinNewAttr.close)

    def bt_selectbyattr_clicked(self):
        # 地图中没有图层，需要报信息
        if len(self.map.layers) == 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowTitle('图层错误')
            msgBox.setText('\n该地图项目中没有图层。\n')
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            msgBox.addButton(QMessageBox.Ok)
            msgBox.exec_()
            return
        self.WinSelect=WinSelectByAttr()
        # 添加图层到图层选择列表中
        combo_layer = self.WinSelect.combo_layer
        combo_layer.addItems([layer.name for layer in self.map.layers])
        if self.map.selectedLayer != -1:
            combo_layer.setCurrentIndex(self.map.selectedLayer)
        self.WinSelect.show()
        # 设置OK键函数
        self.WinSelect.bt_OK.clicked.connect(lambda: selectGeoByStr(self))
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
    def bt_setchart_clicked(self):
        if not self.IsChart:
            self.WinChart = WinChartSet()

            # 初始化combobox
            ind = self.map.selectedLayer
            combo=self.WinChart.comboBox
            combo1=self.WinChart.comboBox_2
            if ind == -1:
                combo.addItems([''])
                combo1.addItems([''])
            else:
                combo.addItems(self.map.layers[ind].table.columns)
                combo1.addItems(self.map.layers[ind].table.columns)

            self.WinChart.show()
            # 设置OK键函数
            self.WinChart.bt_OK.clicked.connect(lambda:SwitchChart(self))
            self.WinChart.bt_Cancel.clicked.connect(self.WinChart.close)
        else:
            SwitchChart(self)

    def bt_setmap_clicked(self):
        if not self.IsMap:
            msgBox = QMessageBox()
            msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
            msgBox.addButton(QMessageBox.Ok)
            index=self.map.selectedLayer
            if index==-1:
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setWindowTitle('未选中图层')
                msgBox.setText('选择图层为空！')
                msgBox.exec_()
            else:
                layer=self.map.layers[index]
                if layer.type==Polygon or layer.type==MultiPolygon:
                    SwitchMap(self)
                else:
                    msgBox.setIcon(QMessageBox.Critical)
                    msgBox.setWindowTitle('非面状图层')
                    msgBox.setText('暂未处理面状图层外的图层类型。')
                    msgBox.exec_()
        else:
            SwitchMap(self)

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

class WinChartSet(QWidget, Ui_Win_Chart):
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


