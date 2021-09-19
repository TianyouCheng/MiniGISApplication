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
        return ("Box:\nMinX={}; MinY={}; MaxX={}; MaxY={}".format(self.MinX,self.MinY,self.MaxX,self.MaxY))
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
        """point在两点构成的上三角形内"""
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
        self.RenewBox()

    # 方法
    # 点选——缓冲区4*4
    def IsPointOn(self,point,BufferDist):
        if self.GetDistance(point)<=BufferDist:
            return True
        else:
            return False

    def IsWithinBox(self,box):
        if box.IsPointOn(self):
            return True
        else:
            return False

    def Move(self,deltaX,deltaY):
        self.X+=deltaX
        self.Y+=deltaY
        self.RenewBox()

    def RenewBox(self):
        self._box.MaxX=self._box.MinX=self.X
        self._box.MaxY = self._box.MinY = self.Y

    def GetDistance(self,MouseLocation):
        dis=math.sqrt((MouseLocation.X-self.X)*(MouseLocation.X-self.X)+(MouseLocation.Y-self.Y)*(MouseLocation.Y-self.Y))
        return dis

    # 重写print
    def __str__(self):
        return ("Point:\nX={}; Y={}; ID={}".format(self.X,self.Y,self.ID))
# endregion

# region 子类——线
class Polyline(Geometry):
    # 属性 data是点构成的List
    def __init__(self,Data,id=-1):
        Geometry.__init__(self,id)
        self.data=Data
        self.RenewBox()

    # 方法
    def IsPointOn(self,point,BufferDist):
        """用盒子判断前要先扩展盒子"""
        self._box.MinX-=BufferDist
        self._box.MinY-=BufferDist
        self._box.MaxX+=BufferDist
        self._box.MaxY+=BufferDist
        if self._box.IsPointOn(point):
            point_dis=self.GetDistance(point)
            if point_dis<=BufferDist:
                return True
            else:
                return False
        else:
            return False
        self.RenewBox()

    def IsWithinBox(self,box):
        if self._box.MaxX<=box.MaxX and self._box.MaxY<=box.MaxY and self._box.MinX>box.MinX and self._box.MinY>box.MinY:
            return True
        for i in range(len(self.data)):
            if self.data[i].IsWithinBox(box):
                return True
        return False

    def Move(self,deltaX,deltaY):
        for i in range(len(self.data)):
            self.data[i].X+=deltaX
            self.data[i].Y+=deltaY
        self.RenewBox()

    def RenewBox(self):
        MaxXY=self.FindMaxXY(self.data)
        MinXY=self.FindMinXY(self.data)
        self._box.MaxX=MaxXY.X
        self._box.MaxY=MaxXY.Y
        self._box.MinX=MinXY.X
        self._box.MinY=MinXY.Y

    def GetDistance(self,MouseLocation):
        """获取点击点到线的距离"""
        MinDistance=math.sqrt((self.data[0].X-MouseLocation.X)*(self.data[0].X-MouseLocation.X)+(self.data[0].Y-MouseLocation.Y)*(self.data[0].Y-MouseLocation.Y))
        distance1=0
        for i in range(len(self.data)-1):
            a=PointD(1,1)
            b=PointD(1,1)
            a.X=MouseLocation.X-self.data[i].X
            a.Y=MouseLocation.Y-self.data[i].Y

            b.X=self.data[i+1].X-self.data[i].X
            b.Y=self.data[i+1].Y-self.data[i].Y
            neiji=(a.X*b.X+a.Y*b.Y)
            judge=neiji/(b.X*b.X+b.Y*b.Y)
            if judge<0:
                distance1=math.sqrt(a.X*a.X+a.Y*a.Y)
            elif judge>1:
                distance1=math.sqrt((MouseLocation.X-self.data[i+1].X)*(MouseLocation.X-self.data[i+1].X)+(MouseLocation.Y-self.data[i+1].Y)*(MouseLocation.Y-self.data[i+1].Y))
            else:
                distance1=abs(a.X*b.Y-b.X*a.Y)/math.sqrt(b.X*b.X+b.Y*b.Y)

            if distance1<MinDistance:
                MinDistance=distance1
        return MinDistance

    def __str__(self):
        s='Line:\n'
        for i in range(len(self.data)):
            s+='Point{}({},{})\n'.format(i+1,self.data[i].X,self.data[i].Y)
        return s
# endregion

# region 子类——多边形
class Polygon(Geometry):
    # 属性 data是点构成的List
    def __init__(self,Data,id=-1):
        Geometry.__init__(self,id)
        self.data=Data
        self.RenewBox()

    # 方法
    def IsPointOn(self,point,BufferDist):
        self._box.MinX -= BufferDist
        self._box.MinY -= BufferDist
        self._box.MaxX += BufferDist
        self._box.MaxY += BufferDist
        if(self._box.IsPointOn(point)):# 先用box判断
            NumOfPointIntersection=0
            for i in range(len(self.data)-1):
                if self.IfHasPoint(point,self.data[i],self.data[i+1]):
                    NumOfPointIntersection+=1
            # 首尾连接线的交点判断
            if self.IfHasPoint(point,self.data[0],self.data[len(self.data)-1]):
                NumOfPointIntersection+=1
            if NumOfPointIntersection%2==0:
                return False
            else:
                return True
        else:
            return False
        # !!!!!!!!!!!!!!!!!!!研究一下这个算法

        self.RenewBox()