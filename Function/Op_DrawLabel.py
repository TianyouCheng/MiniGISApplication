'''
地图显示界面的操作函数
'''

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from . import DrawSomething as DS
from .Geometry import *
from .Layer import Layer
from .Map import Map
from .MapTool import MapTool
from Main import Main_exe


def Refresh(main_exe: Main_exe, mouseLoc: QPoint, new_geo=None, use_base=False):
    '''
    绘制事件触发
    :param new_geo: 可能的新几何体（添加几何体模式）
    :param use_base: 若为True，则使用main_exe.basePixMap绘制底层，
                     否则重新绘制底层并覆盖原来的basePixMap
    '''
    map = main_exe.map
    pixmap = main_exe.Drawlabel.pixmap()
    painter = QPainter(pixmap)
    # 计算屏幕、鼠标位置的地理坐标范围
    width = pixmap.width()
    height = pixmap.height()
    mouse_screenloc = PointD(mouseLoc.x(), mouseLoc.y())
    mouse_geoloc = map.ScreenToGeo(mouse_screenloc, (width, height))
    if use_base:
        painter.drawPixmap(0, 0, main_exe.basePixmap)
    else:
        pixmap.fill(QColor('white'))
        RefreshBasePixmap(painter, map, (width, height))
        main_exe.basePixmap = QPixmap(pixmap)

    if map.selectedLayer != -1:
        DrawSelectedGeo(painter, map, (width, height))
        # “添加几何体”模式，绘制待添加的几何体
        if main_exe.tool == MapTool.AddGeometry:
            pass
        # “编辑几何体”模式，绘制正在编辑的几何体
        elif main_exe.tool == MapTool.EditGeometry:
            pass
        # “选择”模式，绘制选择框
        elif main_exe.tool == MapTool.Select and main_exe.mouseLeftPress:
            pen = QPen(QColor('black'), 1, Qt.PenStyle.DashLine)
            painter.setPen(pen)
            rect = QRect(mouseLoc, main_exe.mousePressLoc)
            painter.fillRect(rect, QColor(0, 162, 232, 64))
            painter.drawRect(rect)
    painter.end()
    main_exe.Drawlabel.update()


def RefreshBasePixmap(painter: QPainter, map_: Map, screen_size):
    '''重新绘制地理底图'''
    screen_minP = map_.ScreenToGeo(PointD(0, screen_size[1]), screen_size)
    screen_maxP = map_.ScreenToGeo(PointD(screen_size[0], 0), screen_size)
    screen_geobox = RectangleD(screen_minP.X, screen_minP.Y, screen_maxP.X, screen_maxP.Y)
    # 若地图工程在显示范围内，则绘制
    if map_.box.IsIntersectBox(screen_geobox):
        # 图层倒序绘制
        for i in range(len(map_.layers) - 1, -1, -1):
            layer = map_.layers[i]
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
                # 判断几何体本身是否与画面相交太费时间，判断外包矩形相交就行了
                if not geometry.box.IsIntersectBox(screen_geobox):
                    continue
                # 坐标转换
                screen_geo = map_.GeoToScreen(geometry, screen_size)
                draw_index = []
                if isinstance(geometry, MultiPolyline) or \
                        isinstance(geometry, MultiPolygon):
                    draw_index = [index for index, part in enumerate(geometry.data)
                                  if part.box.IsIntersectBox(screen_geobox)]
                DS.draw(painter, screen_geo, list=draw_index)


def DrawSelectedGeo(painter: QPainter, map_: Map, screen_size):
    '''绘制被选择的多边形'''
    layer = map_.layers[map_.selectedLayer]
    origin_pen = painter.pen()
    screen_minP = map_.ScreenToGeo(PointD(0, screen_size[1]), screen_size)
    screen_maxP = map_.ScreenToGeo(PointD(screen_size[0], 0), screen_size)
    screen_geobox = RectangleD(screen_minP.X, screen_minP.Y, screen_maxP.X, screen_maxP.Y)
    # 设置被选择时的样式
    new_pen = QPen(QColor('cyan'), 2)
    painter.setPen(new_pen)
    selected = set(layer.selectedItems)
    for item in layer.geometries:
        # 判断几何体本身是否与画面相交太费时间，判断外包矩形相交就行了
        if item.ID in selected and item.box.IsIntersectBox(screen_geobox):
            screen_geo = map_.GeoToScreen(item, screen_size)
            DS.draw(painter, screen_geo)
    painter.setPen(origin_pen)


def LabelMousePress(main_exe: Main_exe, event: QMouseEvent):
    '''处理鼠标按下，且鼠标位置在画布内的事件'''
    map_ = main_exe.map
    width = main_exe.Drawlabel.pixmap().width()
    height = main_exe.Drawlabel.pixmap().height()
    mouse_loc = main_exe.ConvertCor(event)
    if event.button() == Qt.MouseButton.LeftButton:
        # 在“放大”模式下按下左键
        if main_exe.tool == MapTool.ZoomIn:
            map_.ZoomAtPoint((width, height), PointD(mouse_loc.x(), mouse_loc.y()),
                             map_.scale / main_exe.zoomRatio)
            Refresh(main_exe, mouse_loc)
        # 在“缩小”模式下按下左键
        elif main_exe.tool == MapTool.ZoomOut:
            map_.ZoomAtPoint((width, height), PointD(mouse_loc.x(), mouse_loc.y()),
                             map_.scale * main_exe.zoomRatio)
            Refresh(main_exe, mouse_loc)


def LabelMouseMove(main_exe: Main_exe, event: QMouseEvent):
    '''处理鼠标移动，且鼠标位置在画布内的事件'''
    map_ = main_exe.map
    width = main_exe.Drawlabel.pixmap().width()
    height = main_exe.Drawlabel.pixmap().height()
    mouse_loc = main_exe.ConvertCor(event)
    if main_exe.mouseLeftPress:
        # 在“漫游”模式下按住左键拖动
        if main_exe.tool == MapTool.Pan:
            now_geoloc = map_.ScreenToGeo(PointD(mouse_loc.x(), mouse_loc.y()), (width, height))
            old_geoloc = map_.ScreenToGeo(PointD(main_exe.mouseLastLoc.x(),
                                                 main_exe.mouseLastLoc.y()), (width, height))
            map_.offsetX += old_geoloc.X - now_geoloc.X
            map_.offsetY += old_geoloc.Y - now_geoloc.Y
            Refresh(main_exe, mouse_loc)
        # 鼠标框选移动
        elif main_exe.tool == MapTool.Select:
            Refresh(main_exe, mouse_loc, use_base=True)


def LabelMouseRelease(main_exe: Main_exe, event: QMouseEvent):
    '''处理与画布有关的、鼠标松开的事件'''
    map_ = main_exe.map
    width = main_exe.Drawlabel.pixmap().width()
    height = main_exe.Drawlabel.pixmap().height()
    mouse_loc = main_exe.ConvertCor(event)
    # 鼠标选择完成
    if main_exe.tool == MapTool.Select and map_.selectedLayer != -1:
        # 点选模式
        if (main_exe.mousePressLoc.x() - mouse_loc.x()) ** 2 + \
                (main_exe.mousePressLoc.y() - mouse_loc.y()) ** 2 < \
                main_exe.bufferRadius ** 2:
            center_p = (QPointF(main_exe.mousePressLoc) + QPointF(mouse_loc)) / 2
            query = map_.ScreenToGeo(PointD(center_p.x(), center_p.y()), (width, height))
        # 框选模式
        else:
            rect_screen = RectangleD(min(main_exe.mousePressLoc.x(), mouse_loc.x()),
                                     min(main_exe.mousePressLoc.y(), mouse_loc.y()),
                                     max(main_exe.mousePressLoc.x(), mouse_loc.x()),
                                     max(main_exe.mousePressLoc.y(), mouse_loc.y()))
            query = map_.ScreenToGeo(rect_screen, (width, height))
        buffer = map_.ScreenDistToGeo(main_exe.bufferRadius)
        result = map_.layers[map_.selectedLayer].Query(query, buffer)
        map_.layers[map_.selectedLayer].selectedItems = result
        Refresh(main_exe, mouse_loc, use_base=True)
