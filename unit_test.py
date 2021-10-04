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
    map.FullScreen(1010, 566)
    return map
