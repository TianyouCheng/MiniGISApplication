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

        # 创建画布
        canvas = QtGui.QPixmap('UI/whitebg.png')
        self.label.setPixmap(canvas)

        # 绘图函数
        self.draw_something()

    # region 功能函数
    # 坐标转换，将事件E的坐标转换到画布坐标上
    def ConvertCor(self,e):
        point = e.globalPos()
        point = self.label.mapFromGlobal(point)
        return point

    # 绘图，目前加入了点线面类的判断
    def draw_something(self,object='null'):
        # 判断类型
        # print(isinstance(myDlg, Main_exe))
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(40)
        pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)
        painter.drawPoint(30, 30)
        painter.end()

    def mouseMoveEvent(self, e):
        painter = QtGui.QPainter(self.label.pixmap())
        # painter.setPen(QtGui.QColor('white'))
        point=self.ConvertCor(e)
        painter.drawPoint(point.x(), point.y())
        painter.end()
        self.update()

    # endregion

    # region 信号与槽函数

    # endregion


# 作为主窗体运行
if __name__=='__main__':

    # test region 使用方法/功能测试
    # 初始化
    pt1=PointD(0,5,8)#分别为x，y，ID
    pt2=PointD(3,3)#分别为x，y

    # 找到最大/最小X,Y坐标
    pt = pt1.FindMaxXY([pt1,pt2])
    pt = pt1.FindMinXY([pt1, pt2])
    print(pt)

    # 求与pt1的距离
    print(pt.GetDistance(pt1))

    # 判断与pt1的距离是否小于等于2
    print(pt.IsPointOn(pt1,2))

    # 判断是否在所选矩形内
    Rec=RectangleD(2,2,5,5)
    print(pt.IsWithinBox(Rec))

    # 移动点
    pt.Move(5,5)
    print(pt)

    # 当前点的最小外接矩阵
    pt.RenewBox()
    print(pt._box)



    # endregion 可以把这段删掉


    myapp=QApplication(sys.argv)
    myDlg=Main_exe()
    # myDlg.show()
    sys.exit(myapp.exec_())
