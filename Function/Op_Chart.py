'''
图表相关
'''
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget,QMessageBox
from PyQt5.QtCore import QSize,QUrl,QPropertyAnimation,QPoint,QEasingCurve,QCoreApplication,QRect
from PyQt5.QtWebEngineWidgets import QWebEngineSettings,QWebEngineView
from .Geometry import *

def initChart(main_exe):
    webSettings=QWebEngineSettings.globalSettings()
    webSettings.setAttribute(QWebEngineSettings.JavascriptEnabled,True)
    webSettings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
    webSettings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
    main_exe.webView=QWebEngineView(main_exe.widget_4)
    main_exe.webView.setGeometry(QRect(1500, 1, 1005, 480))
    main_exe.webView.setMinimumSize(QSize(1000, 480))
    main_exe.webView.setStyleSheet("background-color:white;\n")
    main_exe.webView.load(QUrl('file:///'+'src/render.html'))

def SwitchChart(main_exe):
    pos_y=1
    pos_x_s=5
    pos_x_e = 1500
    if not main_exe.IsChart:
        runJS(main_exe)
        # chart飞走动画
        main_exe.animation = QPropertyAnimation(main_exe.Drawlabel, b'pos')
        main_exe.animation.setEasingCurve(QEasingCurve.InExpo)
        main_exe.animation.setDuration(300)
        main_exe.animation.setStartValue(QPoint(pos_x_s, pos_y))
        main_exe.animation.setEndValue(QPoint(pos_x_e, pos_y))
        main_exe.animation.start()
        # web飞来动画
        main_exe.animation1 = QPropertyAnimation(main_exe.webView, b'pos')
        main_exe.animation1.setEasingCurve(QEasingCurve.InExpo)
        main_exe.animation1.setDuration(300)
        main_exe.animation1.setStartValue(QPoint(pos_x_e, pos_y))
        main_exe.animation1.setEndValue(QPoint(pos_x_s, pos_y))
        main_exe.animation1.start()

    else:
        # chart飞来动画
        main_exe.animation = QPropertyAnimation(main_exe.Drawlabel, b'pos')
        main_exe.animation.setEasingCurve(QEasingCurve.InExpo)
        main_exe.animation.setDuration(300)
        main_exe.animation.setStartValue(QPoint(pos_x_e, pos_y))
        main_exe.animation.setEndValue(QPoint(pos_x_s, pos_y))
        main_exe.animation.start()
        # web飞走动画
        main_exe.animation1 = QPropertyAnimation(main_exe.webView, b'pos')
        main_exe.animation1.setEasingCurve(QEasingCurve.InExpo)
        main_exe.animation1.setDuration(300)
        main_exe.animation1.setStartValue(QPoint(pos_x_s, pos_y))
        main_exe.animation1.setEndValue(QPoint(pos_x_e, pos_y))
        main_exe.animation1.start()
    main_exe.IsChart = not main_exe.IsChart

def runJS(main_exe):
    '''点击“图标”按钮并OK后'''
    map_ = main_exe.map
    window = main_exe.WinChart
    need_close = True
    try:
        # 未选择图层直接退出
        if map_.selectedLayer==-1:
            raise RuntimeError(u'图层错误',u'未选择图层！')
        layer=map_.layers[map_.selectedLayer]
        column_name=window.comboBox.currentText()
        mark_name=window.comboBox_2.currentText()
        if type(layer.table[column_name][0])==str:
            need_close = False
            raise RuntimeError(u'类型错误', u'请选择数值类型！')
        IDlist=list(layer.table[mark_name])
        valuelist=list(layer.table[column_name])
        js = "setValue({},{})".format(IDlist, valuelist)
        main_exe.webView.page().runJavaScript(js)
    except RuntimeError as e:
        msgBox = QMessageBox()
        msgBox.setWindowTitle(e.args[0])
        msgBox.setText(u'\n{}\n'.format(e.args[1]))
        msgBox.addButton(QMessageBox.Ok)
        msgBox.setWindowIcon(QIcon(r'./UI/icon1.png'))
        msgBox.exec_()
    finally:
        if need_close:
            window.close()

    # js = "setValue({},{})".format([1, 2, 3], [11, 53, 25])
    # main_exe.webView.page().runJavaScript(js)

    main_exe.WinChart.close()

def initWebmap(main_exe):
    webSettings=QWebEngineSettings.globalSettings()
    webSettings.setAttribute(QWebEngineSettings.JavascriptEnabled,True)
    webSettings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
    webSettings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
    main_exe.webViewmap=QWebEngineView(main_exe.widget_4)
    main_exe.webViewmap.setGeometry(QRect(1500, 1, 1005, 480))
    main_exe.webViewmap.setMinimumSize(QSize(1000, 480))
    main_exe.webViewmap.setStyleSheet("background-color:white;\n")
    main_exe.webViewmap.load(QUrl('file:///'+'src/mapbox.html'))

def SwitchMap(main_exe):
    pos_y=1
    pos_x_s=5
    pos_x_e = 1500
    if not main_exe.IsMap:
        runmapJS(main_exe)
        # chart飞走动画
        main_exe.animation = QPropertyAnimation(main_exe.Drawlabel, b'pos')
        main_exe.animation.setEasingCurve(QEasingCurve.InExpo)
        main_exe.animation.setDuration(300)
        main_exe.animation.setStartValue(QPoint(pos_x_s, pos_y))
        main_exe.animation.setEndValue(QPoint(pos_x_e, pos_y))
        main_exe.animation.start()
        # web飞来动画
        main_exe.animation1 = QPropertyAnimation(main_exe.webViewmap, b'pos')
        main_exe.animation1.setEasingCurve(QEasingCurve.InExpo)
        main_exe.animation1.setDuration(300)
        main_exe.animation1.setStartValue(QPoint(pos_x_e, pos_y))
        main_exe.animation1.setEndValue(QPoint(pos_x_s, pos_y))
        main_exe.animation1.start()

    else:
        # chart飞来动画
        main_exe.animation = QPropertyAnimation(main_exe.Drawlabel, b'pos')
        main_exe.animation.setEasingCurve(QEasingCurve.InExpo)
        main_exe.animation.setDuration(300)
        main_exe.animation.setStartValue(QPoint(pos_x_e, pos_y))
        main_exe.animation.setEndValue(QPoint(pos_x_s, pos_y))
        main_exe.animation.start()
        # web飞走动画
        main_exe.animation1 = QPropertyAnimation(main_exe.webViewmap, b'pos')
        main_exe.animation1.setEasingCurve(QEasingCurve.InExpo)
        main_exe.animation1.setDuration(300)
        main_exe.animation1.setStartValue(QPoint(pos_x_s, pos_y))
        main_exe.animation1.setEndValue(QPoint(pos_x_e, pos_y))
        main_exe.animation1.start()
    main_exe.IsMap = not main_exe.IsMap

def runmapJS(main_exe):
    map_ = main_exe.map
    layer = map_.layers[map_.selectedLayer]
    coorlist=[]

    if layer.type==Polygon:
        for geometry in layer.geometries:
            ptlist = []
            for i in range(len(geometry.data)):
                ptlist.append([geometry.data[i].X,geometry.data[i].Y])
            coorlist.append(ptlist)
    elif layer.type==MultiPolygon:
        for geometry in layer.geometries:
            for i in range(len(geometry.data)):
                ptlist = []
                for j in range(len(geometry.data[i].data)):
                    ptlist.append([geometry.data[i].data[j].X,geometry.data[i].data[j].Y])
                coorlist.append(ptlist)


    js = "changesource({})".format(coorlist)
    main_exe.webViewmap.page().runJavaScript(js)