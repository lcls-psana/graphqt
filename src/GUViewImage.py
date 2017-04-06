#!@PYTHON@
"""
Created on September 9, 2016

@author: Mikhail Dubrovin

Class GUViewImage is a QWidget for interactive image.

Usage ::

    Emits signals
    -------------
    w.connect_axes_limits_changed_to(w.test_axes_limits_changed_reception)
    w.connect_pixmap_is_updated_to(w.test_pixmap_is_updated_reception)

    import sys
    from PyQt4 import QtGui, QtCore
    from graphqt.GUViewImage import GUViewImage
    import graphqt.ColorTable as ct
    app = QtGui.QApplication(sys.argv)
    ctab = ct.color_table_monochr256()
    w = GUViewImage(None, arr, origin='UL', scale_ctl='HV', coltab=ctab)
    w.show()
    app.exec_()
"""

#import os
#import math
#import math
from math import floor
import graphqt.ColorTable as ct
from graphqt.GUViewAxes import *
from graphqt.Logger import log

class GUViewImage(GUViewAxes) :
    
    def __init__(self, parent=None, arr=None,\
                 coltab=ct.color_table_rainbow(ncolors=1000, hang1=250, hang2=-20),\
                 origin='UL', scale_ctl='HV', rulers='TBLR',\
                 margl=None, margr=None, margt=None, margb=None) :

        h, w  = arr.shape
        rectax = QtCore.QRectF(0, 0, w, h)

        GUViewAxes.__init__(self, parent, rectax, origin, scale_ctl, rulers, margl, margr, margt, margb)

        self._name = self.__class__.__name__

        #self.scene().removeItem(self.raxi)
        self.pmi  = None

        mean, std = arr.mean(), arr.std()
        amin, amax = mean-2*std, mean+10*std # None, None

        self.set_intensity_limits(amin, amax)
        self.set_color_table(coltab)
        self.set_pixmap_from_arr(arr)


    def set_color_table(self, coltab=None) :
        self.coltab = coltab # if coltab is not None else\
                      #ct.color_table_rainbow(ncolors=1000, hang1=-150, hang2=120)


    def set_style(self) :
        GUViewAxes.set_style(self)
        #w.setContentsMargins(-9,-9,-9,-9)
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


    def image_data(self):
        return self.arr


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
        #self.setWindowTitle('GUViewImage x=%d y=%d v=%s' % (ix, iy, vstr))
        #print 'mouseMoveEvent, current point: ', e.x(), e.y(), ' on scene: %.1f  %.1f' % (p.x(), p.y()) 
        #return ix, iy, v
        self.emit(QtCore.SIGNAL('cursor_pos_value(int,int,float)'), ix, iy, v if not(v is None) else 0)

    def connect_cursor_pos_value_to(self, recip) :
        self.connect(self, QtCore.SIGNAL('cursor_pos_value(int,int,float)'), recip)

    def disconnect_cursor_pos_value_from(self, recip) :
        self.disconnect(self, QtCore.SIGNAL('cursor_pos_value(int,int,float)'), recip)

    def test_cursor_pos_value_reception(self, ix, iy, v) :
        #print 'GUView.test_cursor_pos_value_reception x1: %.2f  x2: %.2f  y1: %.2f  y2: %.2f' % (x1, x2, y1, y2)
        self.setWindowTitle('GUViewImage x=%d y=%d v=%.1f' % (ix, iy, v))

    def mouseMoveEvent(self, e):
        GUViewAxes.mouseMoveEvent(self, e)

#------------------------------
 
    def closeEvent(self, e):
        GUViewAxes.closeEvent(self, e)
        #print '%s.closeEvent' % self._name

#------------------------------

    def reset_original_image_size(self) :
        self.set_view()
        self.update_my_scene()
        self.check_axes_limits()


    def keyPressEvent(self, e) :
        #print 'keyPressEvent, key=', e.key()         
        if   e.key() == Qt.Key_Escape :
            self.close()

        elif e.key() == Qt.Key_R : 
            print '%s: Reset original size' % self._name
            self.reset_original_image_size()

        elif e.key() == Qt.Key_N : 
            print '%s: Test set new pixel map' % self._name
            s = self.pmi.pixmap().size()
            #self.set_pixmap_random((s.width(), s.height()))
            img = image_with_random_peaks((s.height(), s.width()))
            self.set_pixmap_from_arr(img)


    def set_intensity_limits(self, amin=None, amax=None) :
        self.amin = amin
        self.amax = amax


    def add_pixmap_to_scene(self, pixmap, flag=Qt.IgnoreAspectRatio,\
                            mode = Qt.FastTransformation) : # Qt.KeepAspectRatio, IgnoreAspectRatio
        #self.scene().clear()
        #if self.pmi is not None : self.scene().removeItem(self.pmi)
        size = pixmap.size()
        #print 'XXX: size to scale pixmap', size # window size
        #self.pmi = self.scene().addPixmap(pixmap)
        #self.pmi = self.scene().addPixmap(pixmap.scaled(size, flag, mode))

        if self.pmi is None : self.pmi = self.scene().addPixmap(pixmap)
        else                : self.pmi.setPixmap(pixmap)

        #self.pmi.setFlags(self.pmi.ItemIsSelectable)
        self.update_my_scene() # ->
        self.check_axes_limits()


    def set_pixmap_from_arr(self, arr=None) :
        if arr is not None: self.arr = arr
        anorm = self.arr if self.coltab is None else\
                ct.apply_color_table(self.arr, self.coltab, self.amin, self.amax) 
        h, w = self.arr.shape
        image = QtGui.QImage(anorm, w, h, QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.add_pixmap_to_scene(pixmap)
        self.emit(QtCore.SIGNAL('pixmap_is_updated()'))

#------------------------------

    def connect_pixmap_is_updated_to(self, recip) :
        self.connect(self, QtCore.SIGNAL('pixmap_is_updated()'), recip)

    def disconnect_pixmap_is_updated_from(self, recip) :
        self.disconnect(self, QtCore.SIGNAL('pixmap_is_updated()'), recip)

    def test_pixmap_is_updated_reception(self) :
        print 'GUView.test_pixmap_is_updated_reception'

#------------------------------

    def set_pixmap_random(self, shape=(512,512)) :
        from NDArrGenerators import random_array_xffffffff
        w, h = shape # corresponds to row, col i.e. non-matrix...
        arr = random_array_xffffffff(shape)
        image = QtGui.QImage(arr, w, h, QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.add_pixmap_to_scene(pixmap)

#------------------------------
 
    def on_but_save(self, at_obj=None) :
        import os

        fname='fig-image.xpm'
        fltr='*.xpm *.ppm *.png *.jpg *.pgm\n *'
        fname = str(QtGui.QFileDialog.getSaveFileName(at_obj, 'Output file', fname, filter=fltr))
        if fname == '' : return
        log.info('Save image or pixmap in file: %s' % fname, self._name)

        root, ext = os.path.splitext(fname)
        if ext.lower() in ('.xpm', '.ppm', '.pgm') : self.save_pixmap_in_file(fname)
        #elif ext.lower() == '.gif' : self.save_qimage_in_file(fname)
        else : self.save_window_in_file(fname)

#------------------------------
 
    def save_pixmap_in_file(self, fname='fig-image.xpm') :
        p = self.pmi.pixmap()
        p.save(fname, format=None, quality=100)

#------------------------------
 
    def save_qimage_in_file(self, fname='fig-image.gif') :
        qim = self.pmi.pixmap().toImage() # QPixmap -> QImage
        qim.save(fname, format=None, quality=100)

#------------------------------
 
    def save_window_in_file(self, fname='fig-image.png') :
        #p = QtGui.QPixmap.grabWindow(self.winId())
        p = QtGui.QPixmap.grabWidget(self, self.rect())
        p.save(fname, format=None)
    
#------------------------------
 
    def on_but_reset(self) :
        log.debug('%s.on_but_reset - reset original image size' % self._name)
        self.reset_original_image_size()

#------------------------------

def image_with_random_peaks(shape=(500, 500)) : 
    import pyimgalgos.NDArrGenerators as ag
    img = ag.random_standard(shape, mu=0, sigma=10)
    peaks = ag.add_random_peaks(img, npeaks=50, amean=100, arms=50, wmean=1.5, wrms=0.3)
    ag.add_ring(img, amp=20, row=500, col=500, rad=300, sigma=50)
    return img

#-----------------------------

def test_guiviewimage(tname) :
    print '%s:' % sys._getframe().f_code.co_name
    #import numpy as np
    #arr = np.random.random((1000, 1000))
    arr = image_with_random_peaks((1000, 1000))
    ctab = ct.color_table_monochr256()

    app = QtGui.QApplication(sys.argv)
    w = None
    if   tname == '0': 
        w = GUViewImage(None, arr, coltab=ctab, origin='UL', scale_ctl='HV', rulers='UDLR',\
                        margl=0.12, margr=0.10, margt=0.06, margb=0.06)
    elif tname == '1': 
        w = GUViewImage(None, arr, coltab=ctab, origin='UL', scale_ctl='HV', rulers='DL',\
                        margl=0.12, margr=0.02, margt=0.02, margb=0.06)
    elif tname == '2': 
        w = GUViewImage(None, arr, coltab=ctab, origin='UL', scale_ctl='HV', rulers='',\
                        margl=0, margr=0, margt=0, margb=0)
    elif tname == '3':
        ctab=ct.color_table_rainbow(ncolors=1000, hang1=250, hang2=-20)
        w = GUViewImage(None, arr, coltab=ctab, origin='UL', scale_ctl='HV', rulers='UL',\
                        margl=0.12, margr=0.02, margt=0.02, margb=0.06)

    else :
        print 'test %s is not implemented' % tname
        return

    w.connect_axes_limits_changed_to(w.test_axes_limits_changed_reception)
    #w.disconnect_axes_limits_changed_from(w.test_axes_limits_changed_reception)

    w.connect_pixmap_is_updated_to(w.test_pixmap_is_updated_reception)
    #w.disconnect_pixmap_is_updated_from(w.test_pixmap_is_updated_reception)
    
    w.connect_cursor_pos_value_to(w.test_cursor_pos_value_reception)
    #w.disconnect_cursor_pos_value_from(w.test_cursor_pos_value_reception)

    w.show()
    app.exec_()

#------------------------------

if __name__ == "__main__" :
    import sys; global sys
    import numpy as np; global np
    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print 50*'_', '\nTest %s' % tname
    test_guiviewimage(tname)
    sys.exit('End of Test %s' % tname)

#------------------------------
