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
import copy


def RefreshCanvas(main_exe, mouseLoc: QPoint=None, use_base=False, stylelist=[]):

    '''
    绘制事件触发
    :param new_geo: 可能的新几何体（添加几何体模式）
    :param use_base: 若为True，则使用main_exe.basePixMap绘制底层，
                     否则重新绘制底层并覆盖原来的basePixMap
    '''

    map = main_exe.map
    pixmap = main_exe.Drawlabel.pixmap()
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    # 计算屏幕、鼠标位置的地理坐标范围
    width = pixmap.width()
    height = pixmap.height()
    if use_base:
        painter.drawPixmap(0, 0, main_exe.basePixmap)
    else:
        pixmap.fill(QColor('white'))
        RefreshBasePixmap(painter, map, (width, height))
        main_exe.basePixmap = QPixmap(pixmap)

    if map.selectedLayer != -1:
        DrawSelectedGeo(painter, map, (width, height))
        edit_layer = map.layers[map.selectedLayer]
        edit_geom = edit_layer.edited_geometry
        # “添加几何体”模式，绘制待添加的几何体
        if main_exe.tool == MapTool.AddGeometry:
            for g in edit_layer.geometries:
                g_screen = map.GeoToScreen(g, (width, height))
                DS.draw(painter, g_screen)#先把不再编辑的画出来
            if edit_layer.type == PointD:
                pass
            elif edit_layer.type == Polyline:
                cur_line = Polyline(edit_geom)
                DS.draw(painter, cur_line)
                #橡皮筋
                tail = Polyline([PointD(mouseLoc.x(), mouseLoc.y()), edit_geom[-1]])
                DS.draw(painter, tail)
            elif edit_layer.type == Polygon:
                cur_mouse = PointD(mouseLoc.x(), mouseLoc.y())
                if len(edit_geom) == 1:
                    cur_pg = Polygon(edit_geom[0] + [cur_mouse])
                else:
                    holes = edit_geom[1:]
                    cur_holes = holes[:-1] + [holes[-1] + [cur_mouse]]
                    cur_pg = Polygon(edit_geom[0], cur_holes)
                DS.draw(painter, cur_pg)
        # “编辑几何体”模式，绘制正在编辑的几何体
        elif main_exe.tool == MapTool.EditGeometry:
            pass
        # “选择”模式，绘制选择框
        elif main_exe.tool == MapTool.Select and main_exe.mouseLeftPress:
            pen = QPen(QColor('black'), 1, Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.setBrush(QBrush(QColor(0, 162, 232, 64)))
            rect = QRect(mouseLoc, main_exe.mousePressLoc)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
            painter.drawRect(rect)
    painter.end()
    main_exe.Drawlabel.update()


def RefreshBasePixmap(painter: QPainter, map_: Map, screen_size):
    '''重新绘制地理底图'''
    # linestyle传入线型列表
    screen_minP = map_.ScreenToGeo(PointD(0, screen_size[1]), screen_size)
    screen_maxP = map_.ScreenToGeo(PointD(screen_size[0], 0), screen_size)
    screen_geobox = RectangleD(screen_minP.X, screen_minP.Y, screen_maxP.X, screen_maxP.Y)

    # 若地图工程在显示范围内，则绘制
    if map_.box.IsIntersectBox(screen_geobox):
        # 图层倒序绘制
        for i in range(len(map_.layers) - 1, -1, -1):
            layer = map_.layers[i]
            # 判断该图层是否显示、且在屏幕范围内
            if not layer.visible or len(layer.geometries) == 0 or \
                    not layer.box.IsIntersectBox(screen_geobox):
                continue
            # 设置绘制样式，TODO 渲染样式在这里读取，修改
            painter.setPen(QPen(QColor('black'), 1.5))
            painter.setBrush(QBrush(QColor('black')))
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
                # 如果要素已有样式表，按照表渲染
                # TODO: 以后再做全局渲染
                if geometry.StyleList:
                    # 设置轮廓颜色、轮廓宽度
                    tmp_pen=QPen(QColor(geometry.StyleList[0]), geometry.StyleList[2])
                    # 设置线型样式
                    tmp_pen.setStyle(geometry.StyleList[1])
                    painter.setPen(tmp_pen)
                    # 设置填充颜色
                    painter.setBrush(QBrush(QColor(geometry.StyleList[3])))
                DS.draw(painter, screen_geo, list=draw_index)

                if geometry.StyleList:
                    # 注记
                    if geometry.StyleList[5]:
                        # 注记内容
                        labeltxt = str(layer.table.loc[geometry.ID, geometry.StyleList[6]])
                        # 设置画笔
                        font = painter.font()
                        fontsize = geometry.StyleList[9]
                        font.setPixelSize(fontsize)
                        font.setFamily("Microsoft YaHei")
                        painter.setFont(font)
                        painter.setPen(QPen(QColor(geometry.StyleList[10])))
                        # 坐标转换
                        textgeo = map_.GeoToScreen(geometry.MarkPos(), screen_size)
                        # 附加水平垂直偏移
                        painter.drawText(textgeo.X + geometry.StyleList[7], textgeo.Y + geometry.StyleList[8], labeltxt)


def DrawSelectedGeo(painter: QPainter, map_: Map, screen_size):
    '''绘制被选择的多边形'''
    layer = map_.layers[map_.selectedLayer]
    if not layer.visible:
        return
    origin_pen = painter.pen()
    origin_brush = painter.brush()
    screen_minP = map_.ScreenToGeo(PointD(0, screen_size[1]), screen_size)
    screen_maxP = map_.ScreenToGeo(PointD(screen_size[0], 0), screen_size)
    screen_geobox = RectangleD(screen_minP.X, screen_minP.Y, screen_maxP.X, screen_maxP.Y)
    # 设置被选择时的样式
    painter.setPen(QPen(QColor('cyan'), 2.5))
    painter.setBrush(QBrush(QColor('cyan'), Qt.BrushStyle.Dense7Pattern))
    selected = set(layer.selectedItems)
    for item in layer.geometries:
        # 判断几何体本身是否与画面相交太费时间，判断外包矩形相交就行了
        if item.ID in selected and item.box.IsIntersectBox(screen_geobox):
            screen_geo = map_.GeoToScreen(item, screen_size)
            DS.draw(painter, screen_geo)
    painter.setPen(origin_pen)
    painter.setBrush(origin_brush)


def LabelMousePress(main_exe, event: QMouseEvent):
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
            RefreshCanvas(main_exe, mouse_loc)
        # 在“缩小”模式下按下左键
        elif main_exe.tool == MapTool.ZoomOut:
            map_.ZoomAtPoint((width, height), PointD(mouse_loc.x(), mouse_loc.y()),
                             map_.scale * main_exe.zoomRatio)
            RefreshCanvas(main_exe, mouse_loc)
        elif main_exe.tool == MapTool.EditGeometry:
            pass
        elif main_exe.tool == MapTool.AddGeometry:
            edit_layer = main_exe.CurEditLayer
            edit_geom = edit_layer.edited_geometry
            need_save = main_exe.NeedSave
            if edit_layer.type == PointD:
                edit_layer.AddGeometry(map_.ScreenToGeo(PointD(mouse_loc.x(), mouse_loc.y()),(width, height)))
                RefreshCanvas(main_exe, mouse_loc, False, main_exe.StyleList)
            elif edit_layer.type == Polyline:
                edit_geom.append(PointD(mouse_loc.x(), mouse_loc.y()))
                RefreshCanvas(main_exe, mouse_loc, False, main_exe.StyleList)
            elif edit_layer.type == Polygon:
                if len(edit_geom) == 0:
                    edit_geom.append(list())
                edit_geom[-1].append(PointD(mouse_loc.x(), mouse_loc.y()))
                RefreshCanvas(main_exe, mouse_loc, False, main_exe.StyleList)
            elif edit_layer.type == MultiPolyline:
                pass
            elif edit_layer.type == MultiPolygon:
                pass
    else:
        if main_exe.tool == MapTool.AddGeometry:
            edit_layer = main_exe.CurEditLayer
            edit_geom = edit_layer.edited_geometry
            need_save = main_exe.NeedSave
            if edit_layer.type == Polygon:
                edit_geom.append(list())

        elif main_exe.tool == MapTool.EditGeometry:
            pass


def LabelMouseDoubleClick(main_exe, event : QMouseEvent):
    map_ = main_exe.map
    edit_layer = main_exe.map.selectedLayer
    edit_geom = edit_layer.edited_geometry
    if edit_layer.type == Polyline:
        pass
    elif edit_layer.type == Polygon:
        pass
    elif edit_layer.type == MultiPolyline:
        pass
    elif edit_layer.type == MultiPolygon:
        pass
def LabelMouseMove(main_exe, event : QMouseEvent):
    '''处理鼠标移动，且鼠标位置在画布内的事件'''
    map_ = main_exe.map
    edit_layer = main_exe.map.selectedLayer
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
            RefreshCanvas(main_exe, mouse_loc)
        # 鼠标框选移动
        elif main_exe.tool == MapTool.Select:
            RefreshCanvas(main_exe, mouse_loc, use_base=True)
        elif main_exe.tool == MapTool.AddGeometry:
            if edit_layer.type == PointD:
                pass
            elif edit_layer.type == Polyline:
                pass
        elif main_exe.tool == MapTool.EditGeometry:
            pass

def LabelMouseRelease(main_exe, event: QMouseEvent):
    '''处理与画布有关的、鼠标松开的事件'''
    from .Op_TableView import TableUpdate
    edit_layer = main_exe.map.selectedLayer
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
            p_select = True
        # 框选模式
        else:
            rect_screen = RectangleD(min(main_exe.mousePressLoc.x(), mouse_loc.x()),
                                     min(main_exe.mousePressLoc.y(), mouse_loc.y()),
                                     max(main_exe.mousePressLoc.x(), mouse_loc.x()),
                                     max(main_exe.mousePressLoc.y(), mouse_loc.y()))
            query = map_.ScreenToGeo(rect_screen, (width, height))
            p_select = False
        buffer = map_.ScreenDistToGeo(main_exe.bufferRadius)
        result = map_.layers[map_.selectedLayer].Query(query, buffer)
        result = ConcatSelection(map_.layers[map_.selectedLayer].selectedItems, result,
                                 event.modifiers(), p_select)
        map_.layers[map_.selectedLayer].selectedItems = result
        TableUpdate(main_exe)
        RefreshCanvas(main_exe, mouse_loc, use_base=True)


def LabelMouseWheel(main_exe, event: QWheelEvent):
    '''处理画布内的鼠标滚轮事件，可用滚轮放大缩小'''
    map_ = main_exe.map
    width = main_exe.Drawlabel.pixmap().width()
    height = main_exe.Drawlabel.pixmap().height()
    mouse_loc = main_exe.ConvertCor(event)
    # 注：鼠标滚1格一般是120度
    angle = event.angleDelta().y()
    # angle > 0表示鼠标滚轮向前滚，应该放大
    if angle > 0:
        map_.ZoomAtPoint((width, height), PointD(mouse_loc.x(), mouse_loc.y()),
                         map_.scale / (1 + (main_exe.zoomRatio - 1) * angle / 120))
    else:
        map_.ZoomAtPoint((width, height), PointD(mouse_loc.x(), mouse_loc.y()),
                         map_.scale * (1 + (main_exe.zoomRatio - 1) * -angle / 120))
    RefreshCanvas(main_exe, mouse_loc)


def ConcatSelection(old_list, new_list, modifiers: Qt.KeyboardModifiers, p_select):
    '''
    根据键鼠输入状态，合并两个选择集合（重新选择、并集、差集）
    :param modifiers: 功能按键（ctrl, alt, shift）的状态
    :param p_select: 是否为点选
    :return: 合并后的集合
    '''
    result = set(old_list)
    if modifiers == Qt.KeyboardModifier.ControlModifier:
        # 点选ctrl，逻辑是异或，即原来未选择的选上，原来已经选择的去除选择
        if p_select:
            result = result.symmetric_difference(new_list)
        # 框选ctrl，效果与shift相同
        else:
            result = result.union(new_list)
    # 按下shift，输出并集
    elif modifiers == Qt.KeyboardModifier.ShiftModifier:
        result = result.union(new_list)
    # 按下alt，输出差集
    elif modifiers == Qt.KeyboardModifier.AltModifier:
        result = result.difference(new_list)
    # 什么都没按，则用新选择结果代替旧结果
    else:
        return new_list
    return list(result)
