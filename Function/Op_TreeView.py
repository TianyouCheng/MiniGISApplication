'''
树形控件的相关操作函数
'''
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu,QAbstractItemView, QMessageBox
from PyQt5.QtGui import QIcon, QCursor,QFont
from PyQt5.QtCore import Qt
from .Layer import Layer
from .Geometry import *
from .Op_DrawLabel import RefreshCanvas
from .Op_TableView import TableUpdate
from .Op_AttributeWin import RefreshAttr

# 定义可拖拽的QTreeWidget
# 以后每次使用Qt Designer更新界面后，都需要重新在MainGUI.py中导入该类，并将Treewidget用该类初始化！！！
class DragableTree(QTreeWidget):
    def __init__(self,parent):
        super(DragableTree, self).__init__(parent)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.m_bAdjustPos=True
        self.btPressed = False
        self.main_exe = None    # 用于指向主程序的指针

    # https://www.tutorialspoint.com/pyqt/pyqt_drag_and_drop.htm
    # DragEnterEvent provides an event which is sent to the target widget as dragging action enters it.
    #
    # DragMoveEvent is used when the drag and drop action is in progress.
    #
    # DragLeaveEvent is generated as the drag and drop action leaves the widget.
    #
    # DropEvent, on the other hand, occurs when the drop is completed. The event’s proposed action can be accepted or rejected conditionally.

    # 用dropevent代替松开事件

    def set_exe(self, main_exe):
        '''在初始化时用，用于回指向Main_exe'''
        self.main_exe = main_exe

    def mousePressEvent(self, e):
        super(DragableTree, self).mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            self.btPressed = True
            self.m_bAdjustPos = True
            self.m_iLastItemIndex = -1 # 要拖放的点的父节点索引
            self.m_iCurrItemIndex = -1 # 要拖放的点相对父节点索引
            self.m_iLastParentIndex = -1 # 要放到的点的父节点索引
            self.m_iCurrParentIndex = -1 # 要放到的点相对父节点索引
            pt = e.pos()
            currItem = self.itemAt(pt)
            if currItem:
                parentItem = currItem.parent()
                if parentItem: # 当前选中的是子节点
                    self.m_iLastParentIndex = self.indexOfTopLevelItem(parentItem) # 获取父节点和本身相对于父节点的索引
                    self.m_iLastItemIndex = parentItem.indexOfChild(currItem)
                else: # 选中的是父节点
                    self.m_iLastParentIndex = self.indexOfTopLevelItem(currItem) # 对顶级节点的操作

    def dropEvent(self,e):
        if self.btPressed:
            pt=e.pos()
            currItem=self.itemAt(pt)
            if currItem and self.m_bAdjustPos: # 父节点不能调整顺序，即只能调整子节点顺序
                # 调整子节点顺序分在同一个父节点下不在同一个父节点下
                parentItem=currItem.parent()
                if parentItem: # 说明选中的是子节点
                    self.m_iCurrParentIndex=self.indexOfTopLevelItem(parentItem)
                    self.m_iCurrItemIndex=parentItem.indexOfChild(currItem)
                else: # 选中的是父节点
                    self.m_iCurrParentIndex=self.indexOfTopLevelItem(currItem)
                self.adjustItemInfo(self.m_iLastParentIndex,self.m_iLastItemIndex,self.m_iCurrParentIndex,self.m_iCurrItemIndex)
                TreeViewUpdateList(self.main_exe)
                TableUpdate(self.main_exe)
                RefreshCanvas(self.main_exe)
            self.m_bAdjustPos=False
            self.btPressed=False
        else:
            e.ignore()

    def adjustItemInfo(self,lastParIndex,lastSubIndex,currParIndex,currSubIndex):
        # print(lastParIndex,lastSubIndex,currParIndex,currSubIndex)
        if lastParIndex==-1: # 没有选中交换的节点
            return
        if lastSubIndex==-1: # 选中的是父节点，不能拖入到其它级别中
            return
        if currParIndex==-1: # 要拖入的节点不存在
            return
        if lastParIndex==currParIndex and lastSubIndex==currSubIndex:
            return
        # lastParItem=self.topLevelItem(self.m_iLastParentIndex) # 获取要拖动的节点的父节点
        # lastSubItem=lastParItem.takeChild(self.m_iLastItemIndex) # 获取要拖动的节点并移除
        # currParItem=self.topLevelItem(self.m_iCurrParentIndex) # 在指定位置插入节点
        if self.m_iCurrItemIndex==-1:
            self.m_iCurrItemIndex=0
            # currParItem.insertChild(self.m_iCurrItemIndex,lastSubItem)
        # else:
        #     currParItem.insertChild(self.m_iCurrItemIndex,lastSubItem)
        self.main_exe.map.MoveLayer(self.m_iLastItemIndex, self.m_iCurrItemIndex)


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

    self.treeWidget.set_exe(self)
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
    contextMenu = QMenu(main_exe.treeWidget)
    # 点到了非图层的东西（包括列表外、"Layer"标签、"点""线""面"标签）
    if not (item is None or item.parent() is None or item.parent() is not layersItem):
        index = item.parent().indexOfChild(item)
        # 添加右键菜单的条目
        a_moveup = contextMenu.addAction(u'上移图层')
        a_moveup.setEnabled(index > 0)
        a_moveup.triggered.connect(lambda: move_up(main_exe, index))
        a_movedown = contextMenu.addAction(u'下移图层')
        a_movedown.setEnabled(index < item.parent().childCount() - 1)
        a_movedown.triggered.connect(lambda: move_down(main_exe, index))
        a_delLayer = contextMenu.addAction(u'删除该图层')
        a_delLayer.triggered.connect(lambda: check_del_layer(main_exe, index))
    a_clearLayers = contextMenu.addAction(u'清空所有图层')
    a_clearLayers.setEnabled(layersItem.childCount() > 0)
    a_clearLayers.triggered.connect(lambda: check_clear_layer(main_exe))
    contextMenu.popup(QCursor.pos())
    contextMenu.show()

    def move_up(main_exe_, layer_index):
        '''图层上移，然后更新界面'''
        main_exe_.map.MoveUpLayer(layer_index)
        TreeViewUpdateList(main_exe_)
        TableUpdate(main_exe_)
        RefreshCanvas(main_exe_)

    def move_down(main_exe_, layer_index):
        '''图层下移，然后更新界面'''
        main_exe_.map.MoveDownLayer(layer_index)
        TreeViewUpdateList(main_exe_)
        TableUpdate(main_exe_)
        RefreshCanvas(main_exe_)

    def check_del_layer(main_exe_, layer_index):
        '''弹出消息框，询问是否确定删除图层'''
        def del_layer(_main_exe, _index_):
            '''确实删除图层，并更新界面'''
            _main_exe.map.DelLayer(_index_)
            TreeViewUpdateList(_main_exe)
            TableUpdate(_main_exe)
            RefreshCanvas(_main_exe)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setWindowTitle('删除图层')
        msgBox.setText(f'\n确认删除"{main_exe_.map.layers[layer_index].name}"图层？\n')
        btn_ok = msgBox.addButton(QMessageBox.Ok)
        msgBox.addButton(QMessageBox.Cancel)
        btn_ok.clicked.connect(lambda: del_layer(main_exe_, layer_index))
        msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
        msgBox.exec_()

    def check_clear_layer(main_exe_):
        '''弹出消息框，询问是否清空图层'''
        def clear_layer(_main_exe):
            '''确实删除图层，并更新界面'''
            _main_exe.map.ClearLayers()
            TreeViewUpdateList(_main_exe)
            TableUpdate(_main_exe)
            RefreshCanvas(_main_exe)

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setWindowTitle('清空图层')
        msgBox.setText(u'\n确认清空所有图层？\n')
        btn_ok = msgBox.addButton(QMessageBox.Ok)
        msgBox.addButton(QMessageBox.Cancel)
        btn_ok.clicked.connect(lambda: clear_layer(main_exe_))
        msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
        msgBox.exec_()


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
    elif txtType == '多线':
        layer = Layer(MultiPolyline, txtName)
    elif txtType == '多面':
        layer = Layer(MultiPolygon, txtName)
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
