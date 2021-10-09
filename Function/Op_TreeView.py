'''
树形控件的相关操作函数
'''
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt
from .Map import Map
from .Layer import Layer
from .Geometry import *
from .Op_DrawLabel import Refresh
from .Op_TableView import TableUpdate

def treeCheckedChange(item: QTreeWidgetItem, column, main_exe):
    '''图层可见性发生变化，即列表勾选改变'''
    parent = item.parent()
    if parent is main_exe.treeWidget.findItems('Layers', Qt.MatchFlag.MatchStartsWith)[0]:
        index = parent.indexOfChild(item)
        main_exe.map.layers[index].visible = item.checkState(column) == Qt.CheckState.Checked
        Refresh(main_exe, QCursor.pos())


def treeCurrentItemChanged(current, main_exe):
    '''选择的当前操作图层发生变化'''
    layersItem = main_exe.treeWidget.findItems('Layers', Qt.MatchFlag.MatchStartsWith)[0]
    # 点到了layer标签，虽然不会显示被点选状态，但是还是触发该事件，需要引导一下
    if current is None or current.parent() is None:
        if layersItem.childCount() > 0:
            main_exe.treeWidget.setCurrentItem(layersItem.child(0))
            main_exe.update()
            return
    # 点到了“点”、“线”...这些图层类型标签同理
    if current.parent() is not layersItem:
        main_exe.treeWidget.setCurrentItem(current.parent())
        return
    index = -1 if current is None or current.parent() is None \
        else current.parent().indexOfChild(current)
    main_exe.map.selectedLayer = index
    Refresh(main_exe, QCursor.pos(), use_base=True)
    TableUpdate(main_exe.tableWidget, main_exe.map.layers[index], main_exe.StyleOn)


def TreeView_Init(self):
    # TREEVIEW


    pitem1 = QTreeWidgetItem(self.treeWidget, ['Layers'])
    if self.StyleOn:
        pitem1.setForeground(0, Qt.white)
    pitem1.setFlags(pitem1.flags() & ~Qt.ItemIsSelectable)
    # citem1 = QTreeWidgetItem(pitem1, ['Mountain'])
    # citem11 = QTreeWidgetItem(citem1, ['Mountain Symbol'])
    # citem11.setIcon(0, QIcon('./UI/icon1.png'))
    # citem2 = QTreeWidgetItem(pitem1, ['Street'])
    # citem22 = QTreeWidgetItem(citem2, ['Street Symbol'])
    # citem22.setIcon(0, QIcon('./UI/icon1.png'))
    # citem3 = QTreeWidgetItem(pitem1, ['Water'])
    # citem33 = QTreeWidgetItem(citem3, ['Water Symbol'])
    # citem33.setIcon(0, QIcon('./UI/icon1.png'))
    # citem4 = QTreeWidgetItem(pitem1, ['City'])
    # citem44 = QTreeWidgetItem(citem4, ['City Symbol'])
    #
    # citem44.setForeground(0,Qt.red)
    # citem44.setIcon(0, QIcon('./UI/icon1.png'))
    # citem1.setCheckState(0, Qt.Checked)
    # citem2.setCheckState(0, Qt.Checked)
    # citem3.setCheckState(0, Qt.Checked)
    # citem4.setCheckState(0, Qt.Checked)
    self.treeWidget.itemChanged.connect(lambda item, column:
                                        treeCheckedChange(item, column, self))
    self.treeWidget.currentItemChanged.connect(lambda current, previous:
                                               treeCurrentItemChanged(current, self))

    self.treeWidget.header().setVisible(False)
    self.treeWidget.expandAll()

def NewLayer(self):
    txtName = self.Winnewlayer.lineEdit.text()
    layersItem = self.treeWidget.findItems('Layers', Qt.MatchFlag.MatchStartsWith)[0]
    if txtName.replace(' ', '') == '':
        txtName = 'layer {}'.format(layersItem.childCount())
    txtType = self.Winnewlayer.comboBox.currentText()
    if txtType == '点':
        layer = Layer(PointD, txtName)
    elif txtType == '线':
        layer = Layer(Polyline, txtName)
    elif txtType == '面':
        layer = Layer(Polygon, txtName)
    else:
        raise TypeError('图层类型错误')
    pos = self.map.selectedLayer if self.map.selectedLayer != -1 else 0
    self.map.AddLayer(layer, pos)
    self.Winnewlayer.close()
    TreeViewUpdateList(self.treeWidget, self.map, self.StyleOn)
    self.treeWidget.setCurrentItem(layersItem.child(pos))


def TreeViewUpdateList(tree: QTreeWidget, map_: Map, style_on):
    '''
    更新图层列表
    :param tree: 树状视图
    :param map_: 地图
    :param style_on: bool，是否启用样式表
    '''
    layersItem = tree.findItems('Layers', Qt.MatchFlag.MatchStartsWith)[0]
    layersItem.takeChildren()
    for layer in map_.layers:
        newline = QTreeWidgetItem(layersItem)
        if style_on:
            newline.setForeground(0, Qt.GlobalColor.white)
        newline.setCheckState(0, Qt.CheckState.Checked if layer.visible
                              else ~Qt.CheckState.Checked)
        # 点图层
        if layer.type == PointD:
            icon = QIcon('./UI/images/Point.png' if style_on
                         else './UI/images/Point_G.png')
            typetxt = '点'
        # 线、多线图层
        elif layer.type in (Polyline, MultiPolyline):
            icon = QIcon('./UI/images/Line.png' if style_on
                         else './UI/images/Line_G.png')
            typetxt = '线' if layer.type == Polyline else '多线'
        # 面、多面图层
        elif layer.type in (Polygon, MultiPolygon):
            icon = QIcon('./UI/images/Polygon.png' if style_on
                         else './UI/images/Polygon_G.png')
            typetxt = '面' if layer.type == Polygon else '多面'
        else:
            raise TypeError('图层类型错误')

        newline.setText(0,layer.name)
        # 设置层级树样式
        newChildline = QTreeWidgetItem(newline, [typetxt])
        newChildline.setIcon(0, icon)
        newChildline.setFlags(newChildline.flags() & ~Qt.ItemIsSelectable)
        if style_on:
            newChildline.setForeground(0, Qt.GlobalColor.white)

    tree.expandAll()
    tree.setCurrentItem(layersItem if map_.selectedLayer == -1
                        else layersItem.child(map_.selectedLayer))
