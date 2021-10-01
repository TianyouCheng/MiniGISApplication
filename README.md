# MiniGISApplication
For GIS presentation

已实现功能
----
* 点击“创建新图层”按钮，给当前项目增加图层。
* 在某一图层被选中的情况下，点击“编辑模式”，开始编辑当前图层。
* 若无图层被选中，会弹出相应提示。
* 未能完成：在编辑模式下，选择其他的图层后，仍可进行编辑。（正常做法应该是在编辑中不允许选择其他图层）。由于监听选择的函数找不到而且没有这个约束也没有太大损失，因此打算不实现=。=
* 因此，可以开始进行绘图部分的工作啦！手动@侯远樵
* 待完成：选中图层后，将该图层下的所有要素都显示在表格控件中，这一步应该在绘图部分之后完成，因为需要看有哪些属性以及内存中的数据结构。

文件说明
----
### UI文件夹
* 界面文件,包括.UI和一些图像文件
* 把界面`.ui`和`.py`文件放入UI文件夹，然后在`__init__.py`中添加引用，即可在`Main.py`中直接使用。
### Function文件夹
* 函数功能文件
* 目前包括Geometry几何类，Layer图层类，Map地图类，Op_TableView,OP_TreeView控件操作函数
### Main文件
* 主函数文件，包括界面启动及基本功能
### .gitignore文件
* 忽视了使用Pycharm开发时自动生成的.idea，venv文件夹
### README文件

绘图参考
----
    https://www.pythonguis.com/tutorials/bitmap-graphics/

使用简要说明
----
    """点"""
    # 初始化
    pt1=PointD(0,5,8)#分别为x，y，ID
    pt2=PointD(3,3)#分别为x，y

    # 找到最大/最小X,Y坐标
    pt = pt1.FindMaxXY([pt1,pt2])
    pt = pt1.FindMinXY([pt1, pt2])
    print(pt)

    # 求与pt1的距离
    print(pt.GetDistance(pt1))

    # 判断与pt1的距离是否小于等于2
    print(pt.IsPointOn(pt1,2))

    # 判断是否在所选矩形内
    Rec=RectangleD(2,2,5,5)
    print(pt.IsWithinBox(Rec))

    # 移动点
    pt.Move(5,5)
    print(pt)

    # 当前点的最小外接矩阵
    pt.RenewBox()
    print(pt._box)

    """线"""
    # 初始化，以点的列表形式
    L1=Polyline([pt,pt1,pt2])
    print(L1)

    # 求点到直线距离
    L2 = Polyline([PointD(3, 3), PointD(5, 5), PointD(5, 8)])
    print(L2.GetDistance(PointD(3,5)))

    # 判断该直线与点的距离是否在给定buffer内
    print(L2.IsPointOn(PointD(3,5),1))

    # 判断直线上的各点是否在给定矩形内
    """注意：该算法不是判断线段与给定box相交"""
    Rec = RectangleD(3,3.5,4.5,5)
    print(L2.IsWithinBox(Rec))

    # 移动线
    L2.Move(1,1)
    print(L2)

    """面"""
    '''方法都一样，就不再测试（若有Bug再找我= =）'''
    Po1=Polygon([pt,pt1,pt2])
    print(Po1)

    """多线"""
    MulL1=MultiPolyline([L1,L2])
    print(MulL1)

    """多面"""
    Polygon1=Polygon([pt,pt2,pt2])
    Polygon2=Polygon([PointD(10,10),PointD(30,10),PointD(30,30)])
    PPolygon=MultiPolygon([Polygon1,Polygon2])
    print(PPolygon)
