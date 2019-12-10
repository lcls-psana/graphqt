#!@PYTHON@
"""
Class :py:class:`test-QGraphicsView` - test for QGraphicsView geometry
==================================================================================

Usage ::

    python graphqt/src/test-QGraphicsView.py

Created on December 12, 2017 by Mikhail Dubrovin
"""
from __future__ import print_function

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QPointF
from PyQt4.QtGui import QGraphicsView

#-----------------------------

class MyQGraphicsView(QGraphicsView) :

   def __init__(self, parent=None) : 
       QGraphicsView.__init__(self, parent)

   def mousePressEvent(self, e):
       self.p0 = pw = e.pos()
       self.r0 = self.sceneRect() #.center()
       ps = self.mapToScene(pw)
       print('XXX: MyQGraphicsView.mousPressEvent in win: %4d %4d on scene: %.1f %.1f'%\
              (pw.x(), pw.y(), ps.x(), ps.y()))

   def mouseMoveEvent(self, e):
       dp = self.mapToScene(e.pos() - self.p0)
       r = QtCore.QRectF(self.r0)
       r.moveCenter(r.center() - dp)
       self.setSceneRect(r)

   def moveEvent(self, e):
       print('XXX: MyQGraphicsView.moveEvent topLeft:', self.geometry().topLeft())

   def resizeEvent(self, e):
       print('XXX: MyQGraphicsView.resizeEvent size:', self.geometry().size())
       s = self.scene()
       rs = self.sceneRect()

       mx,my = 100,50 # 0,0
       x, y, w, h = rs.getRect()
       rv = QtCore.QRectF(x-mx, y-my, w+2*mx, h+2*my)

       self.fitInView(rv, Qt.IgnoreAspectRatio) # Qt.IgnoreAspectRatio KeepAspectRatio KeepAspectRatioByExpanding
       #self.ensureVisible(rv, xMargin=0, yMargin=0)

#-----------------------------
if __name__ == "__main__" :

    import sys

    app = QtGui.QApplication(sys.argv)
    rs = QtCore.QRectF(0, 0, 1500, 1500)
    ro = QtCore.QRectF(-2, -2, 10, 4)
    re = QtCore.QRectF(640-2, 480-2, 4, 4)

    s = QtGui.QGraphicsScene(rs)
    w = MyQGraphicsView(s)
    w.setGeometry(20, 20, 700, 700)
    #w.setGeometry(20, 20, 800, 800)

    # Invert x,y scales
    sx, sy = -1, -1
    t2 = w.transform().scale(sx, sy)
    #t2 = w.transform().rotate(5)
    w.setTransform(t2)

    print('screenGeometry():', app.desktop().screenGeometry())
    print('geometry():', w.geometry())
    print('scene rect=', s.sceneRect())

    irs = s.addRect(rs, pen=QtGui.QPen(Qt.black, 0, Qt.SolidLine), brush=QtGui.QBrush(Qt.yellow))
    iro = s.addRect(ro, pen=QtGui.QPen(Qt.black, 0, Qt.SolidLine), brush=QtGui.QBrush(Qt.red))
    ire = s.addRect(re, pen=QtGui.QPen(Qt.black, 0, Qt.SolidLine), brush=QtGui.QBrush(Qt.green))

    w.setWindowTitle("My window")
    #w.setContentsMargins(-9,-9,-9,-9)
    print('Before w.show()')
    w.show()
    print('Before app.exec_()')
    app.exec_()
    print('E')
    #s.clear()
    #s.clear()
    s.removeItem(irs)
    s.removeItem(iro)
    s.removeItem(ire)

#-----------------------------
