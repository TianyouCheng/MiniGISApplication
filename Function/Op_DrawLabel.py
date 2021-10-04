'''
地图显示界面的操作函数
'''

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPaintEvent, QPen, QColor, QMouseEvent
from PyQt5.QtCore import QPoint, QSize
from . import DrawSomething as DS
from .Geometry import *
from .Layer import Layer
from .Map import Map
from .MapTool import MapTool
from Main import Main_exe


def Refresh(main_exe: Main_exe, mouseLoc: QPoint, new_geo=None):
    '''
    绘制事件触发
    :param new_geo: 可能的新几何体（添加几何体模式）
    '''
    label = main_exe.Drawlabel
    map = main_exe.map
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

    if map.selectedLayer != -1:
        # “添加几何体”模式，绘制待添加的几何体
        if main_exe.tool == MapTool.AddGeometry:
            pass
        # “编辑几何体”模式，绘制正在编辑的几何体
        elif main_exe.tool == MapTool.EditGeometry:
            pass
        # “选择”模式，绘制被选择的几何体
        elif main_exe.tool == MapTool.Select:
            DrawSelectedGeo(painter, map)
    painter.end()
    label.update()


def DrawSelectedGeo(painter: QPainter, map: Map):
    '''绘制被选择的多边形'''
    layer = map.layers[map.selectedLayer]
    origin_pen = painter.pen()
    # 设置被选择时的样式
    new_pen = QPen(brush=QColor('cyan'), width=2)
    painter.setPen(new_pen)
    selected = set(layer.selectedItems)
    for item in layer.geometries:
        if item.ID in selected:
            screen_geo = map.GeoToScreen(item, (painter.device().width(),
                                                painter.device().height()))
            DS.draw(painter, screen_geo)
    painter.setPen(origin_pen)


def LabelMousePress(main_exe: Main_exe, event: QMouseEvent):
    '''处理鼠标按下，且鼠标位置在画布内的事件'''
    event.button()
