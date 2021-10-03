'''
地图显示界面的操作函数
'''

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPaintEvent, QPen, QColor
from PyQt5.QtCore import QPoint, QSize
from . import DrawSomething as DS
from .Geometry import *
from .Layer import Layer
from .Map import Map


def Refresh(label: QLabel, map: Map, mouseLoc: QPoint):
    '''绘制事件触发'''
    pixmap = label.pixmap()
    pixmap.fill(QColor('white'))
    painter = QPainter(label.pixmap())
    # 计算屏幕、鼠标位置的地理坐标范围
    screen_minP = map.ScreenToGeo(PointD(0, label.height()), (label.width(), label.height()))
    screen_maxP = map.ScreenToGeo(PointD(label.width(), 0), (label.width(), label.height()))
    screen_geobox = RectangleD(screen_minP.X, screen_minP.Y, screen_maxP.X, screen_maxP.Y)
    mouse_screenloc = PointD(mouseLoc.x(), mouseLoc.y())
    mouse_geoloc = map.ScreenToGeo(mouse_screenloc, (label.width(), label.height()))
    # 若地图工程在显示范围内，则绘制
    if map.box.IsIntersectBox(screen_geobox):
        # 图层倒序绘制
        for i in range(len(map.layers) - 1, -1, -1):
            layer = map.layers[i]
            # 判断该图层是否在屏幕范围内
            if len(layer.geometries) == 0 or \
                    not layer.box.IsIntersectBox(screen_geobox):
                continue
            # 设置绘制样式，TODO 渲染样式在这里读取，修改
            pen = QPen()
            pen.setWidth(2)
            pen.setColor(QColor('red'))
            painter.setPen(pen)
            '''
           def draw(painter,object=None,list=[]):
            判断传入几何体的类型并绘制全部或list中的部分; 适用于所有自定义的几何类
           :param painter: 画笔
           :param object: 几何体对象
           :param list: 对于多线和多面，具体绘制哪些（可选）; 传索引不是传序号（即从0开始）
           :return: None
           '''
            # 绘制每个几何体
            for geometry in layer.geometries:
                if not geometry.box.IsIntersectBox(screen_geobox):
                    continue
                # 坐标转换
                screen_geo = map.GeoToScreen(geometry, (label.width(), label.height()))
                draw_index = []
                if isinstance(geometry, MultiPolyline) or \
                        isinstance(geometry, MultiPolygon):
                    draw_index = [index for index, part in enumerate(geometry)
                                  if part.box.IsIntersectBox(screen_geobox)]
                DS.draw(painter, screen_geo, list=draw_index)
    painter.end()
    label.update()
