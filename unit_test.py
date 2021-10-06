'''
单元测试的相关函数
'''


from Function import *


def create_map() -> Map:
    '''构建一个简单的地图MAP样例'''
    map = Map()
    layer1 = Layer(Polyline, name='lines')
    layer1.AddGeometry(Polyline([PointD(1, 1), PointD(2, 2), PointD(2, 4), PointD(4, 6)], id=0))
    layer1.AddGeometry(Polyline([PointD(0, 6), PointD(1, 3), PointD(2, 5), PointD(3, 3)], id=1))
    layer1.AddGeometry(Polyline([PointD(-1, 3), PointD(2, 3), PointD(4, 5), PointD(2, 6)], id=2))
    layer1.selectedItems.append(1)
    map.AddLayer(layer1)

    layer2 = Layer(PointD, name='points')
    layer2.AddGeometry(PointD(0, 2, id=0))
    layer2.AddGeometry(PointD(4, 4, id=1))
    layer2.AddGeometry(PointD(0, 4, id=2))
    layer2.AddGeometry(PointD(3, 2, id=3))
    map.AddLayer(layer2)

    layer3 = Layer(Polygon, name='polygons')
    layer3.AddGeometry(Polygon([PointD(6, 1), PointD(7, 2), PointD(6, 2.5)], id=0))
    layer3.AddGeometry(Polygon([PointD(5, 1.5), PointD(6, 3), PointD(7, 2.5), PointD(6, 4)], id=1))
    layer3.AddGeometry(Polygon([PointD(4, 4.5), PointD(7, 4), PointD(9, 5), PointD(7, 5), PointD(4, 7), PointD(5, 5)], id=2))
    layer3.selectedItems.append(1)
    map.AddLayer(layer3, 2)
    map.selectedLayer = 2
    map.FullScreen(1010, 566)
    return map
