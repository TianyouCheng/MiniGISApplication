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

    self.Attributewidget = QWidget(self.centralwidget)
    self.Attributewidget.setGeometry(QRect(-300, 232, 200, 594))
    self.Attributewidget.setObjectName("Attributewidget")
    self.Attributewidget.setStyleSheet("background-color:transparent;")
    # self.bt_test = QPushButton(self.Attributewidget)
    # self.bt_test.setGeometry(QRect(5,5,80,80))
    # self.bt_test.setText("我是按钮")
    # self.bt_test.setObjectName("bt_test")
    # self.bt_test.setStyleSheet("background-color:white;")

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
        if StyleOn:
            with open('./UI/style_p.qss') as f2:
                qss = f2.read()
            self.setStyleSheet(qss)

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
        if StyleOn:
            with open('./UI/style.qss') as f2:
                qss = f2.read()
            self.setStyleSheet(qss)

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

def OperateStack(main_exe):
    if main_exe.IsOperStacked:
        # Pan
        animition_Oper_on=QPropertyAnimation(main_exe.tsButtonPan,b'pos')
        animition_Oper_on.setEasingCurve(QEasingCurve.OutExpo)
        animition_Oper_on.setDuration(1000)
        animition_Oper_on.setStartValue(QPoint(460,55))
        animition_Oper_on.setEndValue(QPoint(497, 55))

        # ZoomIn
        animition_ZoomIn_on = QPropertyAnimation(main_exe.tsButtonZoomIn, b'pos')
        animition_ZoomIn_on.setEasingCurve(QEasingCurve.OutExpo)
        animition_ZoomIn_on.setDuration(1000)
        animition_ZoomIn_on.setStartValue(QPoint(465, 55))
        animition_ZoomIn_on.setEndValue(QPoint(540, 55))

        # ZoomOut
        animition_ZoomOut_on = QPropertyAnimation(main_exe.tsButtonZoomOut, b'pos')
        animition_ZoomOut_on.setEasingCurve(QEasingCurve.OutExpo)
        animition_ZoomOut_on.setDuration(1000)
        animition_ZoomOut_on.setStartValue(QPoint(470, 55))
        animition_ZoomOut_on.setEndValue(QPoint(583, 55))

        # FullScale
        animition_FullScale_on = QPropertyAnimation(main_exe.tsButtonZoomScale, b'pos')
        animition_FullScale_on.setEasingCurve(QEasingCurve.OutExpo)
        animition_FullScale_on.setDuration(1000)
        animition_FullScale_on.setStartValue(QPoint(475, 55))
        animition_FullScale_on.setEndValue(QPoint(626, 55))

        # Widget
        animition_Widget_on = QPropertyAnimation(main_exe.widget_4, b'pos')
        animition_Widget_on.setEasingCurve(QEasingCurve.OutExpo)
        animition_Widget_on.setDuration(1000)
        animition_Widget_on.setStartValue(QPoint(520, 55))
        animition_Widget_on.setEndValue(QPoint(670, 55))

        animation_group=QParallelAnimationGroup(main_exe)
        animation_group.addAnimation(animition_Oper_on)
        animation_group.addAnimation(animition_ZoomIn_on)
        animation_group.addAnimation(animition_ZoomOut_on)
        animation_group.addAnimation(animition_FullScale_on)
        animation_group.addAnimation(animition_Widget_on)
        animation_group.start()

        # style
        main_exe.tsButtonOperateNone.setStyleSheet('QPushButton#tsButtonOperateNone{border-image:url(UI/icon/mouse.png)}QPushButton#tsButtonOperateNone:pressed{border-image:url(UI/icon/mouse_p.png)}')
        main_exe.tsButtonPan.setStyleSheet('QPushButton#tsButtonPan{border-image:url(UI/icon/pan1.png)}QPushButton#tsButtonPan:pressed{border-image:url(UI/icon/pan1_p.png)}')
        main_exe.tsButtonZoomIn.setStyleSheet('QPushButton#tsButtonZoomIn{border-image:url(UI/icon/zoomin.png)}QPushButton#tsButtonZoomIn:pressed{border-image:url(UI/icon/zoomin_p.png)}')
        main_exe.tsButtonZoomOut.setStyleSheet('QPushButton#tsButtonZoomOut{border-image:url(UI/icon/zoomout.png)}QPushButton#tsButtonZoomOut:pressed{border-image:url(UI/icon/zoomout_p.png)}')
        main_exe.tsButtonZoomScale.setStyleSheet('QPushButton#tsButtonZoomScale{border-image:url(UI/icon/zoomscale.png)}QPushButton#tsButtonZoomScale:pressed{border-image:url(UI/icon/zoomscale_p.png)}')

        main_exe.IsOperStacked = False
    else:
        # Pan
        animition_Oper_off = QPropertyAnimation(main_exe.tsButtonPan, b'pos')
        animition_Oper_off.setEasingCurve(QEasingCurve.OutExpo)
        animition_Oper_off.setDuration(1000)
        animition_Oper_off.setStartValue(QPoint(497, 55))
        animition_Oper_off.setEndValue(QPoint(460, 55))

        # ZoomIn
        animition_ZoomIn_off = QPropertyAnimation(main_exe.tsButtonZoomIn, b'pos')
        animition_ZoomIn_off.setEasingCurve(QEasingCurve.OutExpo)
        animition_ZoomIn_off.setDuration(1000)
        animition_ZoomIn_off.setStartValue(QPoint(540, 55))
        animition_ZoomIn_off.setEndValue(QPoint(465, 55))

        # ZoomOut
        animition_ZoomOut_off = QPropertyAnimation(main_exe.tsButtonZoomOut, b'pos')
        animition_ZoomOut_off.setEasingCurve(QEasingCurve.OutExpo)
        animition_ZoomOut_off.setDuration(1000)
        animition_ZoomOut_off.setStartValue(QPoint(582, 55))
        animition_ZoomOut_off.setEndValue(QPoint(470, 55))

        # FullScale
        animition_FullScale_off = QPropertyAnimation(main_exe.tsButtonZoomScale, b'pos')
        animition_FullScale_off.setEasingCurve(QEasingCurve.OutExpo)
        animition_FullScale_off.setDuration(1000)
        animition_FullScale_off.setStartValue(QPoint(626, 55))
        animition_FullScale_off.setEndValue(QPoint(475, 55))

        # Widget
        animition_Widget_off = QPropertyAnimation(main_exe.widget_4, b'pos')
        animition_Widget_off.setEasingCurve(QEasingCurve.OutExpo)
        animition_Widget_off.setDuration(1000)
        animition_Widget_off.setStartValue(QPoint(670, 55))
        animition_Widget_off.setEndValue(QPoint(520, 55))

        animation_group = QParallelAnimationGroup(main_exe)
        animation_group.addAnimation(animition_Oper_off)
        animation_group.addAnimation(animition_ZoomIn_off)
        animation_group.addAnimation(animition_ZoomOut_off)
        animation_group.addAnimation(animition_FullScale_off)
        animation_group.addAnimation(animition_Widget_off)
        animation_group.start()

        # style
        main_exe.tsButtonOperateNone.setStyleSheet('QPushButton#tsButtonOperateNone{border-image:url(UI/icon/mouse_s.png)}QPushButton#tsButtonOperateNone:pressed{border-image:url(UI/icon/mouse_p.png)}')
        main_exe.tsButtonPan.setStyleSheet(
            'QPushButton#tsButtonPan{border-image:url(UI/icon/pan1_s.png)}QPushButton#tsButtonPan:pressed{border-image:url(UI/icon/pan1_p.png)}')
        main_exe.tsButtonZoomIn.setStyleSheet(
            'QPushButton#tsButtonZoomIn{border-image:url(UI/icon/zoomin_s.png)}QPushButton#tsButtonZoomIn:pressed{border-image:url(UI/icon/zoomin_p.png)}')
        main_exe.tsButtonZoomOut.setStyleSheet(
            'QPushButton#tsButtonZoomOut{border-image:url(UI/icon/zoomout_s.png)}QPushButton#tsButtonZoomOut:pressed{border-image:url(UI/icon/zoomout_p.png)}')
        main_exe.tsButtonZoomScale.setStyleSheet(
            'QPushButton#tsButtonZoomScale{border-image:url(UI/icon/zoomscale_s.png)}QPushButton#tsButtonZoomScale:pressed{border-image:url(UI/icon/zoomscale_p.png)}')

        main_exe.IsOperStacked = True

def EditStack(main_exe):
    if main_exe.IsEditStacked:
        # # AddF
        # animition_AddF_on=QPropertyAnimation(main_exe.tsButtonAddFeature,b'pos')
        # animition_AddF_on.setEasingCurve(QEasingCurve.OutExpo)
        # animition_AddF_on.setDuration(1000)
        # animition_AddF_on.setStartValue(QPoint(770,55))
        # animition_AddF_on.setEndValue(QPoint(802, 55))
        #
        # # EditF
        # animition_EditF_on = QPropertyAnimation(main_exe.tsButtonEditFeature, b'pos')
        # animition_EditF_on.setEasingCurve(QEasingCurve.OutExpo)
        # animition_EditF_on.setDuration(1000)
        # animition_EditF_on.setStartValue(QPoint(780, 55))
        # animition_EditF_on.setEndValue(QPoint(846, 55))
        #
        # # Del
        # animition_Del_on = QPropertyAnimation(main_exe.tsButtonDel, b'pos')
        # animition_Del_on.setEasingCurve(QEasingCurve.OutExpo)
        # animition_Del_on.setDuration(1000)
        # animition_Del_on.setStartValue(QPoint(790, 55))
        # animition_Del_on.setEndValue(QPoint(890, 55))
        #
        # # AddA
        # animition_AddA_on = QPropertyAnimation(main_exe.tsButtonAddAttr, b'pos')
        # animition_AddA_on.setEasingCurve(QEasingCurve.OutExpo)
        # animition_AddA_on.setDuration(1000)
        # animition_AddA_on.setStartValue(QPoint(800, 55))
        # animition_AddA_on.setEndValue(QPoint(934, 55))
        #
        # # Attr
        # animition_Attr_on = QPropertyAnimation(main_exe.tsButtonAttr, b'pos')
        # animition_Attr_on.setEasingCurve(QEasingCurve.OutExpo)
        # animition_Attr_on.setDuration(1000)
        # animition_Attr_on.setStartValue(QPoint(830, 55))
        # animition_Attr_on.setEndValue(QPoint(978, 55))
        #
        # animation_group=QParallelAnimationGroup(main_exe)
        # animation_group.addAnimation(animition_AddF_on)
        # animation_group.addAnimation(animition_EditF_on)
        # animation_group.addAnimation(animition_Del_on)
        # animation_group.addAnimation(animition_AddA_on)
        # animation_group.addAnimation(animition_Attr_on)
        # animation_group.start()

        # # style
        # main_exe.tsButtonOperateNone.setStyleSheet('QPushButton#tsButtonOperateNone{border-image:url(UI/icon/mouse.png)}QPushButton#tsButtonOperateNone:pressed{border-image:url(UI/icon/mouse_p.png)}')
        # main_exe.tsButtonPan.setStyleSheet('QPushButton#tsButtonPan{border-image:url(UI/icon/pan1.png)}QPushButton#tsButtonPan:pressed{border-image:url(UI/icon/pan1_p.png)}')
        # main_exe.tsButtonZoomIn.setStyleSheet('QPushButton#tsButtonZoomIn{border-image:url(UI/icon/zoomin.png)}QPushButton#tsButtonZoomIn:pressed{border-image:url(UI/icon/zoomin_p.png)}')
        # main_exe.tsButtonZoomOut.setStyleSheet('QPushButton#tsButtonZoomOut{border-image:url(UI/icon/zoomout.png)}QPushButton#tsButtonZoomOut:pressed{border-image:url(UI/icon/zoomout_p.png)}')
        # main_exe.tsButtonZoomScale.setStyleSheet('QPushButton#tsButtonZoomScale{border-image:url(UI/icon/zoomscale.png)}QPushButton#tsButtonZoomScale:pressed{border-image:url(UI/icon/zoomscale_p.png)}')

        main_exe.IsEditStacked = False
    else:
        # AddF
        animition_AddF_off = QPropertyAnimation(main_exe.tsButtonAddFeature, b'geometry')
        animition_AddF_off.setEasingCurve(QEasingCurve.OutExpo)
        animition_AddF_off.setDuration(1000)
        animition_AddF_off.setStartValue(QRect(100, 0, 33, 35))
        animition_AddF_off.setEndValue(QRect(120, 0, 33, 35))
        animition_AddF_off.start()

        # # EditF
        # animition_EditF_off = QPropertyAnimation(main_exe.tsButtonEditFeature, b'pos')
        # animition_EditF_off.setEasingCurve(QEasingCurve.OutExpo)
        # animition_EditF_off.setDuration(1000)
        # animition_EditF_off.setStartValue(QPoint(846, 55))
        # animition_EditF_off.setEndValue(QPoint(780, 55))
        #
        # # Del
        # animition_Del_off = QPropertyAnimation(main_exe.tsButtonDel, b'pos')
        # animition_Del_off.setEasingCurve(QEasingCurve.OutExpo)
        # animition_Del_off.setDuration(1000)
        # animition_Del_off.setStartValue(QPoint(890, 55))
        # animition_Del_off.setEndValue(QPoint(790, 55))
        #
        # # AddA
        # animition_AddA_off = QPropertyAnimation(main_exe.tsButtonAddAttr, b'pos')
        # animition_AddA_off.setEasingCurve(QEasingCurve.OutExpo)
        # animition_AddA_off.setDuration(1000)
        # animition_AddA_off.setStartValue(QPoint(934, 55))
        # animition_AddA_off.setEndValue(QPoint(800, 55))
        #
        # # Attr
        # animition_Attr_off = QPropertyAnimation(main_exe.tsButtonAttr, b'pos')
        # animition_Attr_off.setEasingCurve(QEasingCurve.OutExpo)
        # animition_Attr_off.setDuration(1000)
        # animition_Attr_off.setStartValue(QPoint(978, 55))
        # animition_Attr_off.setEndValue(QPoint(830, 55))
        #
        # animation_group = QParallelAnimationGroup(main_exe)
        # animation_group.addAnimation(animition_AddF_off)
        # animation_group.addAnimation(animition_EditF_off)
        # animation_group.addAnimation(animition_Del_off)
        # animation_group.addAnimation(animition_AddA_off)
        # animation_group.addAnimation(animition_Attr_off)
        # animation_group.start()

        # # style
        # main_exe.tsButtonOperateNone.setStyleSheet('QPushButton#tsButtonOperateNone{border-image:url(UI/icon/mouse_s.png)}QPushButton#tsButtonOperateNone:pressed{border-image:url(UI/icon/mouse_p.png)}')
        # main_exe.tsButtonPan.setStyleSheet(
        #     'QPushButton#tsButtonPan{border-image:url(UI/icon/pan1_s.png)}QPushButton#tsButtonPan:pressed{border-image:url(UI/icon/pan1_p.png)}')
        # main_exe.tsButtonZoomIn.setStyleSheet(
        #     'QPushButton#tsButtonZoomIn{border-image:url(UI/icon/zoomin_s.png)}QPushButton#tsButtonZoomIn:pressed{border-image:url(UI/icon/zoomin_p.png)}')
        # main_exe.tsButtonZoomOut.setStyleSheet(
        #     'QPushButton#tsButtonZoomOut{border-image:url(UI/icon/zoomout_s.png)}QPushButton#tsButtonZoomOut:pressed{border-image:url(UI/icon/zoomout_p.png)}')
        # main_exe.tsButtonZoomScale.setStyleSheet(
        #     'QPushButton#tsButtonZoomScale{border-image:url(UI/icon/zoomscale_s.png)}QPushButton#tsButtonZoomScale:pressed{border-image:url(UI/icon/zoomscale_p.png)}')

        main_exe.IsEditStacked = True