import os,sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#region 引入窗体及函数
from UI import *
from Function import *
#endregion

# 主窗体操作
class Main_exe(QMainWindow,Ui_MainWindow):
    def __init__(self):
        # 创建窗体
        super(Main_exe,self).__init__()
        self.setupUi(self)

        # 属性
        self.EditStatus=False

        # 绑定信号与槽函数
        self.slot_connect()

        # 创建画布
        # canvas.size()这个取出来的size不对，是（100，500）,实际是（879，500）
        canvas=QtGui.QPixmap(QtCore.QSize(879, 500))
        canvas.fill(QColor('white'))
        self.label.setPixmap(canvas)

        # 绘图函数
        self.draw_something()

    # region 功能函数
    # 绑定信号与槽函数
    def slot_connect(self):
        self.tsButtonEdit.clicked.connect(self.bt_edit_clicked)

    # 坐标转换，将事件E的坐标转换到画布坐标上
    def ConvertCor(self,e):
        point = e.globalPos()
        point = self.label.mapFromGlobal(point)
        return point

    # 绘图
    def draw_something(self,object='null'):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)
        '''
       def draw(painter,object=None,list=[]):
        判断传入几何体的类型并绘制全部或list中的部分; 适用于所有自定义的几何类
       :param painter: 画笔
       :param object: 几何体对象
       :param list: 对于多线和多面，具体绘制哪些（可选）; 传索引不是传序号（即从0开始）
       :return: None
       '''
        draw(painter,PointD(50,50))
        painter.end()

    def mouseMoveEvent(self, e):
        painter = QtGui.QPainter(self.label.pixmap())
        # painter.setPen(QtGui.QColor('white'))
        point=self.ConvertCor(e)
        if self.EditStatus:
            painter.drawPoint(point.x(), point.y())
            painter.end()
            self.update()

    # endregion

    # region 信号与槽函数
    def bt_edit_clicked(self):
        self.EditStatus=not(self.EditStatus)
        if self.EditStatus:self.tsButtonEdit.setText("正在编辑")
        elif not self.EditStatus:self.tsButtonEdit.setText("编辑模式")
    # endregion


# 作为主窗体运行
if __name__=='__main__':
    myapp=QApplication(sys.argv)
    myDlg=Main_exe()
    myDlg.show()
    sys.exit(myapp.exec_())
