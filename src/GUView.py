#!@PYTHON@
"""
Created on September 9, 2016

@author: Mikhail Dubrovin

Class GUView is a QGraphicsView / QWidget with interactive scalable scene with axes.

Usage ::

    Emits signals
    -------------
    self.connect_wheel_is_stopped_to(recipient)
    self.connect_axes_limits_changed_to(recipient)

    import sys
    from PyQt4 import QtGui, QtCore
    from graphqt.GUView import GUView

    app = QtGui.QApplication(sys.argv)
    w = GUView(None, raxes=QtCore.QRectF(0, 0, 100, 100), origin='UL',\
               scale_ctl='HV', margl=0.12, margr=0.10, margt=0.06, margb=0.06)
    w.show()
    app.exec_()
"""
#------------------------------

from math import floor
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

#------------------------------

def print_rect(r, cmt='') :
    x, y, w, h = r.x(), r.y(), r.width(), r.height()
    print '%s x=%8.2f  y=%8.2f  w=%8.2f  h=%8.2f' % (cmt, x, y, w, h)

#------------------------------

class GUView(QtGui.QGraphicsView) :
    
    def __init__(self, parent=None, rectax=QtCore.QRectF(0, 0, 10, 10), origin='UL', scale_ctl='HV',\
                 margl=None, margr=None, margt=None, margb=None, show_mode=0) :

        self._name = self.__class__.__name__
        #self.rectax = rectax
        self.raxes = rectax
        self.show_mode = show_mode
        self.set_origin(origin)
        self.set_scale_control(scale_ctl)

        sc = QtGui.QGraphicsScene() # rectax
        #print 'scene rect=', sc.sceneRect()        
        #print 'rect img=', self.rectax

        QtGui.QGraphicsView.__init__(self, sc, parent)
        
        self.set_style()
        self.set_margins(margl, margr, margt, margb)
        self.set_view()

        #pen=QtGui.QPen(colfld, 0, Qt.SolidLine)

        if not self._origin_ul :
            t = self.transform()
            sx = 1 if self._origin_l else -1
            sy = 1 if self._origin_u else -1
            t2 = t.scale(sx, sy)
            self.setTransform(t2)

        self.rslefv = None
        self.rsbotv = None
        self.rsrigv = None
        self.rstopv = None

        self.rslefi = None
        self.rsboti = None
        self.rsrigi = None
        self.rstopi = None

        self.raxesv = None
        self.raxesi = None
        self.pos_click = None
        self.scalebw = 3

        self._xmin = None
        self._xmax = None
        self._ymin = None
        self._ymax = None

        self._x1_old = None
        self._x2_old = None
        self._y1_old = None
        self._y2_old = None

        self.update_my_scene()
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.on_timeout)

        #self.connect_wheel_is_stopped_to(self.check_axes_limits)
        #self.disconnect_wheel_is_stopped_from(self.check_axes_limits)
        
        #self.connect_axes_limits_changed_to(self.test_axes_limits_changed_reception)
        #self.disconnect_axes_limits_changed_from(self.test_axes_limits_changed_reception)


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
        self.setWindowTitle("GUView window")
        self.setStyleSheet("background-color:black; border: 0px solid green")
        #w.setContentsMargins(-9,-9,-9,-9)
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground) # Qt.WA_NoSystemBackground
        #self.setInteractive(True)

        self.brudf = QtGui.QBrush()
        self.brubx = QtGui.QBrush(Qt.black, Qt.SolidPattern)

        self.pendf = QtGui.QPen()
        self.pendf.setStyle(Qt.NoPen)
        self.penbx = QtGui.QPen(Qt.black, 6, Qt.SolidLine)
        self.pen_gr=QtGui.QPen(Qt.green, 0, Qt.SolidLine)
        self.pen_bl=QtGui.QPen(Qt.blue, 0, Qt.SolidLine)



    def set_margins(self, margl=None, margr=None, margt=None, margb=None) :
        """Sets margins around axes rect to expend viewed scene"""
        self.margl = margl if margl is not None else 0.12
        self.margr = margr if margr is not None else 0.03
        self.margt = margt if margt is not None else 0.01
        self.margb = margb if margb is not None else 0.06


    def set_view(self) :
        # Sets scene rect larger than axes rect by margins
        ml, mr, mt, mb = self.margl, self.margr, self.margt, self.margb

        r = self.raxes
        #print_rect(r, cmt='XXX rect axes')
        
        x, y, w, h = r.x(), r.y(), r.width(), r.height()
        sx = w/(1. - ml - mr)
        sy = h/(1. - mt - mb)

        my = mt if self._origin_u else mb
        mx = ml if self._origin_l else mr
        rs = QtCore.QRectF(x-mx*sx, y-my*sy, sx, sy)

        #print_rect(rs, cmt='XXX rect scene')

        self.scene().setSceneRect(rs)
        self.fitInView(rs, Qt.IgnoreAspectRatio) # Qt.IgnoreAspectRatio Qt.KeepAspectRatioByExpanding Qt.KeepAspectRatio


    def check_limits(self) :

        if all(v is None for v in (self._xmin, self._xmax, self._ymin, self._ymax)) : return  
        
        sc = self.scene()
        rs = sc.sceneRect()
        x, y, w, h = rs.x(), rs.y(), rs.width(), rs.height()

        x1 = x   if self._xmin is None else self._xmin
        x2 = x+w if self._xmax is None else self._xmax
        y1 = y   if self._ymin is None else self._ymin
        y2 = y+h if self._ymax is None else self._ymax

        rs = QtCore.QRectF(x1, y1, x2-x1, y2-y1)
        sc.setSceneRect(rs)
        self.fitInView(rs, Qt.IgnoreAspectRatio)


    def update_my_scene(self) :
        #print 'In GUIView.update_my_scene'
        self.check_limits()

        sc = self.scene()
        rs = sc.sceneRect()
        x, y, w, h = rs.x(), rs.y(), rs.width(), rs.height()
        #print_rect(rs, cmt='XXX scene rect')

        x1ax, x2ax = x + w*self.margl, x + w - w*self.margr
        y1ax, y2ax = y + h*self.margb, y + h - h*self.margt

        wax = x2ax - x1ax
        hax = y2ax - y1ax

        # set dark rects
        if self.rslefv is not None : self.scene().removeItem(self.rslefv)
        if self.rsbotv is not None : self.scene().removeItem(self.rsbotv)
        if self.rsrigv is not None : self.scene().removeItem(self.rsrigv)
        if self.rstopv is not None : self.scene().removeItem(self.rstopv)

        # set interactive rects
        if self.rslefi is not None : self.scene().removeItem(self.rslefi)
        if self.rsboti is not None : self.scene().removeItem(self.rsboti)
        if self.rsrigi is not None : self.scene().removeItem(self.rsrigi)
        if self.rstopi is not None : self.scene().removeItem(self.rstopi)

        if self.raxesv is not None : self.scene().removeItem(self.raxesv)
        if self.raxesi is not None : self.scene().removeItem(self.raxesi)

        if self._origin_l :            
            #print 'L'
            self.rslef=QtCore.QRectF(x,    y, w*self.margl, h)
            self.rsrig=QtCore.QRectF(x2ax, y, w*self.margr, h)
        else :
            #print 'R'
            self.rslef=QtCore.QRectF(x,    y, w*self.margr, h)
            self.rsrig=QtCore.QRectF(x + w - w*self.margl, y, w*self.margl, h)

        self.rslefv = self.add_rect_to_scene_v1(self.rslef, self.brubx, self.penbx)
        self.rslefi = self.add_rect_to_scene(self.rslef, self.brudf, self.pendf)
        self.rslefi.setCursorHover(Qt.SizeVerCursor)
        self.rslefi.setCursorGrab (Qt.SplitVCursor)

        self.rsrigv = self.add_rect_to_scene_v1(self.rsrig, self.brubx, self.penbx)
        self.rsrigi = self.add_rect_to_scene(self.rsrig, self.brudf, self.pendf)
        self.rsrigi.setCursorHover(Qt.SizeVerCursor)
        self.rsrigi.setCursorGrab (Qt.SplitVCursor)

        if self._origin_ul :            
            #print 'UL'
            self.rstop  = QtCore.QRectF(x1ax, y + h - h*self.margb, wax, h*self.margb)
            self.rsbot  = QtCore.QRectF(x1ax, y, wax, h*self.margt)
            self.rectax = QtCore.QRectF(x1ax, y + h*self.margt, wax, hax)

        elif self._origin_dl :
            #print 'DL'
            self.rsbot  = QtCore.QRectF(x1ax, y,    wax, h*self.margb) #.normalized()
            self.rstop  = QtCore.QRectF(x1ax, y2ax, wax, h*self.margt) #.normalized()
            self.rectax = QtCore.QRectF(x1ax, y1ax, wax, hax) #.normalized()

        elif self._origin_dr : 
            #print 'DR'
            x1ax = x + w*self.margr
            self.rsbot  = QtCore.QRectF(x1ax, y,    wax, h*self.margb) #.normalized()
            self.rstop  = QtCore.QRectF(x1ax, y2ax, wax, h*self.margt) #.normalized()
            self.rectax = QtCore.QRectF(x1ax, y1ax, wax, hax) #.normalized()

        else : #self._origin_ur : 
            #print 'UR'
            x1ax = x + w*self.margr
            y1ax = y + h - h*self.margb
            self.rsbot  = QtCore.QRectF(x1ax, y,    wax, h*self.margt) #.normalized()
            self.rstop  = QtCore.QRectF(x1ax, y1ax, wax, h*self.margb) #.normalized()
            self.rectax = QtCore.QRectF(x1ax, y + h*self.margt, wax, hax)

        self.rsbotv = self.add_rect_to_scene_v1(self.rsbot, self.brubx, self.penbx)
        self.rsboti = self.add_rect_to_scene   (self.rsbot, self.brudf, self.pendf)

        self.rstopv = self.add_rect_to_scene_v1(self.rstop, self.brubx, self.penbx)
        self.rstopi = self.add_rect_to_scene   (self.rstop, self.brudf, self.pendf)

        self.raxesv = self.add_rect_to_scene_v1(self.rectax, self.brubx, self.penbx)
        self.raxesi = self.add_rect_to_scene   (self.rectax, self.brudf, self.pendf) # self.pen_gr
        #print_rect(self.rectax, 'XXX GUView.update_my_scene axes rect')

        self.raxesi.setCursorHover(Qt.CrossCursor)
        self.raxesi.setCursorGrab (Qt.SizeAllCursor)
        self.raxesi.setZValue(20)
        self.raxesv.setZValue(-1)

        self.rsboti.setCursorHover(Qt.SizeHorCursor)
        self.rsboti.setCursorGrab (Qt.SplitHCursor)
        self.rstopi.setCursorHover(Qt.SizeHorCursor)
        self.rstopi.setCursorGrab (Qt.SplitHCursor)

        self.rslefv.setZValue(1)
        self.rsbotv.setZValue(1)
        self.rsrigv.setZValue(1)
        self.rstopv.setZValue(1)

        self.rslefi.setZValue(20)
        self.rsboti.setZValue(20)
        self.rsrigi.setZValue(20)
        self.rstopi.setZValue(20)

        #self.updateScene([self.rsbot, self.rslef, self.rectax])

        #self.check_axes_limits()

        if self.show_mode & 1 :
            colfld = Qt.magenta
            self.raxi = self.add_rect_to_scene_v1(self.raxes, pen=QtGui.QPen(Qt.NoPen), brush=QtGui.QBrush(colfld))

        if self.show_mode & 2 :
            ror=QtCore.QRectF(-2, -2, 4, 4)
            colori = Qt.red
            self.rori = self.add_rect_to_scene(ror, pen=QtGui.QPen(colori, 0, Qt.SolidLine), brush=QtGui.QBrush(colori))

#------------------------------

    def check_axes_limits(self):
        """Checks if axes limits have changed and submits signal with new limits
        """
        rax = self.rectax
        x1, x2 = rax.left(),   rax.right()
        y1, y2 = rax.bottom(), rax.top()

        if x1 != self._x1_old or x2 != self._x2_old \
        or y1 != self._y1_old or y2 != self._y2_old :
            self._x1_old = x1
            self._x2_old = x2
            self._y1_old = y1
            self._y2_old = y2
            #self.evaluate_hist_statistics()
            self.emit(QtCore.SIGNAL('axes_limits_changed(float,float,float,float)'), x1, x2, y1, y2)

    def connect_axes_limits_changed_to(self, recip) :
        self.connect(self, QtCore.SIGNAL('axes_limits_changed(float,float,float,float)'), recip)

    def disconnect_axes_limits_changed_from(self, recip) :
        self.disconnect(self, QtCore.SIGNAL('axes_limits_changed(float,float,float,float)'), recip)

    def test_axes_limits_changed_reception(self, x1, x2, y1, y2) :
        print 'GUView.test_axes_limits_changed_reception x1: %.2f  x2: %.2f  y1: %.2f  y2: %.2f' % (x1, x2, y1, y2)

#------------------------------

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
        #print 'GUView.mouseReleaseEvent, at point: ', e.pos(), ' diff:', e.pos() - self.pos_click
        #self.pos_click = e.pos()
        self.pos_click = None
        self.check_axes_limits()


#    def mouseDoubleCkickEvent(self, e):
#        QtGui.QGraphicsView.mouseDoubleCkickEvent(self, e)
#        print 'mouseDoubleCkickEvent'


    def mousePressEvent(self, e):
        #print 'GUView.mousePressEvent, at point: ', e.pos() #e.globalX(), e.globalY() 
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

        if   item == self.rsboti : self.scalebw = 1 # print 'bottom rect' # |= 1
        elif item == self.rstopi : self.scalebw = 1 # print 'left rect' # |= 2
        elif item == self.rslefi : self.scalebw = 2 # print 'left rect' # |= 2
        elif item == self.rsrigi : self.scalebw = 2 # print 'left rect' # |= 2
        else                     : self.scalebw = 3
        #elif item == self.raxesi   : self.scalebw = 3 # print 'axes rect'
        #print 'selectFurtherAction scalebw:', self.scalebw


    def display_pixel_pos(self, e):
        p = self.mapToScene(e.pos())
        #print 'mouseMoveEvent, current point: ', e.x(), e.y(), ' on scene: %.1f  %.1f' % (p.x(), p.y()) 
        self.setWindowTitle('GUView: x=%.1f y=%.1f' % (p.x(), p.y()))


    def mouseMoveEvent(self, e):
        QtGui.QGraphicsView.mouseMoveEvent(self, e)
        #print 'GUView.mouseMoveEvent, at point: ', e.pos()
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

        self.continue_wheel_event()


    def continue_wheel_event(self, t_msec=500) :
        """Reset time interval for timer in order to catch wheel stop
        """
        self.timer.start(t_msec)
        #print 'update_on_wheel_event'


    def on_timeout(self) :
        """Is activated by timer when wheel is stopped and interval is expired
        """
        #print 'on_timeout'
        self.timer.stop()
        self.check_axes_limits()
        self.emit(QtCore.SIGNAL('wheel_is_stopped()'))

#------------------------------

    def connect_wheel_is_stopped_to(self, recip) :
        self.connect(self, QtCore.SIGNAL('wheel_is_stopped()'), recip)

    def disconnect_wheel_is_stopped_from(self, recip) :
        self.disconnect(self, QtCore.SIGNAL('wheel_is_stopped()'), recip)

    def test_wheel_is_stopped_reception(self) :
        print 'GUView.test_wheel_is_stopped_reception'

#------------------------------

    def enterEvent(self, e) :
    #    print 'enterEvent'
        QtGui.QGraphicsView.enterEvent(self, e)
        #QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.CrossCursor))
        

    def leaveEvent(self, e) :
    #    print 'leaveEvent'
        QtGui.QGraphicsView.leaveEvent(self, e)
        #QtGui.QApplication.restoreOverrideCursor()


    def closeEvent(self, e) :
        QtGui.QGraphicsView.closeEvent(self, e)
        #print 'GUView.closeEvent' #% self._name
        

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

    def reset_original_size(self) :
        self.set_view()
        self.update_my_scene()
        self.check_axes_limits()


    def keyPressEvent(self, e) :
        #print 'keyPressEvent, key=', e.key()         
        if   e.key() == Qt.Key_Escape :
            self.close()

        elif e.key() == Qt.Key_R : 
            print '%s: Reset original size' % self._name
            self.reset_original_size()


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

def test_guiview(tname) :
    print '%s:' % sys._getframe().f_code.co_name
    app = QtGui.QApplication(sys.argv)
    w = None
    rectax=QtCore.QRectF(0, 0, 100, 100)
    if   tname == '0': w=GUView(None, rectax, origin='DL', scale_ctl='HV', margl=0.12, margr=0.10, margt=0.06, margb=0.06, show_mode=3)
    elif tname == '1': w=GUView(None, rectax, origin='DL', scale_ctl='',   show_mode=1)
    elif tname == '2': w=GUView(None, rectax, origin='DL', scale_ctl='H',  show_mode=1)
    elif tname == '3': w=GUView(None, rectax, origin='DL', scale_ctl='V',  show_mode=1)
    elif tname == '4': w=GUView(None, rectax, origin='UL', scale_ctl='HV', show_mode=3)
    elif tname == '5': w=GUView(None, rectax, origin='DL', scale_ctl='HV', show_mode=3)
    elif tname == '6': w=GUView(None, rectax, origin='DR', scale_ctl='HV', show_mode=3)
    elif tname == '7': w=GUView(None, rectax, origin='UR', scale_ctl='HV', show_mode=3)
    else :
        print 'test %s is not implemented' % tname
        return

    w.connect_axes_limits_changed_to(w.test_axes_limits_changed_reception)
    #w.disconnect_axes_limits_changed_from(w.test_axes_limits_changed_reception)

    w.show()
    app.exec_()

#------------------------------

if __name__ == "__main__" :
    import sys; global sys
    import numpy as np; global np
    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print 50*'_', '\nTest %s' % tname
    test_guiview(tname)
    sys.exit('End of Test %s' % tname)

#------------------------------

