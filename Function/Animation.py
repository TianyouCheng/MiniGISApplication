'''
属性窗体切换动画
'''

from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QTableWidget,QSizePolicy,QTableWidgetItem,QHeaderView,QComboBox
from PyQt5.QtGui import QBrush, QColor,QFont
from PyQt5.QtCore import QRect,QPropertyAnimation,QPoint,QEasingCurve,QCoreApplication,Qt,QParallelAnimationGroup

def initAttr(self):
    '''UI里的test文件用于属性窗体的编写，编写完成后记得删除'''
    self.tsButtonZoomScale.raise_()
    self.tsButtonZoomOut.raise_()
    self.tsButtonZoomIn.raise_()
    self.tsButtonPan.raise_()
    self.tsButtonOperateNone.raise_()

    # self.tsButtonAttr.raise_()
    self.tsButtonAddAttr.raise_()
    self.tsButtonDel.raise_()
    self.tsButtonEditFeature.raise_()
    self.tsButtonAddFeature.raise_()
    self.tsButtonEdit.raise_()

    self.Attributewidget = QWidget(self.centralwidget)
    self.Attributewidget.setGeometry(QRect(-300, 232, 200, 594))
    self.Attributewidget.setObjectName("Attributewidget")
    self.Attributewidget.setStyleSheet("background-color:transparent;")

    self.AttrtableWidget = QTableWidget(self.Attributewidget)
    self.AttrtableWidget.setGeometry(QRect(20, 40, 159, 360))
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.AttrtableWidget.sizePolicy().hasHeightForWidth())
    self.AttrtableWidget.setSizePolicy(sizePolicy)
    self.AttrtableWidget.setLineWidth(1)
    self.AttrtableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    self.AttrtableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    self.AttrtableWidget.setShowGrid(False)
    self.AttrtableWidget.setObjectName("AttrtableWidget")
    self.AttrtableWidget.setStyleSheet("border: 0px")
    self.AttrtableWidget.setColumnCount(2)
    self.AttrtableWidget.setRowCount(11)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(0, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(1, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(2, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(3, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(4, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(5, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(6, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(7, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(8, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(9, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setVerticalHeaderItem(10, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setHorizontalHeaderItem(0, item)
    item = QTableWidgetItem()
    self.AttrtableWidget.setHorizontalHeaderItem(1, item)
    self.bt_Apply = QPushButton(self.Attributewidget)
    self.bt_Apply.setGeometry(QRect(50, 440, 101, 91))
    self.bt_Apply.setObjectName("bt_Apply")

    for i in range(self.AttrtableWidget.rowCount()):
        item=QTableWidgetItem()
        item.setFlags(Qt.ItemFlag(0))
        item.setFlags(Qt.ItemIsEnabled)
        item.setFont(QFont("Microsoft YaHei",11))
        if self.StyleOn:
            item.setForeground(QBrush(QColor(255, 255, 255)))
        self.AttrtableWidget.setItem(i, 0, item)


        item = QTableWidgetItem()
        # 设置项的可编辑属性
        if i not in [2,7,8,9]:
            item.setFlags(Qt.ItemFlag(0))
            item.setFlags(Qt.ItemIsEnabled)
        if self.StyleOn:
            item.setForeground(QBrush(QColor(255, 255, 255)))
        self.AttrtableWidget.setItem(i, 1, item)

    self.AttrtableWidget.horizontalHeader().setVisible(False)
    self.AttrtableWidget.verticalHeader().setVisible(False)
    item = self.AttrtableWidget.verticalHeaderItem(0)
    _translate = QCoreApplication.translate
    item.setText(_translate("Form", "OutlineColor"))
    item = self.AttrtableWidget.verticalHeaderItem(1)
    item.setText(_translate("Form", "OutlineStyle"))
    item = self.AttrtableWidget.verticalHeaderItem(2)
    item.setText(_translate("Form", "OutlineWidth"))
    item = self.AttrtableWidget.verticalHeaderItem(3)
    item.setText(_translate("Form", "SymbolColor"))
    item = self.AttrtableWidget.verticalHeaderItem(4)
    item.setText(_translate("Form", "注记"))
    item = self.AttrtableWidget.verticalHeaderItem(5)
    item.setText(_translate("Form", "可见性"))
    item = self.AttrtableWidget.verticalHeaderItem(6)
    item.setText(_translate("Form", "绑定字段"))
    item = self.AttrtableWidget.verticalHeaderItem(7)
    item.setText(_translate("Form", "水平偏移"))
    item = self.AttrtableWidget.verticalHeaderItem(8)
    item.setText(_translate("Form", "垂直偏移"))
    item = self.AttrtableWidget.verticalHeaderItem(9)
    item.setText(_translate("Form", "SymbolColor"))
    item = self.AttrtableWidget.verticalHeaderItem(10)
    item.setText(_translate("Form", "字体颜色"))
    item = self.AttrtableWidget.horizontalHeaderItem(0)
    item.setText(_translate("Form", "新建列"))
    item = self.AttrtableWidget.horizontalHeaderItem(1)
    item.setText(_translate("Form", "符号"))
    __sortingEnabled = self.AttrtableWidget.isSortingEnabled()
    self.AttrtableWidget.setSortingEnabled(False)
    item = self.AttrtableWidget.item(0, 0)
    item.setText(_translate("Form", "轮廓颜色"))
    item = self.AttrtableWidget.item(1, 0)
    item.setText(_translate("Form", "线型样式"))
    item = self.AttrtableWidget.item(2, 0)
    item.setText(_translate("Form", "轮廓宽度"))
    item = self.AttrtableWidget.item(3, 0)
    item.setText(_translate("Form", "填充颜色"))
    item = self.AttrtableWidget.item(5, 0)
    item.setText(_translate("Form", "可见性"))
    item = self.AttrtableWidget.item(6, 0)
    item.setText(_translate("Form", "绑定字段"))
    item = self.AttrtableWidget.item(7, 0)
    item.setText(_translate("Form", "水平偏移"))
    item = self.AttrtableWidget.item(8, 0)
    item.setText(_translate("Form", "垂直偏移"))
    item = self.AttrtableWidget.item(9, 0)
    item.setText(_translate("Form", "字体大小"))
    item = self.AttrtableWidget.item(10, 0)
    item.setText(_translate("Form", "字体颜色"))
    self.AttrtableWidget.setSortingEnabled(__sortingEnabled)
    self.AttrtableWidget.setColumnWidth(0, 70)
    self.AttrtableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    self.bt_Apply.setText(_translate("Form", "应用"))

def Switch(self, IsAttr, StyleOn):
    '''
    :param self: 调用主窗体各控件
    :param IsAttr: 判断当前是否为属性窗体
    :param StyleOn: 样式
    :return: None
    '''
    if not IsAttr:
        # if StyleOn:
        #     with open('./UI/style_p.qss') as f2:
        #         qss = f2.read()
        #     self.setStyleSheet(qss)

        # 设置移动动画。move的参数是移动到的地址
        self.animition_Tree_off=QPropertyAnimation(self.treeWidget,b'pos')
        self.animition_Tree_off.setEasingCurve(QEasingCurve.InExpo)
        self.animition_Tree_off.setDuration(300)
        self.animition_Tree_off.setStartValue(QPoint(0, 0))
        self.animition_Tree_off.setEndValue(QPoint(-300, 0))
        self.animition_Tree_off.start()
        self.animition_Attr_On=QPropertyAnimation(self.Attributewidget,b'pos')
        self.animition_Attr_On.setEasingCurve(QEasingCurve.InExpo)
        self.animition_Attr_On.setDuration(300)
        self.animition_Attr_On.setStartValue(QPoint(-300, 232))
        self.animition_Attr_On.setEndValue(QPoint(1, 232))
        self.animition_Attr_On.start()
        self.IsAttr=True
    else:
        # if StyleOn:
        #     with open('./UI/style.qss') as f2:
        #         qss = f2.read()
        #     self.setStyleSheet(qss)

        self.animition_Tree_on=QPropertyAnimation(self.treeWidget,b'pos')
        self.animition_Tree_on.setEasingCurve(QEasingCurve.InExpo)
        self.animition_Tree_on.setDuration(300)
        self.animition_Tree_on.setStartValue(QPoint(-300,0))
        self.animition_Tree_on.setEndValue(QPoint(0,0))
        self.animition_Tree_on.start()
        self.animition_Attr_Off=QPropertyAnimation(self.Attributewidget,b'pos')
        self.animition_Attr_Off.setEasingCurve(QEasingCurve.InExpo)
        self.animition_Attr_Off.setDuration(300)
        self.animition_Attr_Off.setStartValue(QPoint(1, 232))
        self.animition_Attr_Off.setEndValue(QPoint(-300, 232))
        self.animition_Attr_Off.start()
        self.IsAttr=False

def OperateStack(main_exe,dua=1000):
    '''
    四元判断：指针叠起，编辑叠起
    :param main_exe:
    :return:
    '''
    # 指针叠起的四个按钮控件
    bt_Oper = [main_exe.tsButtonPan, main_exe.tsButtonZoomIn, main_exe.tsButtonZoomOut, main_exe.tsButtonZoomScale]
    bt_Oper_pos0 = [420] # 指针后四按钮叠起位置
    bt_Oper_pos1 = [458] # 指针后四按钮展开初始位置
    # 指针叠起后的8个控件
    bt_OperRest = [main_exe.tsButtonSelect, main_exe.tsButtonSelectByAttr,main_exe.tsButtonNewLayer, main_exe.tsButtonEdit,
                   main_exe.tsButtonAddFeature, main_exe.tsButtonEditFeature, main_exe.tsButtonDel,
                   main_exe.tsButtonAddAttr, main_exe.tsButtonAttr,main_exe.tsButtonChart,main_exe.tsButtonMap]
    bt_OperRest_pos0=[458] # 指针后8控件叠起位置
    bt_OperRest_pos1=[618] # 指针后8控件展开初始位置
    interval_small=38 # 按钮间隔
    interval_big=41 # 叠起按钮与后一按钮间隔
    ypos = 45 # 纵向坐标

    # 扩展四按钮位置坐标
    for i in range(1,len(bt_Oper)):
        bt_Oper_pos0.append(bt_Oper_pos0[0])
        bt_Oper_pos1.append(bt_Oper_pos1[0]+i*interval_small)

    # 使用判断来切换坐标
    if not main_exe.IsOperStacked:
        tp_pos=bt_Oper_pos0
        bt_Oper_pos0=bt_Oper_pos1
        bt_Oper_pos1=tp_pos
        tp_pos = bt_OperRest_pos0
        bt_OperRest_pos0 = bt_OperRest_pos1
        bt_OperRest_pos1 = tp_pos

        # style
        main_exe.tsButtonOperateNone.setStyleSheet('QPushButton#tsButtonOperateNone{border-image:url(UI/icon/mouse_s.png)}QPushButton#tsButtonOperateNone:pressed{border-image:url(UI/icon/mouse_p.png)}')
    else:
        # style
        main_exe.tsButtonOperateNone.setStyleSheet(
            'QPushButton#tsButtonOperateNone{border-image:url(UI/icon/mouse.png)}QPushButton#tsButtonOperateNone:pressed{border-image:url(UI/icon/mouse_p.png)}')
    animation_group = QParallelAnimationGroup(main_exe)

    # 指针后四按钮叠起/展开动画
    for i in range(len(bt_Oper)):
        animition_Oper_on=QPropertyAnimation(bt_Oper[i],b'pos')
        animition_Oper_on.setEasingCurve(QEasingCurve.OutExpo)
        animition_Oper_on.setDuration(dua)
        animition_Oper_on.setStartValue(QPoint(bt_Oper_pos0[i],ypos))
        animition_Oper_on.setEndValue(QPoint(bt_Oper_pos1[i], ypos))
        animation_group.addAnimation(animition_Oper_on)

    # 指针后八按钮叠起/展开动画
    # 指针叠起，编辑未叠
    if not main_exe.IsEditStacked:
        for i in range(len(bt_OperRest)):
            animition_Widget_on =QPropertyAnimation(bt_OperRest[i], b'pos')
            animition_Widget_on.setEasingCurve(QEasingCurve.OutExpo)
            animition_Widget_on.setDuration(dua)
            animition_Widget_on.setStartValue(QPoint(bt_OperRest_pos0[0]+i*interval_small, ypos))
            animition_Widget_on.setEndValue(QPoint(bt_OperRest_pos1[0]+i*interval_small, ypos))
            animation_group.addAnimation(animition_Widget_on)
    # 指针叠起，编辑叠起
    # 若编辑叠起,需分三类按钮考虑
    else:
        for i in range(3):
            animition_Widget_on =QPropertyAnimation(bt_OperRest[i], b'pos')
            animition_Widget_on.setEasingCurve(QEasingCurve.OutExpo)
            animition_Widget_on.setDuration(dua)
            animition_Widget_on.setStartValue(QPoint(bt_OperRest_pos0[0]+i*interval_small, ypos))
            animition_Widget_on.setEndValue(QPoint(bt_OperRest_pos1[0]+i*interval_small, ypos))
            animation_group.addAnimation(animition_Widget_on)
        for i in range(3,8):
            animition_Widget_on = QPropertyAnimation(bt_OperRest[i], b'pos')
            animition_Widget_on.setEasingCurve(QEasingCurve.OutExpo)
            animition_Widget_on.setDuration(dua)
            animition_Widget_on.setStartValue(QPoint(bt_OperRest_pos0[0]+3*interval_small, ypos))
            animition_Widget_on.setEndValue(QPoint(bt_OperRest_pos1[0]+3*interval_small, ypos))
            animation_group.addAnimation(animition_Widget_on)
        for i in range(8,11):
            animition_Widget_on = QPropertyAnimation(bt_OperRest[i], b'pos')
            animition_Widget_on.setEasingCurve(QEasingCurve.OutExpo)
            animition_Widget_on.setDuration(dua)
            animition_Widget_on.setStartValue(QPoint(bt_OperRest_pos0[0] + 3 * interval_small + interval_big+(i-8)*interval_small, ypos))
            animition_Widget_on.setEndValue(QPoint(bt_OperRest_pos1[0] + 3 * interval_small + interval_big+(i-8)*interval_small, ypos))
            animation_group.addAnimation(animition_Widget_on)

    animation_group.start()

    main_exe.IsOperStacked = not main_exe.IsOperStacked



def EditStack(main_exe,dua=1000):
    # 编辑叠起的四个按钮控件
    bt_Edit = [main_exe.tsButtonAddFeature, main_exe.tsButtonEditFeature, main_exe.tsButtonDel,
                           main_exe.tsButtonAddAttr]
    bt_Edit_pos0 = [693+38]  # 编辑后四按钮叠起位置
    bt_Edit_pos1 = [734+38]  # 编辑后四按钮展开初始位置

    interval_small = 38  # 按钮间隔
    interval_big = 41  # 叠起按钮与后一按钮间隔
    # 编辑叠起后一控件
    bt_EditRest=[main_exe.tsButtonAttr,main_exe.tsButtonChart,main_exe.tsButtonMap]
    bt_EditRest_pos0 = [bt_Edit_pos0[0]+interval_big]  # 编辑后一控件叠起位置
    bt_EditRest_pos1 = [bt_Edit_pos1[0]+interval_small*(len(bt_Edit)-1)+interval_big]  # 编辑后一控件展开初始位置
    interval_OperStack=160
    ypos = 45  # 纵向坐标


    for i in range(1, len(bt_Edit)):
        bt_Edit_pos0.append(bt_Edit_pos0[0])
        bt_Edit_pos1.append(bt_Edit_pos1[0] + i * interval_small)


    animation_group = QParallelAnimationGroup(main_exe)

    if not main_exe.IsEditStacked:
        tp_pos = bt_Edit_pos0
        bt_Edit_pos0 = bt_Edit_pos1
        bt_Edit_pos1 = tp_pos
        tp_pos = bt_EditRest_pos0
        bt_EditRest_pos0 = bt_EditRest_pos1
        bt_EditRest_pos1 = tp_pos
        main_exe.tsButtonEdit.setStyleSheet('QPushButton#tsButtonEdit{border-image:url(UI/icon/edit_s.png)}QPushButton#tsButtonOperateNone:pressed{border-image:url(UI/icon/edit_p.png)}')
    else:
        main_exe.tsButtonEdit.setStyleSheet('QPushButton#tsButtonEdit{border-image:url(UI/icon/edit_p.png)}QPushButton#tsButtonOperateNone:pressed{border-image:url(UI/icon/edit_p.png)}')


    if main_exe.IsOperStacked:
        for i in range(len(bt_Edit_pos0)):
            bt_Edit_pos0[i]=bt_Edit_pos0[i]-interval_OperStack
            bt_Edit_pos1[i] = bt_Edit_pos1[i] - interval_OperStack
        for i in range(len(bt_EditRest_pos0)):
            bt_EditRest_pos0[i]=bt_EditRest_pos0[i]-interval_OperStack
            bt_EditRest_pos1[i] = bt_EditRest_pos1[i] - interval_OperStack


    # 指针未叠，编辑未叠
    for i in range(len(bt_EditRest)):
        animition_Attr_on=QPropertyAnimation(bt_EditRest[i],b'pos')
        animition_Attr_on.setEasingCurve(QEasingCurve.OutExpo)
        animition_Attr_on.setDuration(dua)
        animition_Attr_on.setStartValue(QPoint(bt_EditRest_pos0[0]+i*interval_small,ypos))
        animition_Attr_on.setEndValue(QPoint(bt_EditRest_pos1[0]+i*interval_small, ypos))
        animation_group.addAnimation(animition_Attr_on)

    # Widget
    for i in range(len(bt_Edit)):
        animition_Widget_off = QPropertyAnimation(bt_Edit[i], b'pos')
        animition_Widget_off.setEasingCurve(QEasingCurve.OutExpo)
        animition_Widget_off.setDuration(dua)
        animition_Widget_off.setStartValue(QPoint(bt_Edit_pos0[i], ypos))
        animition_Widget_off.setEndValue(QPoint(bt_Edit_pos1[i], ypos))
        animation_group.addAnimation(animition_Widget_off)

    animation_group.start()

    main_exe.IsEditStacked = not main_exe.IsEditStacked