'''
图层类别及相关操作
'''
from Geometry import *


class Layer(object):
    def __init__(self, _type, name='new_layer'):
        '''
        :param _type: 图层中几何体的类别，用type类型
        :param name: 图层名字
        '''
        self.type = _type           # 图层中几何体类别
        self.name = name            # 图层名字
        self.visible = True         # 图层可见状态
        self.geometries = []        # 几何体列表
        self.box = RectangleD()     # 图层外包矩形
        self.selectedItems = []     # 被选中的几何体ID（为了使选中几何体和属性表结合）

        self.srid=3857
        self.attr_desp_dict={}      # 属性表描述，k为属性名称，v为属性类型，k,v均为str类型
        self.table = None           # 属性表，TODO 属性表的实现方法待定
        # TODO 有时间的话增加：绘制属性、按属性条件渲染、注记……

    def RefreshBox(self):
        '''更新图层的外包矩形'''
        if len(self.geometries) > 0:
            first_box = self.geometries[0].box
            self.box.MinX =first_box.MinX
            self.box.MinY = first_box.MinY
            self.box.MaxX = first_box.MaxX
            self.box.MaxY = first_box.MaxY
            # 遍历所有几何体找到最终的min, max值
            for geometry in self.geometries:
                if geometry.box.MinX < self.box.MinX:
                    self.box.MinX = geometry.box.MinX
                if geometry.box.MinY < self.box.MinY:
                    self.box.MinY = geometry.box.MinY
                if geometry.box.MaxX > self.box.MaxX:
                    self.box.MaxX = geometry.box.MaxX
                if geometry.box.MaxY > self.box.MaxY:
                    self.box.MaxY = geometry.box.MaxY

    def AddGeometry(self, geometry, row=None):
        '''
        向图层中增加几何体
        :param geometry: `Geometry`的子类几何体
        :param row: 可选，该行的属性数据
        '''
        if not isinstance(geometry, self.type):
            raise TypeError('添加几何体类型与图层类型不匹配')
        self.geometries.append(geometry)
        # TODO 记得给几何体分配ID，并在属性表中添加该几何体的属性信息
        self.RefreshBox()

    def DelGeometry(self, _id):
        index = None
        for i, geo in enumerate(self.geometries):
            if geo.ID == _id:
                index = i
                break
        if index is not None:
            self.geometries.pop(index)
            # TODO 属性表也要跟着删除
        self.RefreshBox()

    def Query(self, query, *args):
        '''
        查找满足条件的几何体
        :param query: 可以是一个点（鼠标点选查询）、一个矩形框（鼠标框选）、
                      可以是属性查询语句？选做？
                      点选条件下应明确写成Query(point, buffer)
        :return: 被选中的几何体ID集合（注：未更新self.selectedItems）
        '''
        if isinstance(query, PointD):
            return self.QueryPoint(query, args[0])
        if isinstance(query, RectangleD):
            return self.QueryBox(query)
        if isinstance(query, str):
            return self.QuerySQL(query)

    def QueryPoint(self, point, buffer):
        '''
        点选几何体
        :param point: 鼠标点的地理坐标
        :param buffer: 地理距离（鼠标点与之距离小于buffer则选中）
        :return: 被选中的几何体ID集合（注：未更新self.selectedItems）
        '''
        selected = []
        if self.box.IsPointOn(point):
            for geometry in self.geometries:
                if geometry.IsPointOn(point, buffer):
                    selected.append(geometry.ID)
        return selected

    def QueryBox(self, box):
        '''
        框选几何体
        :param box: 矩形框的地理坐标
        :return: 被选中的几何体ID集合（注：未更新self.selectedItems）
        '''
        selected = []
        if not (self.box.MinX > box.MaxX or self.box.MinY > box.MaxY or
                self.box.MaxX < box.MinX or self.box.MaxY < box.MaxY):
            for geometry in self.geometries:
                if geometry.IsIntersectBox(box):
                    selected.append(geometry.ID)
        return selected

    def QuerySQL(self, sql):
        '''
        几何体的属性查询
        :param sql: 文本查询
        :return: 被选中的几何体ID集合（注：未更新self.selectedItems）
        '''
        pass

    @property
    def Count(self):
        return len(self.geometries)


    #假设属性表用的pandas，根据geom id查询其属性，一般返回所有属性值构成的列表，当指定name时返回单个属性值构成的列表。也可以是字典
    def get_attr(self,id,attr_name=None):
        pass

if __name__=='__main__':
    print(1)