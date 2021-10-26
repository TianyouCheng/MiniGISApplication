'''
图表相关
'''
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize,QUrl,QPropertyAnimation,QPoint,QEasingCurve,QCoreApplication
from PyQt5.QtWebEngineWidgets import QWebEngineSettings,QWebEngineView
def initChart(main_exe):
    if not main_exe.IsChart:
        webSettings=QWebEngineSettings.globalSettings()
        webSettings.setAttribute(QWebEngineSettings.JavascriptEnabled,True)
        webSettings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        webSettings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)

        main_exe.webView=QWebEngineView()
        main_exe.webView.load(QUrl('file:///'+'src/render.html'))

        main_exe.webView.setMinimumSize(QSize(1000, 490))
        main_exe.verticalLayout_2.removeWidget(main_exe.Drawlabel)
        main_exe.verticalLayout_2.removeWidget(main_exe.tableWidget)
        main_exe.verticalLayout_2.addWidget(main_exe.webView)
        main_exe.verticalLayout_2.addWidget(main_exe.tableWidget)

    else:
        main_exe.verticalLayout_2.removeWidget(main_exe.webView)
        main_exe.verticalLayout_2.removeWidget(main_exe.tableWidget)
        main_exe.verticalLayout_2.addWidget(main_exe.Drawlabel)
        main_exe.verticalLayout_2.addWidget(main_exe.tableWidget)

    js="setValue({},{})".format([1,2,3],[11,55,22])
    main_exe.webView.page().runJavaScript(js)
    main_exe.IsChart=not main_exe.IsChart
    # animation=QPropertyAnimation(main_exe.Drawlabel,b'pos')
    # animation.setEasingCurve(QEasingCurve.InExpo)
    # animation.setDuration(300)
    # animation.setStartValue(QPoint(1, 1))
    # animation.setEndValue(QPoint(1500, 0))
    # animation.start()
    # animation1 = QPropertyAnimation(main_exe.webView, b'pos')
    # animation1.setEasingCurve(QEasingCurve.InExpo)
    # animation1.setDuration(300)
    # animation1.setStartValue(QPoint(1500, 0))
    # animation1.setEndValue(QPoint(1, 1))
    # animation1.start()


