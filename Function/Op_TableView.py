'''
表格控件的相关操作函数
'''
import PyQt5
from PyQt5.QtWidgets import QTableWidgetItem,QAbstractItemView,QHeaderView, QTableWidget, QMessageBox,QMenu
from PyQt5.QtWidgets import QTableWidgetSelectionRange as TabRange
from PyQt5.QtGui import QFont,QColor,QBrush, QIcon,QCursor
from PyQt5.Qt import Qt
from PyQt5.QtCore import Qt as qcq
import random
from .MapTool import MapTool
from .Op_DrawLabel import RefreshCanvas

def TableView_Init(self,nColumn):
    '''
    TableView控件的初始化
    目前实现了删除单行，看需不需要删除多行。
    :param self: 主窗体类
    :param nColumn: 表格的列数
    :return: None
    '''
    font = QFont('微软雅黑', 8)
    font.setBold(True)  # 设置字体加粗
    self.tableWidget.horizontalHeader().setFont(font)  # 设置表头字体

    # self.tableWidget.setFrameShape(QFrame.NoFrame)  ##设置无表格的外框
    self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)  # 设置只可以单选，可以使用ExtendedSelection进行多选
    self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置不可选择单个单元格，只可选择一行。
    self.tableWidget.setColumnCount(nColumn)  ##设置表格一共有五列
    # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
    self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置第五列宽度自动调整，充满屏幕
    # 设置表头
    self.tableWidget.setHorizontalHeaderLabels(['序号', '姓名', '年龄', '地址', '成绩'])
    self.lines = []
    self.id = 1

    # 信号与槽函数
    self.tableWidget.itemSelectionChanged.connect(self.tableSelectionChanged)
    self.tableWidget.itemChanged.connect(self.tableItemChanged)

    # 右键菜单
    self.tableWidget.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
    self.tableWidget.horizontalHeader().customContextMenuRequested.connect(lambda:TableContextMenu(self))

def TableContextMenu(self):
    self.contextMenu=QMenu()
    self.actionA = self.contextMenu.addAction(u'动作a')
    self.contextMenu.popup(QCursor.pos())
    self.actionA.triggered.connect(lambda:actionHandler())
    self.contextMenu.show()

def actionHandler():
    print(222)

def TableUpdate(main_exe):
    '''更新属性数据的表格内容'''
    tabWid = main_exe.tableWidget
    tabWid.itemSelectionChanged.disconnect(main_exe.tableSelectionChanged)
    tabWid.itemChanged.disconnect(main_exe.tableItemChanged)
    tabWid.clearContents()
    index = main_exe.map.selectedLayer
    if index == -1:
        tabWid.setColumnCount(0)
        tabWid.setRowCount(0)
    else:
        layer = main_exe.map.layers[main_exe.map.selectedLayer]
        table = layer.table
        tabWid.setColumnCount(table.shape[1])
        tabWid.setRowCount(table.shape[0])
        tabWid.setHorizontalHeaderLabels(table.columns)
        selectedItems = set(layer.selectedItems)
        selected_rows = []
        for row in range(table.shape[0]):
            for col in range(table.shape[1]):
                item = QTableWidgetItem(str(table.iloc[row, col]))
                if main_exe.StyleOn:
                    item.setForeground(QColor(255, 255, 255))
                tabWid.setItem(row, col, item)
            tabWid.item(row,0).setFlags(qcq.ItemIsSelectable|qcq.ItemIsEnabled)
            if table.loc[row, 'ID'] in selectedItems:
                selected_rows.append(row)
        # 在表格中选择要素
        for row in selected_rows:
            tabWid.setRangeSelected(TabRange(row, 0, row, tabWid.columnCount() - 1), True)
    tabWid.itemSelectionChanged.connect(main_exe.tableSelectionChanged)
    tabWid.itemChanged.connect(main_exe.tableItemChanged)


def TableSelectionChanged(main_exe):
    '''在属性表的选择内容改变，联动到地图上'''
    tabWid = main_exe.tableWidget
    map_ = main_exe.map
    layer = map_.layers[map_.selectedLayer]
    r = TabRange()
    r.bottomRow()
    # 仅在非编辑状态下联动表格
    if not main_exe.EditStatus:
        layer.selectedItems.clear()
        for range_ in tabWid.selectedRanges():
            ids = layer.table.loc[range(range_.topRow(), range_.bottomRow() + 1), 'ID']
            layer.selectedItems.extend(ids)
        RefreshCanvas(main_exe, use_base=True)


def addAttr(main_exe):
    '''点击“添加属性”按钮并OK后'''
    map_ = main_exe.map
    window = main_exe.WinNewAttr
    need_close = True
    try:
        # 未选择图层直接退出
        if map_.selectedLayer == -1:
            raise RuntimeError(u'图层错误', u'未选择图层！')
        layer = map_.layers[map_.selectedLayer]
        column_name = window.lineEdit.text()
        # TODO 数据库中的列名不支持哪些字符？还没处理
        # 输入的字段名已经存在，报错
        if column_name.lower() in map(str.lower, layer.table.columns):
            need_close = False
            raise RuntimeError(u'字段错误', f'该图层已经有"{column_name}"字段！')
        layer.add_attr(column_name, window.comboBox.currentText())
    # 运行错误则弹出对话框
    except RuntimeError as e:
        msgBox = QMessageBox()
        msgBox.setWindowTitle(e.args[0])
        msgBox.setText(f'\n{e.args[1]}\n')
        msgBox.addButton(QMessageBox.Ok)
        msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
        msgBox.exec_()
    finally:
        if need_close:
            window.close()
            TableUpdate(main_exe)

def TableItemChanged(main_exe,item):
    text=item.text()
    if item.whatsThis()=='int':
        text=int(text)
    elif item.whatsThis()=='float':
        text=float(text)
    cur_layer=main_exe.map.layers[main_exe.map.selectedLayer]
    cur_id=int(main_exe.tableWidget.item(item.row(),0).text())
    cur_dict={main_exe.tableWidget.horizontalHeaderItem(item.column()).text():text}
    main_exe.dbm.update_geometry(cur_layer,cur_id,cur_dict)

def selectGeoByStr(main_exe):
    '''属性表选择点击OK之后'''
    window = main_exe.WinSelect
    index = window.combo_layer.currentIndex()
    try:
        # 判断选择的图层
        if index is None or index >= len(main_exe.map.layers) or index < 0:
            raise RuntimeError('图层错误', '未选择正确图层！')
        layer = main_exe.map.layers[index]
        try:
            selected_geom = layer.Query(window.lineEdit_SelectState.text())
        except NameError:
            raise RuntimeError('表达式错误', '输入的字段名不存在。请重新输入表达式。')
        except Exception:
            raise RuntimeError('表达式错误', '表达式不合法。请重新输入表达式。')
        select_mode = window.comboBox_SelectMode.currentIndex()
        # 选择模式：交并差
        if select_mode == 0:
            layer.selectedItems = selected_geom
        elif select_mode == 1:
            layer.selectedItems = sorted(list(set(layer.selectedItems).union(selected_geom)))
        elif select_mode == 2:
            layer.selectedItems = sorted(list(set(layer.selectedItems).difference(selected_geom)))
        else:
            layer.selectedItems = sorted(list(set(layer.selectedItems).intersection(selected_geom)))
        window.close()
        if index == main_exe.map.selectedLayer:
            TableUpdate(main_exe)
            RefreshCanvas(main_exe, use_base=True)
        # 如果当前图层不是选择的图层，则跳转
        else:
            tree = main_exe.treeWidget
            topItem = tree.findItems('Layers', Qt.MatchStartsWith)[0]
            tree.setCurrentItem(topItem.child(index))
    except RuntimeError as e:
        msgBox = QMessageBox()
        msgBox.setWindowTitle(e.args[0])
        msgBox.setText(f'\n{e.args[1]}\n')
        msgBox.addButton(QMessageBox.Ok)
        msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
        msgBox.exec_()
