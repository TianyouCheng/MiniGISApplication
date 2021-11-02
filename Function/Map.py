'''
地图类别，可以认为是多个图层组成的容器，相当于一个工程
一个工程里面有统一的显示范围、比例尺、……
'''

from .Layer import *


class Map(object):
    def __init__(self):
        self.layers = []            # 图层集合。下标0为最顶层
        self.offsetX = 0            # 显示区域中心的X地理坐标
        self.offsetY = 0            # 显示区域中心的Y地理坐标
        self.scale = 1              # 地图缩小系数（即比例尺为1:scale），scale越大几何体越小
        self.box = RectangleD()     # 全地图的外包矩形
        self.selectedLayer = -1     # 选定图层的下标，默认为-1，即未选择图层
        

    def RefreshBox(self):
        '''更新外包矩形框'''
        if len(self.layers) > 0:
            first_box = self.layers[0].box
            self.box.MinX = first_box.MinX
            self.box.MinY = first_box.MinY
            self.box.MaxX = first_box.MaxX
            self.box.MaxY = first_box.MaxY
            # 遍历所有几何体找到最终的min, max值
            for layer in self.layers:
                if layer.box.MinX < self.box.MinX:
                    self.box.MinX = layer.box.MinX
                if layer.box.MinY < self.box.MinY:
                    self.box.MinY = layer.box.MinY
                if layer.box.MaxX > self.box.MaxX:
                    self.box.MaxX = layer.box.MaxX
                if layer.box.MaxY > self.box.MaxY:
                    self.box.MaxY = layer.box.MaxY

    def GeoToScreen(self, geometry, screenSize):
        '''
        将地理坐标转化为屏幕坐标
        :param geometry: 地理坐标的几何体（Geometry的子类、或RectangleD）
        :param screenSize: 屏幕大小[width, height]列表
        :return: 转化为屏幕坐标的几何体（Geometry的子类、或RectangleD）
        '''
        if isinstance(geometry, PointD):
            return PointD(x=(geometry.X - self.offsetX) / self.scale + screenSize[0] / 2,
                          y=(self.offsetY - geometry.Y) / self.scale + screenSize[1] / 2,
                          id=geometry.ID)
        elif isinstance(geometry, Polyline):
            data = [self.GeoToScreen(geo, screenSize) for geo in geometry.data]
            return Polyline(data, id=geometry.ID)
        elif isinstance(geometry, Polygon):
            data = [self.GeoToScreen(geo, screenSize) for geo in geometry.data]
            holes = None if geometry.holes is None else \
                [self.GeoToScreen(geo, screenSize) for geo in geometry.holes]
            return Polygon(data, holes=holes, id=geometry.ID)
        elif isinstance(geometry, MultiPolyline):
            data = [self.GeoToScreen(geo, screenSize) for geo in geometry.data]
            return MultiPolyline(data, id=geometry.ID)
        elif isinstance(geometry, MultiPolygon):
            data = [self.GeoToScreen(geo, screenSize) for geo in geometry.data]
            return MultiPolygon(data, id=geometry.ID)
        elif isinstance(geometry, RectangleD):
            p_min = self.GeoToScreen(PointD(geometry.MinX, geometry.MaxY), screenSize)
            p_max = self.GeoToScreen(PointD(geometry.MaxX, geometry.MinY), screenSize)
            return RectangleD(minx=p_min.X, miny=p_min.Y, maxx=p_max.X, maxy=p_max.Y)
        else:
            raise ValueError('geometry not supported.')

    def ScreenToGeo(self, geometry, screenSize):
        '''
        将屏幕坐标转化为地理坐标
        :param geometry: 屏幕坐标的几何体（Geometry的子类、或RectangleD）
        :param screenSize: 屏幕大小[width, height]列表
        :return: 转化为地理坐标的几何体（Geometry的子类、或RectangleD）
        '''
        if isinstance(geometry, PointD):
            return PointD(x=(geometry.X - screenSize[0] / 2) * self.scale + self.offsetX,
                          y=self.offsetY - (geometry.Y - screenSize[1] / 2) * self.scale,
                          id=geometry.ID)
        elif isinstance(geometry, Polyline):
            data = [self.ScreenToGeo(geo, screenSize) for geo in geometry.data]
            return Polyline(data, id=geometry.ID)
        elif isinstance(geometry, Polygon):
            data = [self.ScreenToGeo(geo, screenSize) for geo in geometry.data]
            holes = None if geometry.holes is None else \
                [self.ScreenToGeo(geo, screenSize) for geo in geometry.holes]
            return Polygon(data, holes=holes, id=geometry.ID)
        elif isinstance(geometry, Polyline):
            data = [self.ScreenToGeo(geo, screenSize) for geo in geometry.data]
            return MultiPolyline(data, id=geometry.ID)
        elif isinstance(geometry, Polyline):
            data = [self.ScreenToGeo(geo, screenSize) for geo in geometry.data]
            return MultiPolygon(data, id=geometry.ID)
        elif isinstance(geometry, RectangleD):
            p_min = self.ScreenToGeo(PointD(geometry.MinX, geometry.MaxY), screenSize)
            p_max = self.ScreenToGeo(PointD(geometry.MaxX, geometry.MinY), screenSize)
            return RectangleD(minx=p_min.X, miny=p_min.Y, maxx=p_max.X, maxy=p_max.Y)
        else:
            raise ValueError('geometry not supported.')

    def GeoDistToScreen(self, distance):
        '''
        将地理距离转化为屏幕的（像素）距离
        :param distance: 地理距离(float)
        :return: 屏幕距离(float)
        '''
        return distance / self.scale

    def ScreenDistToGeo(self, distance):
        '''
        将屏幕像素距离转化地理距离
        :param distance: 屏幕距离(float)
        :return: 地理距离(float)
        '''
        return distance * self.scale

    def FullScreen(self, width, height):
        '''
        将地图缩放、平移至全屏显示box范围，即缩放范围至显示所有图层的要素
        :param width: 屏幕宽度（像素）
        :param height: 屏幕高度（像素）
        '''
        # 加这么一个判断是为了防止图层内什么都没有，外包矩形框过小
        # 或是矩形框的长度、宽度为0而出现bug
        if (self.box.MaxX - self.box.MinX) > 1e-6 and \
                (self.box.MaxY - self.box.MinY) > 1e-6:
            self.offsetX = (self.box.MinX + self.box.MaxX) / 2
            self.offsetY = (self.box.MinY + self.box.MaxY) / 2
            self.scale = max((self.box.MaxX - self.box.MinX) / width,
                             (self.box.MaxY - self.box.MinY) / height)

    def ZoomAtPoint(self, screenSize, point, newScale):
        '''
        以给定点（屏幕坐标）为缩放中心，缩放显示画面
        :param screenSize: 屏幕大小[width, height]列表
        :param point: 屏幕坐标的点（PointD类型）
        :param newScale: 更改后的缩小系数，一般是原来的scale乘除固定数
        '''
        self.offsetX += (point.X - screenSize[0] / 2) * (self.scale - newScale)
        self.offsetY += (point.Y - screenSize[1] / 2) * (newScale - self.scale)
        self.scale = newScale

    def AddLayer(self, layer, pos=0):
        '''
        添加一个图层，默认在最顶上
        :param layer: 图层Layer对象
        :param pos: 图层的位置，0为最顶层
        '''
        self.layers.insert(pos, layer)
        self.selectedLayer = pos
        self.RefreshBox()

    def DelLayer(self, index):
        '''删除指定下标的图层'''
        self.layers.pop(index)
        # 删除被选择的图层，默认将被选择图层转为最顶层
        if self.selectedLayer == index:
            self.selectedLayer = 0 if len(self.layers) > 0 else -1
        elif self.selectedLayer > index:
            self.selectedLayer -= 1
        self.RefreshBox()

    def ClearLayers(self):
        '''清除所有图层'''
        self.layers.clear()
        self.selectedLayer = -1

    def MoveUpLayer(self, index):
        '''将指定下标的图层上移一层，即index和index-1的图层位置交换'''
        if index > 0:
            self.layers[index], self.layers[index-1] = self.layers[index-1], self.layers[index]
            # 若指定移动的图层和当前被选择的图层有关系，则更新被选择图层
            if self.selectedLayer == index:
                self.selectedLayer -= 1
            elif self.selectedLayer == index - 1:
                self.selectedLayer += 1
        else:
            raise ValueError('已至最顶层')

    def MoveDownLayer(self, index):
        '''将指定下标的图层下移一层，即index和index+1的图层位置交换'''
        if index < len(self.layers) - 1:
            self.layers[index], self.layers[index+1] = self.layers[index+1], self.layers[index]
            # 若指定移动的图层和当前被选择的图层有关系，则更新被选择图层
            if self.selectedLayer == index:
                self.selectedLayer += 1
            elif self.selectedLayer == index + 1:
                self.selectedLayer -= 1
        else:
            raise ValueError('已至最底层')

    def MoveLayer(self, start_idx, end_idx):
        '''将下标为`start_idx`的图层取出，插入至下标为`end_idx`位置'''
        if start_idx == end_idx:
            return
        layer = self.layers.pop(start_idx)
        self.layers.insert(end_idx, layer)
        self.selectedLayer = end_idx
