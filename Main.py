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
        # canvas = QtGui.QPixmap('UI/whitebg.png')
        # self.label.setPixmap(canvas)
        canvas=QtGui.QPixmap(self.label.size())
        canvas.fill(QColor('white'))
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
    """点"""
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

    """线"""
    # 初始化，以点的列表形式
    L1=Polyline([pt,pt1,pt2])
    print(L1)

    # 求点到直线距离
    L2 = Polyline([PointD(3, 3), PointD(5, 5), PointD(5, 8)])
    print(L2.GetDistance(PointD(3,5)))

    # 判断该直线与点的距离是否在给定buffer内
    print(L2.IsPointOn(PointD(3,5),1))

    # 判断直线上的各点是否在给定矩形内
    """注意：该算法不是判断线段与给定box相交"""
    Rec = RectangleD(3,3.5,4.5,5)
    print(L2.IsWithinBox(Rec))

    # 移动线
    L2.Move(1,1)
    print(L2)

    """面"""
    '''方法都一样，就不再测试（若有Bug再找我= =）'''
    Po1=Polygon([pt,pt1,pt2])
    print(Po1)

    """多线"""
    MulL1=MultiPolyline([L1,L2])
    print(MulL1)

    """多面"""
    Polygon1=Polygon([pt,pt2,pt2])
    Polygon2=Polygon([PointD(10,10),PointD(30,10),PointD(30,30)])
    PPolygon=MultiPolygon([Polygon1,Polygon2])
    print(PPolygon)
    # endregion 可以把这段删掉


    myapp=QApplication(sys.argv)
    myDlg=Main_exe()
    myDlg.show()
    sys.exit(myapp.exec_())
