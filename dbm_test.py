from Function import *

def create_map(dbm:DBM):
    map = Map()
    layer1 = Layer(Polyline, name='lines')
    layer1.AddGeometry(Polyline([PointD(1, 1), PointD(2, 2), PointD(2, 4), PointD(4, 6)], id=0),
                       pd.DataFrame({'ID': [0], 'name': ['aaa']}))
    layer1.AddGeometry(Polyline([PointD(0, 6), PointD(1, 3), PointD(2, 5), PointD(3, 3)], id=1),
                       pd.DataFrame({'ID': [1], 'name': ['bbb']}))
    layer1.AddGeometry(Polyline([PointD(-1, 3), PointD(2, 3), PointD(4, 5), PointD(2, 6)], id=2),
                       pd.DataFrame({'ID': [2], 'name': ['ccc']}))
    layer1.selectedItems.extend([0, 1])
    map.AddLayer(layer1)

    map.FullScreen(1010, 566)
    dbm.add_layer_from_memory(layer1)
    return map

if __name__=='__main__':
    dbm=DBM()
    a=dbm.get_layers_info()
    print(a)
    a.dbm