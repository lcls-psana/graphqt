#!@PYTHON@
"""
Created on September 9, 2016

@author: Mikhail Dubrovin

Class GUViewFWImage is a QWidget for interactive image.

Usage ::

    import sys
    from PyQt4 import QtGui, QtCore
    from graphqt.GUViewFWImage import GUViewFWImage
    import graphqt.ColorTable as ct
    app = QtGui.QApplication(sys.argv)
    ctab = ct.color_table_monochr256()
    w = GUViewFWImage(None, arr, origin='UL', scale_ctl='HV', coltab=ctab)
    w.show()
    app.exec_()
"""

#import os
#import math
#import math
import numpy as np
from PyQt5.QtWidgets import *
from math import floor
import graphqt.ColorTable as ct
from graphqt.GUViewFW import *

class GUViewFWImage(GUViewFW) :
    
    click_on_color_bar = QtCore.pyqtSignal()

    def __init__(self, parent=None, arr=None,\
                 coltab=ct.color_table_rainbow(ncolors=1000, hang1=250, hang2=-20),\
                 origin='UL', scale_ctl='HV') :

        h, w = arr.shape
        rectax = QtCore.QRectF(0, 0, w, h)
        GUViewFW.__init__(self, parent, rectax, origin, scale_ctl)
        self._name = self.__class__.__name__

        #self.scene().removeItem(self.raxi)
        self.coltab = coltab
        self.pmi = None
        self.set_pixmap_from_arr(arr)


    def set_style(self) :
        GUViewFW.set_style(self)
        self.setWindowTitle("GUViewFWImage window")
        #self.setContentsMargins(-9,-9,-9,-9)
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


    def display_pixel_pos(self, e):
        p = self.mapToScene(e.pos())
        ix, iy = int(floor(p.x())), int(floor(p.y()))
        v = None
        arr = self.arr
        if ix<0\
        or iy<0\
        or iy>arr.shape[0]-1\
        or ix>arr.shape[1]-1 : pass
        else : v = self.arr[iy,ix]
        vstr = 'None' if v is None else '%.1f' % v 
        #print 'mouseMoveEvent, current point: ', e.x(), e.y(), ' on scene: %.1f  %.1f' % (p.x(), p.y()) 
        self.setWindowTitle('GUViewFWImage x=%d y=%d v=%s' % (ix, iy, vstr))
        #return ix, iy, v


    def mousePressEvent(self, e):
        GUViewFW.mousePressEvent(self, e)
        #print 'GUViewFWImage.mousePressEvent'
        self.click_on_color_bar.emit()

#------------------------------

    def connect_click_on_color_bar_to(self, recip) :
        self.click_on_color_bar.connect(recip)

    def disconnect_click_on_color_bar_from(self, recip) :
        self.click_on_color_bar.disconnect(recip)

#------------------------------

    def mouseMoveEvent(self, e):
        GUViewFW.mouseMoveEvent(self, e)

#------------------------------
 
    def closeEvent(self, e):
        GUViewFW.closeEvent(self, e)
        #print '%s.closeEvent' % self._name

#------------------------------

    def keyPressEvent(self, e) :
        #print 'keyPressEvent, key=', e.key()         
        if   e.key() == Qt.Key_Escape :
            self.close()

        elif e.key() == Qt.Key_R : 
            print 'Reset original size'
            self.set_view()
            self.update_my_scene()

        elif e.key() == Qt.Key_N : 
            print 'Set new pixel map'
            s = self.pmi.pixmap().size()
            #self.set_pixmap_random((s.width(), s.height()))
            #img = image_with_random_peaks((s.width(), s.height()))
            img = image_with_random_peaks((s.height(), s.width()))
            self.set_pixmap_from_arr(img)


    def add_pixmap_to_scene(self, pixmap, flag=Qt.IgnoreAspectRatio,\
                            mode = Qt.FastTransformation) : # Qt.KeepAspectRatio, IgnoreAspectRatio
        #size = pixmap.size()
        #print 'size',  size

        if self.pmi is None : self.pmi = self.scene().addPixmap(pixmap)
        else                : self.pmi.setPixmap(pixmap)
        self.update_my_scene()


    def set_pixmap_from_arr(self, arr) :
        """Input array is scailed by color table. If color table is None arr set as is.
        """
        self.arr = arr
        anorm = arr if self.coltab is None else\
                ct.apply_color_table(arr, ctable=self.coltab) 
        h, w = arr.shape
        #print 'GUViewFWImage.set_pixmap_from_arr shape=', arr.shape
        self.raxes = QtCore.QRectF(0, 0, w, h)        
        image = QtGui.QImage(anorm, w, h, QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.add_pixmap_to_scene(pixmap)
        self.set_view()


    def set_pixmap_random(self, shape=(512,512)) :
        from NDArrGenerators import random_array_xffffffff
        h, w = shape # corresponds to row, col
        arr = random_array_xffffffff(shape)
        image = QtGui.QImage(arr, w, h, QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.add_pixmap_to_scene(pixmap)

#------------------------------

def image_with_random_peaks(shape=(500, 500)) : 
    import pyimgalgos.NDArrGenerators as ag
    img = ag.random_standard(shape, mu=0, sigma=10)
    peaks = ag.add_random_peaks(img, npeaks=50, amean=100, arms=50, wmean=1.5, wrms=0.3)
    ag.add_ring(img, amp=20, row=500, col=500, rad=300, sigma=50)
    return img

#-----------------------------

def test_guiviewfwimage(tname) :
    print '%s:' % sys._getframe().f_code.co_name
    #import numpy as np
    #arr = np.random.random((1000, 1000))
    arr = image_with_random_peaks((1000, 1000))
    #ctab = ct.color_table_rainbow(ncolors=1000, hang1=250, hang2=-20)
    ctab = ct.color_table_monochr256()
    #ctab = ct.color_table_interpolated()

    app = QtGui.QApplication(sys.argv)
    w = None
    if   tname == '0': w = GUViewFWImage(None, arr, coltab=ctab, origin='UL', scale_ctl='HV')
    elif tname == '1': w = GUViewFWImage(None, arr, coltab=ctab, origin='UL', scale_ctl='H')
    elif tname == '2': w = GUViewFWImage(None, arr, coltab=ctab, origin='UL', scale_ctl='V')
    elif tname == '3': w = GUViewFWImage(None, arr, coltab=ctab, origin='UL', scale_ctl='')
    elif tname == '4':
        arrct = ct.array_for_color_bar(orient='H')
        w = GUViewFWImage(None, arrct, coltab=None, origin='UL', scale_ctl='H')
        w.setGeometry(50, 50, 500, 40)
    elif tname == '5':
        arrct = ct.array_for_color_bar(orient='V')
        w = GUViewFWImage(None, arrct, coltab=None, origin='UL', scale_ctl='V')
        w.setGeometry(50, 50, 40, 500)
    elif tname == '6':
        #ctab= ct.color_table_rainbow(ncolors=1000, hang1=0, hang2=360)
        #ctab = ct.color_table_rainbow(ncolors=1000, hang1=250, hang2=-20)
        #ctab = ct.color_table_monochr256()
        ctab = ct.color_table_interpolated()
        arrct = ct.array_for_color_bar(ctab, orient='H')
        w = GUViewFWImage(None, arrct, coltab=None, origin='UL', scale_ctl='H')
        w.setGeometry(50, 50, 500, 40)
    elif tname == '7':
        a = np.arange(15).reshape((5, 3))
        w = GUViewFWImage(None, a, coltab=ctab, origin='UL', scale_ctl='HV')
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
    test_guiviewfwimage(tname)
    sys.exit('End of Test %s' % tname)

#------------------------------
