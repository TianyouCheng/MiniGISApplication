'''
表格控件的相关操作函数
'''
from PyQt5.QtWidgets import QTableWidgetItem,QAbstractItemView,QHeaderView, QTableWidget
from PyQt5.QtWidgets import QTableWidgetSelectionRange as TabRange
from PyQt5.QtGui import QFont,QColor,QBrush
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
    self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
    self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置第五列宽度自动调整，充满屏幕
    # 设置表头
    self.tableWidget.setHorizontalHeaderLabels(['序号', '姓名', '年龄', '地址', '成绩'])
    self.lines = []
    self.id = 1

    # 信号与槽函数
    self.tableWidget.itemSelectionChanged.connect(self.tableSelectionChanged)

def TableUpdate(main_exe):
    '''更新属性数据的表格内容'''
    tabWid = main_exe.tableWidget
    tabWid.itemSelectionChanged.disconnect(main_exe.tableSelectionChanged)
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
            if table.loc[row, 'ID'] in selectedItems:
                selected_rows.append(row)
        # 在表格中选择要素
        for row in selected_rows:
            tabWid.setRangeSelected(TabRange(row, 0, row, tabWid.columnCount() - 1), True)
    tabWid.itemSelectionChanged.connect(main_exe.tableSelectionChanged)


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

# TODO 添加属性的响应函数
def addAttr(main_exe):
    pass;