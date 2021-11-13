'''
几何相关类+外包矩阵类
'''
import math
from abc import ABC, abstractmethod
import re
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

    # 判断两个矩形是否相交
    def IsIntersectBox(self, box):
        return not (self.MaxX < box.MinX or self.MaxY < box.MinY or
                    self.MinX > box.MaxX or self.MinY > box.MaxY)

    def Expand(self, radius):
        '''
        将矩形按照radius半径扩张，即四个边向外移动radius距离。返回一个新的矩形。
        :param radius: 扩张半径
        :return: 扩张后的矩形
        '''
        return RectangleD(minx=self.MinX - radius, miny=self.MinY - radius,
                          maxx=self.MaxX + radius, maxy=self.MaxY + radius)

    # 重写print
    def __str__(self):
        return ("Box:\nMinX={}; MinY={}; MaxX={}; MaxY={}".format(self.MinX,self.MinY,self.MaxX,self.MaxY))
# endregion

# region 集合类——基类
class Geometry(ABC):

    # 属性
    def __init__(self, id=-1):
        self._box = RectangleD()
        self.ID=id
        self.gid=id
        # 轮廓颜色、线性、宽度、填充颜色、无、可见性、绑定字段、水平偏移、垂直偏移、字体大小、字体颜色
        # str/int/float/str/int/int/str/int/int/int/str
        self.StyleList=[
            '#f5f500',
            0,
            1.5,
            '#6edda4',
            0,
            0,
            'id',
            0,
            0,
            10,
            '#000000'
        ]

    @property
    def box(self):
        return self._box

    @box.setter
    def box(self,value):
        self._box=value

    # 方法
    # 图像整体平移
    @abstractmethod
    def Move(self,deltaX,deltaY):pass

    # 点选一该Point是否能选中几何体
    @abstractmethod
    def IsPointOn(self,point,BufferDist):pass

    # 框选一该box是否能选中几何体
    @abstractmethod
    def IsIntersectBox(self, box):pass

    # 找到画注记的位置，为几何中心或距离几何中心最近的点
    @abstractmethod
    def MarkPos(self):pass

    # 将几何体转为WKT字符串
    @abstractmethod
    def ToWkt(self):pass

    @abstractmethod
    def GetDistance(self,MouseLocation):pass

    # 私有函数
    @abstractmethod
    def RenewBox(self):pass

    @staticmethod
    def FindMaxXY(data):
        maxX=data[0].X
        maxY=data[0].Y
        for i in range(len(data)):
            if data[i].X>maxX:
                maxX=data[i].X
            if data[i].Y>maxY:
                maxY=data[i].Y
        outputP=PointD(maxX,maxY)
        return outputP

    @staticmethod
    def FindMinXY(data):
        minX = data[0].X
        minY = data[0].Y
        for i in range(len(data)):
            if data[i].X < minX:
                minX = data[i].X
            if data[i].Y < minY:
                minY = data[i].Y
        outputP = PointD(minX, minY)
        return outputP

    @staticmethod
    def IfHasPoint(point,startP,endP):
        """
        :return：True为point向右的射线与(startP, endP)线段相交
        :exception 可以处理平行的情况
        """
        maxY=max(startP.Y,endP.Y)
        minY=min(startP.Y,endP.Y)
        if point.Y>minY and point.Y<=maxY:
            cx=(startP.X-endP.X)/(startP.Y-endP.Y)*(point.Y-endP.Y)+endP.X
            return cx>=point.X
        else:
            return False

    @staticmethod
    def IsLineIntersect(pa1, pa2, pb1, pb2):
        '''
        判断两“线段”是否相交：
        若相交，则线段1的两端点在线段2两侧，同时线段2的两端点在线段1两侧
        算法：向量(OB x OA)(OC x OA) < 0，则B、C两点在OA两侧
        '''
        z1 = (pb1.X - pa1.X) * (pa2.Y - pa1.Y) - (pa2.X - pa1.X) * (pb1.Y - pa1.Y)
        z2 = (pb2.X - pa1.X) * (pa2.Y - pa1.Y) - (pa2.X - pa1.X) * (pb2.Y - pa1.Y)
        z3 = (pa1.X - pb1.X) * (pb2.Y - pb1.Y) - (pb2.X - pb1.X) * (pa1.Y - pb1.Y)
        z4 = (pa2.X - pb1.X) * (pb2.Y - pb1.Y) - (pb2.X - pb1.X) * (pa2.Y - pb1.Y)
        return z1 * z2 < 0 and z3 * z4 < 0

# endregion

# region 子类——点
class PointD(Geometry):
    # 属性
    def __init__(self,x=0,y=0,id=-1):
        Geometry.__init__(self,id)
        if type(x)==str:
            wkt_find=re.compile(r'\(\S+ \S+\)')
            find_rslt=wkt_find.findall(x)
            if find_rslt:
                match_rslt=re.match('^\((\S+) (\S+)\)$',find_rslt[0])
                if match_rslt:
                    self.X=float( match_rslt.group(1))
                    self.Y=float(match_rslt.group(2))
            else:
                self.X=0
                self.Y=0
        else:
            self.X=x
            self.Y=y
        self.RenewBox()


    # 方法
    # 点选——缓冲区4*4
    def IsPointOn(self,point,BufferDist):
        buffer_box = self._box.Expand(BufferDist)
        if not buffer_box.IsPointOn(point):
            return False
        if self.GetDistance(point)<=BufferDist:
            return True
        else:
            return False

    def IsIntersectBox(self, box):
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

    def MarkPos(self):
        return self

    def GetDistance(self,MouseLocation):
        dis=math.sqrt((MouseLocation.X-self.X)*(MouseLocation.X-self.X)+(MouseLocation.Y-self.Y)*(MouseLocation.Y-self.Y))
        return dis

    # 重写print
    def __str__(self):
        return ("Point:\nX={}; Y={}; ID={}".format(self.X,self.Y,self.ID))

    # 覆盖基类的ToWkt，将几何体转为WKT字符串
    def ToWkt(self):
        wkt=f"POINT({self.X} {self.Y})"
        return wkt
# endregion

# region 子类——线
class Polyline(Geometry):
    # 属性 data是点构成的List
    def __init__(self,Data,id=-1):
        Geometry.__init__(self,id)
        if type(Data)==str:
            wkt_find=re.compile(r'[^\(\)\, ]+ [^\(\)\, ]+')
            find_rslt=wkt_find.findall(Data)
            data=[]
            if find_rslt:
                for p in find_rslt:
                    match_rslt=re.match('^(\S+) (\S+)$',p)
                    if match_rslt:
                        data.append(PointD(float( match_rslt.group(1)),float(match_rslt.group(2))))
            self.data=data
        else:
            self.data=Data
        self.RenewBox()


    # 方法
    def IsPointOn(self,point,BufferDist):
        """用盒子判断前要先扩展盒子"""
        buffer = self._box.Expand(BufferDist)
        if buffer.IsPointOn(point):
            point_dis=self.GetDistance(point)
            if point_dis<=BufferDist:
                return True
        return False

    def IsIntersectBox(self, box):
        if not self._box.IsIntersectBox(box):
            return False
        if self._box.MaxX<=box.MaxX and self._box.MaxY<=box.MaxY and self._box.MinX>box.MinX and self._box.MinY>box.MinY:
            return True
        for i in range(len(self.data)):
            if self.data[i].IsIntersectBox(box):
                return True
        # 剩下的可能情形：折线每个端点都不在矩形内，却有可能与矩形相交
        # 这种相交一定会跟矩形的对角线相交
        for i in range(len(self.data) - 1):
            if self.IsLineIntersect(self.data[i], self.data[i + 1],
                               PointD(box.MinX, box.MinY), PointD(box.MaxX, box.MaxY)) \
                    or self.IsLineIntersect(self.data[i], self.data[i + 1],
                                       PointD(box.MaxX, box.MinY), PointD(box.MinX, box.MaxY)):
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

    def MarkPos(self):
        return self.data[len(self.data)//2]

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

    # 覆盖基类的ToWkt，将几何体转为WKT字符串
    def ToWkt(self):
        wkt=f"LINESTRING({','.join([f'{p.X} {p.Y}' for p in self.data])})"
        return wkt
# endregion

# region 子类——多边形
class Polygon(Geometry):
    # 属性 data是点构成的List, 表示多边形的外边界
    # 属性holes是Polygon构成的List（这些Polygon不能再有holes），表示多边形的洞
    def __init__(self,Data,holes=[], id=-1):
        Geometry.__init__(self,id)
        if type(Data)==str:
            wkt_find=re.compile(r'\([^\(\)\, ]+ [^\(\)\, ]+(?:\,[^\(\)\, ]+ [^\(\)\, ]+)+\)')
            # wkt_find=re.compile(r'[^\(\)\, ]+ [^\(\)\, ]+')
            find_rslt=wkt_find.findall(Data)
            data=[]
            holes=[]
            if find_rslt:
                wkt_find_line=re.compile(r'[^\(\)\, ]+ [^\(\)\, ]+')
                find_rslt_line=wkt_find_line.findall(find_rslt[0])
                if find_rslt_line:
                    for p in find_rslt_line:
                        match_rslt=re.match('^(\S+) (\S+)$',p)
                        if match_rslt:
                            data.append(PointD(float( match_rslt.group(1)),float(match_rslt.group(2))))
                for hole_line in find_rslt[1:]:
                    find_rslt_line=wkt_find_line.findall(hole_line)
                    hole_data=[]
                    if find_rslt_line:
                        for p in find_rslt_line:
                            match_rslt=re.match('^(\S+) (\S+)$',p)
                            if match_rslt:
                                hole_data.append(PointD(float( match_rslt.group(1)),float(match_rslt.group(2))))
                    holes.append(Polygon(hole_data[:-1]))
            self.data=data[:-1]
            self.holes=holes
        else:
            self.data=Data
            if len(holes) > 0 and not isinstance(holes[0], Polygon):
                holes = [Polygon(part) for part in holes]
            self.holes = holes
        self.RenewBox()


    # 方法
    def IsPointOn(self,point, BufferDist=0):
        """判断点是否在多边形内
            看待测点是否在两点连线之上
            即通过这个点划一条水平射线，看该射线与多边形相交几次
            可以处理平行的情况
        """
        flag = False
        # 先判断是否在多边形外边界内
        if(self._box.IsPointOn(point)):# 先用box判断
            NumOfPointIntersection=0
            for i in range(len(self.data)-1):
                if self.IfHasPoint(point,self.data[i],self.data[i+1]):
                    NumOfPointIntersection+=1
            # 首尾连接线的交点判断
            if self.IfHasPoint(point,self.data[0],self.data[len(self.data)-1]):
                NumOfPointIntersection+=1
            if NumOfPointIntersection%2==1:
                flag = True
                # 判断完外边界，判断内边界
                if self.holes is not None:
                    for hole in self.holes:
                        if hole.IsPointOn(point, BufferDist):
                            flag = False
                            break
        return flag

    def IsIntersectBox(self, box):
        """
        判断矩形是否与多边形相交
        :param box:待判断矩形
        :return:布尔变量
        """
        if not self._box.IsIntersectBox(box):
            return False
        if self._box.MaxX<=box.MaxX and self._box.MaxY<=box.MaxY and self._box.MinX>box.MinX and self._box.MinY>box.MinY:
            return True
        for i in range(len(self.data)):
            if self.data[i].IsIntersectBox(box):return True
        if self.holes is not None:
            for hole in self.holes:
                if not hole.box.IsIntersectBox(box):
                    continue
                for hole_point in hole.data:
                    if hole_point.IsIntersectBox(box):
                        return True
        boxP=[PointD(box.MinX,box.MinY),PointD(box.MinX,box.MaxY),PointD(box.MaxX,box.MinY),PointD(box.MaxX,box.MaxY)]
        for i in range(4):
            if self.IsPointOn(boxP[i]):return True
        # 剩下的可能情形：折线每个端点都不在矩形内，却有可能与矩形相交
        # 这种相交一定会跟矩形的对角线相交
        for i in range(len(self.data) - 1):
            if self.IsLineIntersect(self.data[i], self.data[i + 1],
                                    PointD(box.MinX, box.MinY), PointD(box.MaxX, box.MaxY)) \
                    or self.IsLineIntersect(self.data[i], self.data[i + 1],
                                            PointD(box.MaxX, box.MinY), PointD(box.MinX, box.MaxY)):
                return True
        return False

    def Move(self,deltaX,deltaY):
        for i in range(len(self.data)):
            self.data[i].X+=deltaX
            self.data[i].Y+=deltaY
        if self.holes is not None:
            for hole in self.holes:
                hole.Move(deltaX, deltaY)
        self.RenewBox()

    def MarkPos(self):
        return PointD((self._box.MaxX+self._box.MinX)/2,(self._box.MaxY+self._box.MinY)/2)

    def RenewBox(self):
        if len(self.data) == 0:
            return
        MaxXY = self.FindMaxXY(self.data)
        MinXY = self.FindMinXY(self.data)
        self._box.MaxX = MaxXY.X
        self._box.MaxY = MaxXY.Y
        self._box.MinX = MinXY.X
        self._box.MinY = MinXY.Y

    def GetDistance(self, MouseLocation):pass

    def __str__(self):
        s='Polygon:\n'
        for i in range(len(self.data)):
            s+='Point{}({},{})\n'.format(i+1,self.data[i].X,self.data[i].Y)
        return s

    # 覆盖基类的ToWkt，将几何体转为WKT字符串
    def ToWkt(self):
        wkt=f"POLYGON(({','.join([f'{p.X} {p.Y}' for p in self.data+[self.data[0]]])}){''.join([',({})'.format(','.join([f'{p.X} {p.Y}' for p in hole.data+[hole.data[0]]])) for hole in self.holes])})"
        return wkt
# endregion

# region 子类——多线
class MultiPolyline(Geometry):
    # 属性 data是线构成的List
    def __init__(self, Data, id=-1):
        Geometry.__init__(self, id)
        if type(Data)==str:
            wkt_find=re.compile(r'\([^\(\)\, ]+ [^\(\)\, ]+(?:\,[^\(\)\, ]+ [^\(\)\, ]+)+\)')
            find_rslt=wkt_find.findall(Data)
            data=[]
            if find_rslt:
                for line in find_rslt:
                    data.append(Polyline(line))
            self.data=data
        else:
            self.data=Data
        self.data=Data
        self.RenewBox()

    # 方法
    def IsPointOn(self,point,BufferDist):
        """
        判断点是否在多线的Buffer范围内
        :param point: PointD类型待测点
        :param BufferDist: int类型
        :return: 布尔变量
        """
        result=False
        buffer_box = self._box.Expand(BufferDist)
        if not(buffer_box.IsPointOn(point)):return False
        for i in range(len(self.data)):
            buffer_box = self.data[i].box.Expand(BufferDist)
            if not buffer_box.IsPointOn(point):
                continue
            dis=self.data[i].GetDistance(point)
            if dis<=BufferDist:
                result=True
                break
        return result

    def IsIntersectBox(self, box):
        """
        判断多线上的各点是否在给定box内
        同样，无法判断相交
        :param box: RectangleD类型
        :return:布尔变量
        """
        if not self._box.IsIntersectBox(box):
            return False
        if self._box.MaxX<=box.MaxX and self._box.MaxY<=box.MaxY and self._box.MinX>box.MinX and self._box.MinY>box.MinY:
            return True
        for i in range(len(self.data)):
            if self.data[i].IsIntersectBox(box): return True
        return False

    def Move(self,deltaX,deltaY):
        for i in range(len(self.data)):
            for j in range(len(self.data[i].data)):
                self.data[i].data[j].X+=deltaX
                self.data[i].data[j].Y+=deltaY

    def MarkPos(self):
        return PointD((self._box.MaxX+self._box.MinX)/2,(self._box.MaxY+self._box.MinY)/2)

    def RenewBox(self):
        if len(self.data)==0:
            self._box=RectangleD()
            return
        self.data[0].RenewBox()
        maxX=self.data[0]._box.MaxX
        maxY=self.data[0]._box.MaxY
        minX=self.data[0]._box.MinX
        minY=self.data[0]._box.MinY
        for i in range(1,len(self.data)):
            self.data[i].RenewBox()
            if self.data[i]._box.MaxX>maxX:maxX=self.data[i]._box.MaxX
            if self.data[i]._box.MaxY > maxY: maxY = self.data[i]._box.MaxY
            if self.data[i]._box.MinX < minX: minX = self.data[i]._box.MinX
            if self.data[i]._box.MinY < minY: minY = self.data[i]._box.MinY
        self._box.MinX=minX
        self._box.MinY=minY
        self._box.MaxX=maxX
        self._box.MaxY=maxY

    def GetDistance(self, MouseLocation):
        pass

    def __str__(self):
        s=''
        for i in range(len(self.data)):
            s+='Polyline {}:\n'.format(i+1)
            for j in range(len(self.data[i].data)):
                s+='Point{}({},{})\n'.format(j+1,self.data[i].data[j].X,self.data[i].data[j].Y)
        return s

    def ToWkt(self):
        wkt=f"MULTILINESTRING({','.join([l.ToWkt()[10:] for l in self.data])})"
        return wkt
# endregion

# region 子类——多多边形
class MultiPolygon(Geometry):
    # 属性 data是面构成的List
    def __init__(self,Data,id=-1):
        Geometry.__init__(self,id)
        if type(Data)==str:
            wkt_find=re.compile(r'\(\([^\(\)\, ]+ [^\(\)\, ]+(?:\,[^\(\)\, ]+ [^\(\)\, ]+)+\)(?:\,\([^\(\)\, ]+ [^\(\)\, ]+(?:\,[^\(\)\, ]+ [^\(\)\, ]+)+\))*\)')
            find_rslt=wkt_find.findall(Data)
            data=[]
            if find_rslt:
                for pg in find_rslt:
                    data.append(Polygon(pg))
            self.data=data
        else:
            self.data=Data
        self.RenewBox()

    # 方法
    def IsPointOn(self,point, BufferDist=0):
        result=False
        if not(self._box.IsPointOn(point)):return False
        for i in range(len(self.data)):
            if self.data[i].IsPointOn(point):
                result=True
                break
        return result

    def IsIntersectBox(self, box):
        """
        判断矩形是否与多边形相交
        :param box:待判断矩形
        :return:布尔变量
        """
        if not self._box.IsIntersectBox(box):
            return False
        if self._box.MaxX<=box.MaxX and self._box.MaxY<=box.MaxY and self._box.MinX>box.MinX and self._box.MinY>box.MinY:
            return True
        for i in range(len(self.data)):
            if self.data[i].IsIntersectBox(box):return True
        return False

    def Move(self,deltaX,deltaY):
        for i in range(len(self.data)):
            for j in range(len(self.data[i].data)):
                self.data[i].data[j].X+=deltaX
                self.data[i].data[j].Y+=deltaY

    def MarkPos(self):
        return PointD((self._box.MaxX+self._box.MinX)/2,(self._box.MaxY+self._box.MinY)/2)

    def RenewBox(self):
        if len(self.data)==0:
            self._box=RectangleD()
            return
        self.data[0].RenewBox()
        maxX=self.data[0]._box.MaxX
        maxY=self.data[0]._box.MaxY
        minX=self.data[0]._box.MinX
        minY=self.data[0]._box.MinY
        for i in range(1,len(self.data)):
            self.data[i].RenewBox()
            if self.data[i]._box.MaxX>maxX:maxX=self.data[i]._box.MaxX
            if self.data[i]._box.MaxY > maxY: maxY = self.data[i]._box.MaxY
            if self.data[i]._box.MinX < minX: minX = self.data[i]._box.MinX
            if self.data[i]._box.MinY < minY: minY = self.data[i]._box.MinY
        self._box.MinX=minX
        self._box.MinY=minY
        self._box.MaxX=maxX
        self._box.MaxY=maxY

    def GetDistance(self, MouseLocation):
        pass

    def __str__(self):
        s = ''
        for i in range(len(self.data)):
            s += 'Polygon {}:\n'.format(i + 1)
            for j in range(len(self.data[i].data)):
                s += 'Point{}({},{})\n'.format(j + 1, self.data[i].data[j].X, self.data[i].data[j].Y)
        return s

    # 覆盖基类的ToWkt，将几何体转为WKT字符串
    def ToWkt(self):
        wkt=f"MULTIPOLYGON({','.join([pg.ToWkt()[7:] for pg in self.data])})"
        return wkt

if __name__=='__main__':
    # pg=Polygon([PointD(1,1),PointD(1,2),PointD(1,3),PointD(1,1)],[Polygon([PointD(1,1),PointD(1,2),PointD(1,3),PointD(1,1)])])
    # mpg=MultiPolygon([pg,pg])
    # print(mpg.ToWkt())
    pt=PointD('POINT(1 2)')
    pl=Polyline('LINESTRING(1.2 -1,2 2,3 3,)')
    pd=MultiPolygon('MULTIPOLYGON(((1.2 -1,2 2,3 3,1.2 -1)),((1.2 -1,2 2,3 3,1.2 -1)))')
    print(pd)