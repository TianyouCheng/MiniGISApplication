'''
图层类别及相关操作
'''
from .Geometry import *
import pandas as pd
from osgeo import ogr
from osgeo import gdal
import os

class Layer(object):
    def __init__(self, _type, name='new_layer',srid=3857):
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

        self.srid=srid
        self.attr_desp_dict = {'ID': 'int'}         # 属性表描述，k为属性名称，v为属性类型，k,v均为str类型
        self.table = pd.DataFrame(columns=['ID'])   # 属性表，TODO 属性表的实现方法目前就定是pandas了

        # TODO 有时间的话增加：绘制属性、按属性条件渲染、注记……
        self.edited_geometry=[]

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
        new_id = 0 if self.table.shape[0] == 0 \
                else self.table['ID'].max() + 1
        self.geometries.append(geometry)
        # TODO 记得给几何体分配ID，并在属性表中添加该几何体的属性信息
        geometry.ID = new_id
        if row is None:
            row = pd.DataFrame({'ID': [new_id]})
        else:
            row['ID'] = new_id
        self.table = self.table.append(row, ignore_index=True)
        self.table.reset_index(drop=True, inplace=True)
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
            self.table.drop(index=self.table[self.table['ID'] == _id].index, inplace=True)
            self.table.reset_index(drop=True, inplace=True)
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
        buffer_box = self.box.Expand(buffer)
        if buffer_box.IsPointOn(point):
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
        if self.box.IsIntersectBox(box):
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
        result = self.table[self.table['ID'] == id]
        if result.shape[0] == 0:
            return []
        if attr_name is None:
            return list(result.iloc[0, :])
        else:
            return result.iloc[0, attr_name]

    def import_from_shplayer(self, shplayer):
        ori_type = shplayer.GetGeomType()
        defn = shplayer.GetLayerDefn()
        fieldcount = shplayer.GetFieldCount()
        fields = list()
        type_dict = {ogr.OFTInteger: 'int',
                     ogr.OFTString: 'varchar',
                     ogr.OFTReal: 'float'
                     }
        for att in range(fieldcount):
            field = defn.GetFieldDefn(att)
            fields.append(field.GetNameRef())
            self.attr_desp_dict[field.GetNameRef()] = type_dict[field.GetType()]
        feat = shplayer.GetNextFeature()
        while feat:
            geom = feat.GetGeometryRef()
            id = int(feat.GetFieldAsString('FID'))
            field_dict = dict()
            field_dict['ID'] = [0]
            for name in fields:
                if self.attr_desp_dict[name] == 'int':
                    field_dict[name] = [int(feat.GetFieldAsString(name))]
                elif self.attr_desp_dict[name] == 'float':
                    field_dict[name] = [float(feat.GetFieldAsString(name))]
                else:
                    field_dict[name] = [feat.GetFieldAsString(name)]
            if ori_type == ogr.wkbPoint:
                ft = PointD(geom.GetX(), geom.GetY(), id)
            elif ori_type == ogr.wkbLineString:
                ptnum = geom.GetPointCount()
                data = list()
                for i in range(ptnum):
                    data.append(PointD(geom.GetX(i), geom.GetY(i)))
                ft = Polyline(data, id)
            elif ori_type == ogr.wkbPolygon:
                ringnum = geom.GetGeometryCount()
                outring = list()
                inring = list()
                for i in range(ringnum):
                    ring = geom.GetGeometryRef(i)
                    pt_num = ring.GetPointCount()
                    if i == 0:
                        for j in range(pt_num - 1):
                            outring.append(PointD(ring.GetX(j), ring.GetY(j)))
                    else:
                        insubring = list()
                        for j in range(pt_num - 1):
                            insubring.append(PointD(ring.GetX(j), ring.GetY(j)))
                        inring.append(insubring)
                ft = Polygon(outring, inring, id)
            elif ori_type == ogr.wkbMultiLineString:
                linenum = geom.GetGeometryCount()
                lines = list()
                for i in range(linenum):
                    line = geom.GetGeometryRef(i)
                    pt_num = ring.GetPointCount()
                    pts = list()
                    for j in range(pt_num):
                        pts.append(PointD(line.GetX(j), line.GetY(j)))
                    lines.append(Polyline(pts))
                ft = MultiPolyline(lines, id)
            elif ori_type == ogr.wkbMultiPolygon:
                poly_num = geom.GetGeometryCount()
                polygons = list()
                for i in range(poly_num):
                    pg = geom.GetGeometryRef(i)
                    ringnum = pg.GetPointCount()
                    outring = list()
                    inring = list()
                    for j in range(ringnum):
                        ring = pg.GetGeometryRef(j)
                        pt_num = ring.GetPointCount()
                        if j == 0:
                            for k in range(pt_num - 1):
                                outring.append(PointD(ring.GetX(k),ring.GetY(k)))
                        else:
                            insubring = list()
                            for k in range(pt_num - 1):
                                insubring.append(PointD(ring.GetX(k),ring.GetY(k)))
                            inring.append(insubring)
                    polygons.append(Polygon(outring, inring))
                ft = MultiPolygon(polygons, id)
            self.AddGeometry(ft, field_dict)
            feat = shplayer.GetNextFeature()

    def export_to_shplayer(self, path):
        type_dict = {'int' : ogr.OFTInteger,
                     'varchar' : ogr.OFTString,
                     'float' : ogr.OFTReal
                     }
        geotype_dict = {
            PointD : ogr.wkbPoint,
            Polyline : ogr.wkbLineString,
            Polygon : ogr.wkbPolygon,
            MultiPolyline : ogr.wkbMultiLineString,
            MultiPolygon : ogr.wkbMultiPolygon
        }
        file_name = path.split('/')[-1]
        related_path = path.split(file_name)[0]
        os.chdir(related_path)
        oDriver = ogr.GetDriverByName('ESRI Shapefile')
        oDs = oDriver.CreateDataSource(file_name)
        if os.path.exists(path):
            oDriver.DeleteDataSource(file_name)
        fields = self.table.columns.tolist()
        outlayer = oDs.CreateLayer(file_name.split('.')[0], geom_type=geotype_dict[self.type])
        for f in fields:
            new_field = ogr.FieldDefn(f, type_dict[self.attr_desp_dict[f]])
            outlayer.CreateField(new_field)
        featureDefn = outlayer.GetLayerDefn()
        for i, g in enumerate(self.geometries):
            geom = ogr.CreateGeometryFromWkt(g.ToWkt())
            ft = ogr.Feature(featureDefn)
            ft.SetGeometry(geom)
            values = self.table.iloc[[i]].tolist()
            for f, v in zip(fields, values):
                ft.SetField(f, v)
            outlayer.CreateFeature(ft)

if __name__=='__main__':
    print(1)