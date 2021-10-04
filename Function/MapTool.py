'''
枚举类，记录软件当前的使用工具
'''

from enum import Enum, unique


@unique
class MapTool(Enum):
    '''
    枚举类，记录软件当前的使用工具，也即鼠标的状态
    '''
    Null = 1            # 单纯的鼠标指针，什么用都没有
    ZoomIn = 2          # 放大，左键单击可以放大显示界面
    ZoomOut = 4         # 缩小，左键单击可以缩小显示界面
    Pan = 8             # 漫游，按住左键可拖动显示画面
    Select = 16         # 选择，左键单击点选，按住左键拖动可框选
    AddGeometry = 32    # 添加几何体模式
    EditGeometry = 64   # 编辑几何体模式
