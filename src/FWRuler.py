#!@PYTHON@
"""
Class :py:class:`FWRuler` adds a ruller to one of the sides of the scene rectangle
==================================================================================

Usage ::

    rs = QtCore.QRectF(0, 0, 1, 1)
    s = QtGui.QGraphicsScene(rs)
    v = QtGui.QGraphicsView(s)
    v.setGeometry(20, 20, 600, 400)

    v.fitInView(rs, Qt.IgnoreAspectRatio) # Qt.IgnoreAspectRatio Qt.KeepAspectRatioByExpanding Qt.KeepAspectRatio

    ruler1 = FWRuler(s, 'L')
    ruler2 = FWRuler(s, 'D')
    ruler3 = FWRuler(s, 'U')
    ruler4 = FWRuler(s, 'R')

    ruler1.remove()
    
    ruler4.remove()

Created on December 12, 2017 by Mikhail Dubrovin
"""

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QPointF

from graphqt.AxisLabeling import best_label_locs

class FWRuler() :
    def __init__(self, scene, orient='U', **kwargs) :

        self.scene  = scene
        self.orient = orient
        self.horiz  = orient in ('D','U')

        self.font        = kwargs.get('font',  QtGui.QFont('Courier', 12, QtGui.QFont.Normal))
        self.pen         = kwargs.get('pen',   QtGui.QPen(Qt.black, 1, Qt.SolidLine))
        self.brush       = kwargs.get('brush', QtGui.QBrush(Qt.red))
        self.color       = kwargs.get('color', QtGui.QColor(Qt.red))
        self.tick_fr     = kwargs.get('tick_fr', 0.015)
        self.txtoff_vfr  = kwargs.get('txtoff_vfr',  0)
        self.txtoff_hfr  = kwargs.get('txtoff_hfr',  0)
        self.size_inches = kwargs.get('size_inches', 3)
        self.zvalue      = kwargs.get('zvalue',     10)
        self.fmt         = kwargs.get('fmt',      '%g')

        #QtGui.QPainterPath.__init__(self)
   
        self.pen.setCosmetic(True)
        self.pen.setColor(self.color)

        self.path = None
        self.path_item = None

        r = self.rect=self.scene.sceneRect()
        vmin = r.x() if self.horiz else r.y()
        vmax = r.x()+r.width() if self.horiz else r.y()+r.height()
        self.labels = best_label_locs(vmin, vmax, self.size_inches, density=1, steps=None)

        #print 'labels', self.labels

        self.set_pars()
        self.add()


    def set_pars(self) :

        r = self.rect
        w,h = r.width(), r.height()
        self.hoff = -0.01*w # label offset for each character 

        if self.orient == 'U' :
            self.p1   = r.topLeft()
            self.p2   = r.topRight()
            self.dt1  = QPointF(0, self.tick_fr * h)
            self.dtxt = QPointF(-0.005*w, 0.01*h)
            self.vort = self.p1.y()
 
        elif self.orient == 'L' :
            self.p1   = r.topLeft()
            self.p2   = r.bottomLeft()
            self.dt1  = QPointF(self.tick_fr * w, 0)
            self.dtxt = QPointF(0.01*w,-0.025*h)
            self.vort = self.p1.x()
            self.hoff = 0 # 0.01*w

        elif self.orient == 'R' : 
            self.p1   = r.topRight()
            self.p2   = r.bottomRight()
            self.dt1  = QPointF(-self.tick_fr * w, 0)
            self.dtxt = QPointF(-0.03*w,-0.025*h)
            self.vort = self.p2.x() # x + w

        elif self.orient == 'D' :
            self.p1   = r.bottomLeft()
            self.p2   = r.bottomRight()
            self.dt1  = QPointF(0, -self.tick_fr * h)
            self.dtxt = QPointF(-0.005*w, -0.05*h)
            self.vort = self.p2.y() # y + h
            #print 'p1,p2, dt1, dtxt, vort', self.p1, self.p2, self.dt1, self.dtxt, self.vort

        else :
            print 'ERROR: non-defined axis orientation "%s". Use L, R, U, or D.' % str(self.orient)


    def add(self) :
        # add ruller to the path of the scene
        if self.path_item is not None : self.scene.removeItem(self.path_item)

        self.path = QtGui.QPainterPath(self.p1)
        #self.path.closeSubpath()
        self.path.moveTo(self.p1)
        self.path.lineTo(self.p2)

        #print 'self.p1', self.p1
        #print 'self.p2', self.p2

        for v in self.labels :
            pv = QPointF(v, self.vort) if self.horiz else QPointF(self.vort, v)
            self.path.moveTo(pv)
            self.path.lineTo(pv+self.dt1)

        # add path with ruler lines to scene

        self.lst_of_items=[]

        self.path_item = self.scene.addPath(self.path, self.pen, self.brush)
        self.path_item.setZValue(self.zvalue)
        self.lst_of_items.append(self.path_item)

        #print 'path_item is created'

        r = self.rect
        w,h = r.width(), r.height()
        # add labels to scene 
        for v in self.labels :
            pv = QPointF(v, self.vort) if self.horiz else QPointF(self.vort, v)
            vstr = self.fmt%v
            pt = pv + self.dtxt + QPointF(self.hoff*len(vstr),0)\
                 + QPointF(self.txtoff_hfr*h, self.txtoff_vfr*h)
            txtitem = self.scene.addText(vstr, self.font)
            txtitem.setDefaultTextColor(self.color)
            txtitem.moveBy(pt.x(), pt.y())
            txtitem.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations, True)
            txtitem.setZValue(self.zvalue)

            self.lst_of_items.append(txtitem)       

        #self.item_group = self.scene.createItemGroup(self.lst_of_items)

    def remove(self) :
        for item in self.lst_of_items :
            self.scene.removeItem(item)
        self.lst_of_items=[]

        #self.scene.removeItem(self.path_item)
        #self.scene.destroyItemGroup(self.item_group)


    def update(self) :
        self.remove()
        self.set_pars()
        self.add()


    def __del__(self) :
        self.remove()

#-----------------------------
if __name__ == "__main__" :

    import sys

    app = QtGui.QApplication(sys.argv)
    rs = QtCore.QRectF(0, 0, 100, 100)
    ro = QtCore.QRectF(-1, -1, 3, 2)
    s = QtGui.QGraphicsScene(rs)
    w = QtGui.QGraphicsView(s)
    w.setGeometry(20, 20, 600, 600)

    print 'screenGeometry():', app.desktop().screenGeometry()
    print 'scene rect=', s.sceneRect()

    w.fitInView(rs, Qt.KeepAspectRatio) # Qt.IgnoreAspectRatio Qt.KeepAspectRatioByExpanding Qt.KeepAspectRatio

    s.addRect(rs, pen=QtGui.QPen(Qt.black, 0, Qt.SolidLine), brush=QtGui.QBrush(Qt.yellow))
    s.addRect(ro, pen=QtGui.QPen(Qt.black, 0, Qt.SolidLine), brush=QtGui.QBrush(Qt.red))

    ruler1 = FWRuler(s, 'L')
    ruler2 = FWRuler(s, 'D')
    ruler3 = FWRuler(s, 'U')
    ruler4 = FWRuler(s, 'R')

    w.setWindowTitle("My window")
    w.setContentsMargins(-9,-9,-9,-9)
    w.show()
    app.exec_()

    #s.clear()

    ruler1.remove()
    ruler2.remove()
    ruler3.remove()
    ruler4.remove()

#-----------------------------
