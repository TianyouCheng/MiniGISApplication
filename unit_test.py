'''
单元测试的相关函数
'''


from Function import *
import pandas as pd


def create_map() -> Map:
    '''构建一个简单的地图MAP样例'''
    map = Map()
    layer1 = Layer(Polyline, name='lines')
    layer1.add_attr('name', 'str')
    layer1.add_attr('value', 'float')
    layer1.AddGeometry(Polyline([PointD(1, 1), PointD(2, 2), PointD(2, 4), PointD(4, 6), PointD(6, 6)], id=0),
                       pd.DataFrame({'id': [0], 'name': ['aaa'], 'value': [20]}))
    layer1.AddGeometry(Polyline([PointD(0, 6), PointD(1, 3), PointD(2, 5), PointD(3, 3)], id=1),
                       pd.DataFrame({'id': [1], 'name': ['bbb'], 'value': [53]}))
    layer1.AddGeometry(Polyline([PointD(-1, 3), PointD(2, 3), PointD(4, 5), PointD(2, 6)], id=2),
                       pd.DataFrame({'id': [2], 'name': ['ccc'], 'value': [32]}))
    layer1.selectedItems.extend([0, 1])
    map.AddLayer(layer1)

    layer2 = Layer(PointD, name='point')
    layer2.AddGeometry(PointD(0, 3, id=0))
    layer2.AddGeometry(PointD(4, 5, id=1))
    layer2.AddGeometry(PointD(0, 4, id=2))
    layer2.AddGeometry(PointD(3, 3, id=3))
    map.AddLayer(layer2)

    layer3 = Layer(Polygon, name='polygons')
    layer3.AddGeometry(Polygon([PointD(6, 1), PointD(7, 2), PointD(6, 2.5)], id=0))
    layer3.AddGeometry(Polygon([PointD(5, 1.5), PointD(6, 3), PointD(7, 2.5), PointD(6, 4)], id=1))
    polygon2 = Polygon([PointD(4, 4.5), PointD(7, 4), PointD(9, 5), PointD(7, 5), PointD(4, 7), PointD(5, 5)],
                       holes=[Polygon([PointD(5, 6), PointD(7, 4.5), PointD(5.5, 5)])],
                       id=2)
    layer3.AddGeometry(polygon2)

    layer3.selectedItems.append(1)
    map.AddLayer(layer3, 2)
    map.selectedLayer = 1
    map.FullScreen(1010, 566)
    return map
