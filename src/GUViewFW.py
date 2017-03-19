#!@PYTHON@
"""
Created on January 3, 2017

@author: Mikhail Dubrovin

Class GUViewFW is a QGraphicsView / QWidget with interactive scalable scene with axes.
FW stands for Full Window - no margins for axes

Usage ::

    import sys
    from PyQt4 import QtGui, QtCore
    from graphqt.GUViewFW import GUViewFW

    app = QtGui.QApplication(sys.argv)
    w = GUViewFW(None, raxes=QtCore.QRectF(0, 0, 100, 100), origin='UL', scale_ctl='HV')
    w.show()
    app.exec_()
"""

from math import floor
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class GUViewFW(QtGui.QGraphicsView) :
    
    def __init__(self, parent=None, rectax=QtCore.QRectF(0, 0, 10, 10), origin='UL', scale_ctl='HV', show_mode=0) :

        self._name = self.__class__.__name__

        self.raxes = rectax
        self.set_origin(origin)
        self.set_scale_control(scale_ctl)

        sc = QtGui.QGraphicsScene() # rectax
        #print 'scene rect=', sc.sceneRect()        
        #print 'rect img=', self.rectax

        QtGui.QGraphicsView.__init__(self, sc, parent)
        
        self.set_style()
        self.set_view()
        colfld = Qt.magenta
        colori = Qt.red
        #pen=QtGui.QPen(colfld, 0, Qt.SolidLine)

        if show_mode & 1 :
            self.raxi = self.add_rect_to_scene_v1(self.raxes, pen=QtGui.QPen(Qt.NoPen), brush=QtGui.QBrush(colfld))

        if show_mode & 2 :
            ror=QtCore.QRectF(-1, -1, 2, 2)
            self.rori = self.add_rect_to_scene(ror, pen=QtGui.QPen(colori, 0, Qt.SolidLine), brush=QtGui.QBrush(colori))

        if not self._origin_ul :
            t = self.transform()
            sx = 1 if self._origin_l else -1
            sy = 1 if self._origin_u else -1
            t2 = t.scale(sx, sy)
            self.setTransform(t2)

        self.raxesi = None
        self.pos_click = None
        self.scalebw = 3

        self.update_my_scene()
        

    def set_origin(self, origin='UL') :
        self._origin = origin
        key = origin.upper()

        self._origin_u = 'U' in key or 'T' in key
        self._origin_d = not self._origin_u

        self._origin_l = 'L' in key 
        self._origin_r = not self._origin_l

        self._origin_ul = self._origin_u and self._origin_l
        self._origin_ur = self._origin_u and self._origin_r
        self._origin_dl = self._origin_d and self._origin_l
        self._origin_dr = self._origin_d and self._origin_r


    def set_scale_control(self, scale_ctl='HV') :
        """Sets scale control bit-word
           = 0 - x, y frozen scales
           + 1 - x is interactive
           + 2 - y is interactive
           bit value 0/1 frozen/interactive  
        """
        self._scale_ctl = 0
        if 'H' in scale_ctl : self._scale_ctl += 1
        if 'V' in scale_ctl : self._scale_ctl += 2
 
    def scale_control(self) :
        return self._scale_ctl


    def set_style(self) :
        self.setGeometry(20, 20, 600, 600)
        self.setWindowTitle("GUViewFW window")
        #self.setContentsMargins(-9,-9,-9,-9)
        self.setStyleSheet("background-color:black; border: 0px solid green")
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setInteractive(True)
        #self.setFixedSize(600, 22)

        self.brudf = QtGui.QBrush()
        self.brubx = QtGui.QBrush(Qt.black, Qt.SolidPattern)

        self.pendf = QtGui.QPen()
        self.pendf.setStyle(Qt.NoPen)
        self.penbx = QtGui.QPen(Qt.black, 6, Qt.SolidLine)


    def set_view(self) :
        rs = self.raxes
        self.scene().setSceneRect(rs)
        self.fitInView(rs, Qt.IgnoreAspectRatio) # Qt.IgnoreAspectRatio Qt.KeepAspectRatioByExpanding Qt.KeepAspectRatio


    def update_my_scene(self) :
        sc = self.scene()
        rs = sc.sceneRect()
        x, y, w, h = rs.x(), rs.y(), rs.width(), rs.height()

        x1ax, x2ax = x, x + w
        y1ax, y2ax = y, y + h
        wax = x2ax - x1ax
        hax = y2ax - y1ax

        if self.raxesi is not None : self.scene().removeItem(self.raxesi)

        self.rectax = QtCore.QRectF(x1ax, y,    wax, hax) if self._origin_ul else\
                      QtCore.QRectF(x1ax, y1ax, wax, hax).normalized()

        self.raxesi = self.add_rect_to_scene(self.rectax, self.brudf, self.pendf)
        self.raxesi.setCursorHover(Qt.CrossCursor)
        self.raxesi.setCursorGrab (Qt.SizeAllCursor)
        self.raxesi.setZValue(20)


    def remove(self) :
        #remove ruler lines
        #self.scene.removeItem(self.path_item)
        #remove labels
        #for item in self.lst_txtitems :
        #    self.scene.removeItem(item)
        #self.textitems=[]
        pass


#    def update(self) :
#        print 'update signal is received'
#        self.update_my_scene()


    def __del__(self) :
        self.remove()


    def mouseReleaseEvent(self, e):
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QGraphicsView.mouseReleaseEvent(self, e)
        #print 'GUViewFW.mouseReleaseEvent, at point: ', e.pos(), ' diff:', e.pos() - self.pos_click
        #self.pos_click = e.pos()
        self.pos_click = None


#    def mouseDoubleCkickEvent(self, e):
#        QtGui.QGraphicsView.mouseDoubleCkickEvent(self, e)
#        print 'mouseDoubleCkickEvent'


    def mousePressEvent(self, e):
        #print 'GUViewFW.mousePressEvent, at point: ', e.pos() #e.globalX(), e.globalY() 
        #QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.SizeAllCursor))# ClosedHandCursor
        QtGui.QGraphicsView.mousePressEvent(self, e)

        self.pos_click = e.pos()
        #self.pos_click_sc = self.mapToScene(self.pos_click)
        self.rs_center = self.scene().sceneRect().center()
        self.invscalex = 1./self.transform().m11()
        self.invscaley = 1./self.transform().m22()

        self.selectFurtherAction(e)

        
    def selectFurtherAction(self, e):
        if self._scale_ctl != 3 :
            self.scalebw = self._scale_ctl
            return

        pos_on_sc = self.mapToScene(e.pos())
        item = self.scene().itemAt(pos_on_sc)

        self.scalebw = 3

        #elif item == self.raxesi   : self.scalebw = 3 # print 'axes rect'
        #print 'selectFurtherAction scalebw:', self.scalebw


    def display_pixel_pos(self, e):
        p = self.mapToScene(e.pos())
        #print 'mouseMoveEvent, current point: ', e.x(), e.y(), ' on scene: %.1f  %.1f' % (p.x(), p.y()) 
        self.setWindowTitle('GUViewFW: x=%.1f y=%.1f' % (p.x(), p.y()))


    def mouseMoveEvent(self, e):
        QtGui.QGraphicsView.mouseMoveEvent(self, e)
        #print 'GUViewFW.mouseMoveEvent, at point: ', e.pos()
        self.display_pixel_pos(e)

        if self._scale_ctl==0 : return

        if self.pos_click is None : return        

        dp = e.pos() - self.pos_click
        #print 'mouseMoveEvent, at point: ', e.pos(), ' diff:', dp
        
        dx = dp.x()*self.invscalex if self.scalebw & 1 else 0
        dy = dp.y()*self.invscaley if self.scalebw & 2 else 0
        dpsc = QtCore.QPointF(dx, dy)

        sc = self.scene()
        rs = sc.sceneRect()
        rs.moveCenter(self.rs_center - dpsc)
        sc.setSceneRect(rs)

        self.update_my_scene()


    def wheelEvent(self, e) :
        QtGui.QGraphicsView.wheelEvent(self, e)

        if self._scale_ctl==0 : return

        self.selectFurtherAction(e)

        #print 'wheelEvent: ', e.delta()
        f = 1 + 0.4 * (1 if e.delta()>0 else -1)
        #print 'Scale factor =', f

        p = self.mapToScene(e.pos())
        px, py = p.x(), p.y() 
        #print 'wheel x,y = ', e.x(), e.y(), ' on scene x,y =', p.x(), p.y() 
        #rectax = self.rectax

        sc = self.scene()
        rs = sc.sceneRect()
        x,y,w,h = rs.x(), rs.y(), rs.width(), rs.height()
        #print 'Scene x,y,w,h:', x,y,w,h

        # zoom relative to axes center
        #dxc = (f-1)*0.55*w 
        #dyc = (f-1)*0.45*h

        # zoom relative to mouse position
        dxc = (f-1)*(px-x)
        dyc = (f-1)*(py-y) 
        dx, sx = (dxc, f*w) if self.scalebw & 1 else (0, w)
        dy, sy = (dyc, f*h) if self.scalebw & 2 else (0, h)

        rs.setRect(x-dx, y-dy, sx, sy)      
        sc.setSceneRect(rs)

        #self.update_transform()
        #sc.update()
        #rs = self.scene().sceneRect()    
        self.fitInView(rs, Qt.IgnoreAspectRatio)
        self.update_my_scene()

        #self.scalebw = 3


    def enterEvent(self, e) :
    #    print 'enterEvent'
        QtGui.QGraphicsView.enterEvent(self, e)
        #QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.CrossCursor))
        

    def leaveEvent(self, e) :
    #    print 'leaveEvent'
        QtGui.QGraphicsView.leaveEvent(self, e)
        #QtGui.QApplication.restoreOverrideCursor()


    def closeEvent(self, e) :
        #print 'GUViewFW.closeEvent' # % self._name
        QtGui.QGraphicsView.closeEvent(self, e)
        

    #def moveEvent(self, e) :
    #    print 'moveEvent'
    #    print 'Geometry rect:', self.geometry()


    def resizeEvent(self, e) :
         QtGui.QGraphicsView.resizeEvent(self, e)
         #print 'resizeEvent'
         #print 'Geometry rect:', self.geometry()
         rs = self.scene().sceneRect()    
         #print 'Rect of the scene =', rs
         self.fitInView(rs, Qt.IgnoreAspectRatio)


    #def paintEvent(e):
    #    pass


    def keyPressEvent(self, e) :
        #print 'keyPressEvent, key=', e.key()         
        if   e.key() == Qt.Key_Escape :
            self.close()

        elif e.key() == Qt.Key_R : 
            print 'Reset original size'
            self.set_view()
            self.update_my_scene()


    def add_rect_to_scene_v1(self, rect, brush=QtGui.QBrush(), pen=QtGui.QPen(Qt.yellow, 4, Qt.DashLine)) :
        """Adds rect to scene, returns QGraphicsRectItem"""
        pen.setCosmetic(True)
        return self.scene().addRect(rect, pen, brush)


    def add_rect_to_scene(self, rect, brush=QtGui.QBrush(), pen=QtGui.QPen(Qt.yellow, 4, Qt.DashLine)) :
        """Adds rect to scene, returns GUQGraphicsRectItem - for interactive stuff"""
        from graphqt.GUQGraphicsRectItem import GUQGraphicsRectItem
        pen.setCosmetic(True)
        item = GUQGraphicsRectItem(rect, parent=None, scene=self.scene())
        item.setPen(pen)
        item.setBrush(brush)
        return item

#-----------------------------

def test_guiviewfw(tname) :
    print '%s:' % sys._getframe().f_code.co_name

    app = QtGui.QApplication(sys.argv)
    w = None
    if   tname == '0': w=GUViewFW(None, rectax=QtCore.QRectF(0, 0, 100, 100), origin='DL', show_mode=3, scale_ctl='HV')
    elif tname == '1': w=GUViewFW(None, rectax=QtCore.QRectF(0, 0, 100, 100), origin='DL', show_mode=3, scale_ctl='')
    elif tname == '2': w=GUViewFW(None, rectax=QtCore.QRectF(0, 0, 100, 100), origin='DL', show_mode=3, scale_ctl='H')
    elif tname == '3': w=GUViewFW(None, rectax=QtCore.QRectF(0, 0, 100, 100), origin='DL', show_mode=3, scale_ctl='V')
    elif tname == '4': w=GUViewFW(None, rectax=QtCore.QRectF(0, 0, 100, 100), origin='DL', show_mode=1, scale_ctl='HV')
    else :
        print 'test %s is not implemented' % tname
        return
    w.show()
    app.exec_()

#------------------------------

if __name__ == "__main__" :
    import sys; global sys
    import numpy as np; global np
    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print 50*'_', '\nTest %s' % tname
    test_guiviewfw(tname)
    sys.exit('End of Test %s' % tname)

#------------------------------

