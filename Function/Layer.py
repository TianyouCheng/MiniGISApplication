'''
图层类别及相关操作
'''
from .Geometry import *
import pandas as pd
from osgeo import ogr
from osgeo import osr
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
        self.attr_desp_dict = {'id': 'int'}         # 属性表描述，k为属性名称，v为属性类型，k,v均为str类型
        self.table = pd.DataFrame(columns=['id'])   # 属性表

        # TODO 有时间的话增加：绘制属性、按属性条件渲染、注记……
        self.edited_geometry=[]
        self.saved_in_dbm=False

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
                else self.table['id'].max() + 1
        self.geometries.append(geometry)
        geometry.ID = new_id
        new_row = pd.DataFrame(columns=self.table.columns)
        # 添加属性
        default_val = {'int': 0, 'float': 0.0, 'str': ''}
        if row is None:
            row = {key: default_val[val] for key, val in self.attr_desp_dict.items()}
        for col_name, col_type in self.attr_desp_dict.items():
            if col_name == 'id':
                new_row[col_name] = [new_id]
            elif col_name in row:
                new_row[col_name] = row[col_name] if isinstance(row, pd.DataFrame) else row[col_name] \
                    if isinstance(row[col_name], (tuple, list)) else [row[col_name]]
            else:
                new_row[col_name] = default_val[col_type] if isinstance(default_val[col_type], (tuple, list)) \
                    else [default_val[col_type]]
        self.table = self.table.append(new_row, ignore_index=True)
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
            self.table.drop(index=self.table[self.table['id'] == _id].index, inplace=True)
            self.table.reset_index(drop=True, inplace=True)
        self.RefreshBox()

    def add_attr(self, attr_name, attr_type):
        '''
        给属性表增加一列字段
        :param attr_name: 列名称
        :param attr_type: 列的类型，字符串：支持'int', 'float', 'string'
        '''
        import numpy as np
        geoms_num = self.table.shape[0]
        if attr_type == 'int':
            new_column = pd.DataFrame(data={attr_name: np.zeros((geoms_num,), dtype=np.int_)})
        elif attr_type == 'float':
            new_column = pd.DataFrame(data={attr_name: np.zeros((geoms_num,), dtype=np.float_)})
        elif attr_type == 'string' or attr_type == 'str':
            new_column = pd.DataFrame(data={attr_name: [''] * geoms_num}, dtype=str)
            attr_type = 'str'
        else:
            raise ValueError(f'不支持添加"{attr_type}"类型字段')
        self.attr_desp_dict[attr_name] = attr_type
        self.table = pd.concat([self.table, new_column], axis=1)

    def del_attr(self, attr_name):
        '''
        删除属性表中的一列字段
        :param attr_name: 列名称
        '''
        del self.table[attr_name]
        del self.attr_desp_dict[attr_name]

    def Query(self, query, *args):
        '''
        查找满足条件的几何体
        :param query: 可以是一个点（鼠标点选查询）、一个矩形框（鼠标框选）、
                      可以是属性查询语句？选做？
                      点选条件下应明确写成Query(point, buffer)
        :return: 被选中的几何体ID集合（注：未更新self.selectedItems）
        '''
        if isinstance(query, PointD):
            return self._QueryPoint(query, args[0])
        if isinstance(query, RectangleD):
            return self._QueryBox(query)
        if isinstance(query, str):
            return self._QuerySQL(query)

    def _QueryPoint(self, point, buffer):
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

    def _QueryBox(self, box):
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

    def _QuerySQL(self, sql):
        '''
        几何体的属性查询
        :param sql: 文本查询
        :return: 被选中的几何体ID集合（注：未更新self.selectedItems）
        '''
        return list(self.table.query(sql)['id'])

    @property
    def Count(self):
        return len(self.geometries)


    #假设属性表用的pandas，根据geom id查询其属性，一般返回所有属性值构成的列表，当指定name时返回单个属性值构成的列表。也可以是字典
    def get_attr(self,id,attr_name=None):
        result = self.table[self.table['id'] == id]
        if result.shape[0] == 0:
            return []
        if attr_name is None:
            return list(result.iloc[0, :])
        else:
            return result.iloc[0, attr_name]

    def import_from_shplayer(self, shplayer):
        defn = shplayer.GetLayerDefn()
        fieldcount = defn.GetFieldCount()
        fields = list()
        type_dict = {ogr.OFTInteger: 'int',
                     ogr.OFTString: 'str',
                     ogr.OFTReal: 'float'
                     }
        for att in range(fieldcount):
            field = defn.GetFieldDefn(att)
            fields.append(field.GetNameRef())
            self.add_attr(field.GetNameRef(), type_dict[field.GetType()])
        feat = shplayer.GetNextFeature()
        while feat:
            geom = feat.GetGeometryRef()
            geom_type = geom.GetGeometryType()
            id = int(feat.GetFieldAsString('FID') if 'FID' in self.attr_desp_dict else 0)
            field_dict = dict()
            field_dict['id'] = [id]
            for name in fields:
                if self.attr_desp_dict[name] == 'int':
                    field_dict[name] = [int(feat.GetFieldAsString(name))]
                elif self.attr_desp_dict[name] == 'float':
                    field_dict[name] = [float(feat.GetFieldAsString(name))]
                else:
                    field_dict[name] = [feat.GetFieldAsString(name)]
            if geom_type == ogr.wkbPoint:
                ft = PointD(geom.GetX(), geom.GetY(), id)
            elif geom_type == ogr.wkbLineString:
                ptnum = geom.GetPointCount()
                data = list()
                for i in range(ptnum):
                    data.append(PointD(geom.GetX(i), geom.GetY(i)))
                if self.type == MultiPolyline:
                    ft = MultiPolyline([Polyline(data)], id)
                else:
                    ft = Polyline(data, id)
            elif geom_type == ogr.wkbPolygon:
                ringnum = geom.GetGeometryCount()
                outring = list()
                inring = list()
                pin = None
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
                        pin = Polygon(insubring)
                        inring.append(pin)
                if self.type == MultiPolygon:
                    ft = MultiPolygon([Polygon(outring, inring)], id)
                else:
                    ft = Polygon(outring, inring, id)
            elif geom_type == ogr.wkbMultiLineString:
                linenum = geom.GetGeometryCount()
                lines = list()
                for i in range(linenum):
                    line = geom.GetGeometryRef(i)
                    pt_num = line.GetPointCount()
                    pts = list()
                    for j in range(pt_num):
                        pts.append(PointD(line.GetX(j), line.GetY(j)))
                    lines.append(Polyline(pts))
                ft = MultiPolyline(lines, id)
            elif geom_type == ogr.wkbMultiPolygon:
                poly_num = geom.GetGeometryCount()
                polygons = list()
                for i in range(poly_num):
                    pg = geom.GetGeometryRef(i)
                    ringnum = pg.GetGeometryCount()
                    outring = list()
                    inring = list()
                    for j in range(ringnum):
                        ring = pg.GetGeometryRef(j)
                        pt_num = ring.GetPointCount()
                        if j == 0:
                            for k in range(pt_num - 1):
                                outring.append(PointD(ring.GetX(k), ring.GetY(k)))
                        else:
                            insubring = list()
                            for k in range(pt_num - 1):
                                insubring.append(PointD(ring.GetX(k), ring.GetY(k)))
                            inring.append(Polygon(insubring))
                    polygons.append(Polygon(outring, inring))
                ft = MultiPolygon(polygons, id)
            else:
                ft = None
            self.AddGeometry(ft, field_dict)
            feat = shplayer.GetNextFeature()

    def export_to_shplayer(self, path):
        type_dict = {'int' : ogr.OFTInteger,
                     'str' : ogr.OFTString,
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
        dst_osr = osr.SpatialReference()
        dst_osr.ImportFromEPSG(3857)
        outlayer = oDs.CreateLayer(file_name.split('.')[0], dst_osr, geom_type=geotype_dict[self.type])
        for f in fields:
            new_field = ogr.FieldDefn(f, type_dict[self.attr_desp_dict[f]])
            outlayer.CreateField(new_field)
        featureDefn = outlayer.GetLayerDefn()
        for i, g in enumerate(self.geometries):
            geom = ogr.CreateGeometryFromWkt(g.ToWkt())
            ft = ogr.Feature(featureDefn)
            ft.SetGeometry(geom)
            values = self.table.iloc[i].tolist()
            for f, v in zip(fields, values):
                ft.SetField(f, v)
            outlayer.CreateFeature(ft)

if __name__=='__main__':
    print(1)