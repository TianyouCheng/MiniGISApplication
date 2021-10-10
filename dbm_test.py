from Function import *

def create_map(dbm):
    layer_list=dbm.get_layers_list()
    map=Map()
    map.AddLayer(dbm.load_layer(layer_list[2]))
    return map

if __name__=='__main__':
    dbm=DBM()
    a=dbm.get_layers_info()
    print(a)
    a.dbm