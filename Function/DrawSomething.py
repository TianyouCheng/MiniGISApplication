'''
绘图函数
'''
from .Geometry import *
def draw(painter,object=None,list=[]):
    '''
    判断传入几何体的类型并绘制全部或list中的部分; 适用于所有自定义的几何类
    :param painter: 画笔
    :param object: 几何体对象
    :param list: 对于多线和多面，具体绘制哪些（可选）; 传索引不是传序号（即从0开始）
    :return: None
    '''
    if isinstance(object, PointD):
        painter.drawPoint(object.X,object.Y)
    elif isinstance(object, Polyline):
        for i in range(len(object.data)-1):
            painter.drawLine(object.data[i].X,object.data[i].Y,object.data[i+1].X,object.data[i+1].Y)
    elif isinstance(object, Polygon):
        painter.drawLine(object.data[len(object.data)-1].X, object.data[len(object.data)-1].Y, object.data[0].X, object.data[0].Y)
        for i in range(len(object.data)-1):
            painter.drawLine(object.data[i].X,object.data[i].Y,object.data[i+1].X,object.data[i+1].Y)
    elif isinstance(object, MultiPolyline):
        mylist=[i for i in range(len(object.data))]
        if len(list)!=0:mylist=list
        for i in mylist:
            for j in range(len(object.data[i].data) - 1):
                painter.drawLine(object.data[i].data[j].X, object.data[i].data[j].Y, object.data[i].data[j+1].X, object.data[i].data[j+1].Y)
    elif isinstance(object, MultiPolygon):
        mylist = [i for i in range(len(object.data))]
        if len(list) != 0: mylist = list
        for i in mylist:
            painter.drawLine(object.data[i].data[len(object.data) - 1].X, object.data[i].data[len(object.data) - 1].Y, object.data[i].data[0].X,
                             object.data[i].data[0].Y)
            for j in range(len(object.data[i].data)-1):
                painter.drawLine(object.data[i].data[j].X, object.data[i].data[j].Y, object.data[i].data[j + 1].X,
                                 object.data[i].data[j + 1].Y)