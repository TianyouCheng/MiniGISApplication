'''
几何相关类+外包矩阵类
'''
import math
# region 矩阵类——外包矩阵、框选矩阵
class RectangleD(object):
    def __init__(self,minx=0,miny=0,maxx=0,maxy=0):
        self.MinX=minx
        self.MinY=miny
        self.MaxX=maxx
        self.MaxY=maxy

    # 判断点是否在矩形内，是返回True
    def IsPointOn(self, point):
        return point.X>=self.MinX and point.Y>=self.MinY and point.X<=self.MaxX and point.Y<=self.MaxY

    # 重写print
    def __str__(self):
        return ("MinX={}; MinY={}; MaxX={}; MaxY={}".format(self.MinX,self.MinY,self.MaxX,self.MaxY))
# endregion

# region 集合类——基类
class Geometry(object):
    _needRenewBox=True
    _box=RectangleD()

    # 属性
    def __init__(self, id=-1):
        self.ID=id

    def box(self):
        return self._box

    def box(self,value):
        self._box=value

    # 方法
    # 图像整体平移
    def Move(self,deltaX,deltaY):pass

    # 点选一该Point是否能选中几何体
    def IsPointOn(self,point,BufferDist):pass

    # 框选一该box是否能选中几何体
    def IsWithinBox(self,box):pass

    # 指示几何体需更新外包矩形
    def NeedRenewBox(self):
        self._needRenewBox=True

    def GetDistance(self,MouseLocation):pass

    # 私有函数
    def _RenewBox(self):pass

    def FindMaxXY(self,data):
        maxX=data[0].X
        maxY=data[0].Y
        for i in range(len(data)):
            if data[i].X>maxX:
                maxX=data[i].X
            if data[i].Y>maxY:
                maxY=data[i].Y
        outputP=PointD(maxX,maxY)
        return outputP

    def FindMinXY(self,data):
        minX = data[0].X
        minY = data[0].Y
        for i in range(len(data)):
            if data[i].X < minX:
                minX = data[i].X
            if data[i].Y < minY:
                minY = data[i].Y
        outputP = PointD(minX, minY)
        return outputP

    def IfHasPoint(self,point,startP,endP):
        maxY=max(startP.Y,endP.Y)
        minY=min(startP.Y,endP.Y)
        if point.Y>minY and point.Y<=maxY:
            cx=(startP.X-endP.X)/(startP.Y-endP.Y)*(point.Y-endP.Y)+endP.X
            print(cx)
            return cx>=point.X
        else:
            return False
# endregion

# region 子类——点
class PointD(Geometry):
    # 属性
    def __init__(self,x=0,y=0,id=-1):
        Geometry.__init__(self,id)
        self.X=x
        self.Y=y

    # 方法
    # 点选——缓冲区4*4
    def IsPointOn(self,point,BufferDist):
        if self.GetDistance(point)<=BufferDist:
            return True
        else:
            return False

    def IsWithinBox(self,box):
        if(box.IsPointOn(self)):
            return True
        else:
            return False

    def Move(self,deltaX,deltaY):
        self.X+=deltaX
        self.Y+=deltaY

    def RenewBox(self):
        self._box.MaxX=self._box.MinX=self.X
        self._box.MaxY = self._box.MinY = self.Y

    def GetDistance(self,MouseLocation):
        dis=math.sqrt((MouseLocation.X-self.X)*(MouseLocation.X-self.X)+(MouseLocation.Y-self.Y)*(MouseLocation.Y-self.Y))
        return dis

    # 重写print
    def __str__(self):
        return ("X={}; Y={}; ID={}".format(self.X,self.Y,self.ID))
# endregion

