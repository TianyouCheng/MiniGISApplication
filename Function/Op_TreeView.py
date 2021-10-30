'''
树形控件的相关操作函数
'''
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu
from PyQt5.QtGui import QIcon, QCursor,QFont
from PyQt5.QtCore import Qt
from .Map import Map
from .Layer import Layer
from .Geometry import *
from .Op_DrawLabel import RefreshCanvas
from .Op_TableView import TableUpdate
from .Op_AttributeWin import RefreshAttr

def treeCheckedChange(item: QTreeWidgetItem, column, main_exe):
    '''图层可见性发生变化，即列表勾选改变'''
    parent = item.parent()
    if parent is main_exe.treeWidget.findItems('Layers', Qt.MatchFlag.MatchStartsWith)[0]:
        index = parent.indexOfChild(item)
        main_exe.map.layers[index].visible = item.checkState(column) == Qt.CheckState.Checked
        RefreshCanvas(main_exe)


def treeCurrentItemChanged(current, main_exe):
    '''选择的当前操作图层发生变化'''
    layersItem = main_exe.treeWidget.findItems('Layers', Qt.MatchFlag.MatchStartsWith)[0]
    # 点到了layer标签，虽然不会显示被点选状态，但是还是触发该事件，需要引导一下
    if current is None:
        return
    if current.parent() is None:
        if layersItem.childCount() > 0:
            main_exe.treeWidget.setCurrentItem(layersItem.child(0))
            return
    # 点到了“点”、“线”...这些图层类型标签同理
    if current.parent() is not layersItem:
        main_exe.treeWidget.setCurrentItem(current.parent())
        return
    index = -1 if current is None or current.parent() is None \
        else current.parent().indexOfChild(current)
    main_exe.map.selectedLayer = index
    TableUpdate(main_exe)
    RefreshCanvas(main_exe, use_base=True)
    RefreshAttr(main_exe)


def TreeView_Init(self):
    # TREEVIEW


    pitem1 = QTreeWidgetItem(self.treeWidget, ['Layers'])
    pitem1.setFont(0,QFont("Microsoft YaHei", 11))
    if self.StyleOn:
        pitem1.setForeground(0, Qt.white)
    pitem1.setFlags(pitem1.flags() & ~Qt.ItemIsSelectable)
    self.treeWidget.itemChanged.connect(self.treeViewItemChanged)
    self.treeWidget.currentItemChanged.connect(self.treeViewCurrentItemChanged)

    self.treeWidget.header().setVisible(False)
    self.treeWidget.expandAll()

    # 设置右键菜单
    self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
    self.treeWidget.customContextMenuRequested.connect(lambda pos: TreeContextMenu(self, pos))


def TreeContextMenu(main_exe, pos):
    '''添加右键菜单内容，触发函数'''
    layersItem = main_exe.treeWidget.findItems('Layers', Qt.MatchFlag.MatchStartsWith)[0]
    item = main_exe.treeWidget.itemAt(pos)
    # 点到了非图层的东西（包括列表外、"Layer"标签、"点""线""面"标签）
    if item is None or item.parent() is None or item.parent() is not layersItem:
        return
    index = item.parent().indexOfChild(item)
    contextMenu = QMenu(main_exe.treeWidget)
    # 添加右键菜单的条目
    a_moveup = contextMenu.addAction(u'上移图层')
    a_moveup.setEnabled(index > 0)
    a_movedown = contextMenu.addAction(u'下移图层')
    a_movedown.setEnabled(index < item.parent().childCount() - 1)
    a_delLayer = contextMenu.addAction(u'删除该图层')
    contextMenu.popup(QCursor.pos())
    # a_moveup.triggered.connect(lambda: del_column(self, layer, col_idx))
    contextMenu.show()


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
    TreeViewUpdateList(self)
    TableUpdate(self)
    RefreshCanvas(self, use_base=True)


def TreeViewUpdateList(main_exe):
    '''
    更新图层列表
    :param tree: 树状视图
    :param map_: 地图
    :param style_on: bool，是否启用样式表
    '''
    tree = main_exe.treeWidget
    map_ = main_exe.map
    # 先断开事件，更新完再恢复
    tree.itemChanged.disconnect(main_exe.treeViewItemChanged)
    tree.currentItemChanged.disconnect(main_exe.treeViewCurrentItemChanged)
    layersItem = tree.findItems('Layers', Qt.MatchFlag.MatchStartsWith)[0]
    layersItem.takeChildren()
    for layer in map_.layers:
        newline = QTreeWidgetItem(layersItem)
        if main_exe.StyleOn:
            newline.setForeground(0, Qt.GlobalColor.white)
        newline.setCheckState(0, Qt.CheckState.Checked if layer.visible
                              else ~Qt.CheckState.Checked)
        # 点图层
        if layer.type == PointD:
            icon = QIcon('./UI/images/Point.png' if main_exe.StyleOn
                         else './UI/images/Point_G.png')
            typetxt = '点'
        # 线、多线图层
        elif layer.type in (Polyline, MultiPolyline):
            icon = QIcon('./UI/images/Line.png' if main_exe.StyleOn
                         else './UI/images/Line_G.png')
            typetxt = '线' if layer.type == Polyline else '多线'
        # 面、多面图层
        elif layer.type in (Polygon, MultiPolygon):
            icon = QIcon('./UI/images/Polygon.png' if main_exe.StyleOn
                         else './UI/images/Polygon_G.png')
            typetxt = '面' if layer.type == Polygon else '多面'
        else:
            raise TypeError('图层类型错误')

        newline.setText(0,layer.name)
        newline.setFont(0,QFont("Microsoft YaHei", 11))
        # 设置层级树样式
        newChildline = QTreeWidgetItem(newline, [typetxt])
        newChildline.setFont(0,QFont("Microsoft YaHei", 11))
        newChildline.setIcon(0, icon)
        newChildline.setFlags(newChildline.flags() & ~Qt.ItemIsSelectable)
        if main_exe.StyleOn:
            newChildline.setForeground(0, Qt.GlobalColor.white)

    tree.expandAll()
    tree.setCurrentItem(layersItem if map_.selectedLayer == -1
                        else layersItem.child(map_.selectedLayer))
    tree.itemChanged.connect(main_exe.treeViewItemChanged)
    tree.currentItemChanged.connect(main_exe.treeViewCurrentItemChanged)
