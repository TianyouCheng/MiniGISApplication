'''
绘图函数
'''
from PyQt5.QtGui import QPainter, QPainterPath, QPolygonF
from PyQt5.QtCore import QPointF, Qt
from .Geometry import *

def draw(painter: QPainter,object=None,list=[]):
    '''
    判断传入几何体的类型并绘制全部或list中的部分; 适用于所有自定义的几何类
    :param painter: 画笔
    :param object: 几何体对象
    :param list: 对于多线和多面，具体绘制哪些（可选）; 传索引不是传序号（即从0开始）
    :return: None
    '''
    if isinstance(object, PointD):
        painter.drawPoint(QPointF(object.X, object.Y))
        painter.drawEllipse(QPointF(object.X, object.Y), 2.0, 2.0)
    elif isinstance(object, Polyline):
        for i in range(len(object.data)-1):
            painter.drawLine(QPointF(object.data[i].X,object.data[i].Y),
                             QPointF(object.data[i+1].X,object.data[i+1].Y))
    elif isinstance(object, Polygon):
        DrawPolygon(painter, object)
    elif isinstance(object, MultiPolyline):
        mylist=[i for i in range(len(object.data))]
        if len(list)!=0:mylist=list
        for i in mylist:
            for j in range(len(object.data[i].data) - 1):
                painter.drawLine(QPointF(object.data[i].data[j].X, object.data[i].data[j].Y),
                                 QPointF(object.data[i].data[j+1].X, object.data[i].data[j+1].Y))
    elif isinstance(object, MultiPolygon):
        mylist = [i for i in range(len(object.data))]
        if len(list) != 0: mylist = list
        for i in mylist:
            DrawPolygon(painter, object.data[i])


def DrawPolygon(painter: QPainter, polygon: Polygon):
    '''绘制多边形，包括外包和洞'''
    polygon_holes = []
    if polygon.holes is not None:
        for hole in polygon.holes:
            qpg = QPolygonF([QPointF(point.X, point.Y) for point in hole.data])
            polygon_holes.append(qpg)
    qpg_out = QPolygonF([QPointF(point.X, point.Y) for point in polygon.data])
    # 先绘制多边形内部填充。
    # QT有bug是不能很好绘制带洞的多边形，因此绘制内部和边界需要两个不同的函数
    qpg = QPolygonF(qpg_out)
    for hole in polygon_holes:
        qpg = qpg.subtracted(hole)
    path = QPainterPath()
    path.addPolygon(qpg)
    painter.fillPath(path, painter.brush())
    path.clear()
    # 绘制多边形边界
    path.addPolygon(qpg_out)
    path.closeSubpath()
    for hole in polygon_holes:
        path.addPolygon(hole)
        path.closeSubpath()
    painter.brush().setStyle(Qt.BrushStyle.NoBrush)
    painter.drawPath(path)
    painter.brush().setStyle(Qt.BrushStyle.SolidPattern)
