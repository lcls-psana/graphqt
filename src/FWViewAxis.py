#!@PYTHON@
"""
Class :py:class:`FWViewAxis` is a widget with interactive axes
==============================================================

FWViewAxis <- FWView <- QGraphicsView <- QWidget

Usage ::

    Create FWViewAxis object within pyqt QApplication
    --------------------------------------------------
    import sys
    from PyQt4 import QtGui, QtCore
    from graphqt.FWViewAxis import FWViewAxis

    app = QtGui.QApplication(sys.argv)
    w = FWViewAxis(None, raxes=QtCore.QRectF(0, 0, 100, 100), origin='UL',\
                   scale_ctl='HV', rulers='TR')
    w.show()
    app.exec_()

    Connect/disconnecr recipient to signals
    ---------------------------------------

    Methods
    -------
    w.set_show_rulers(rulers='TBLR')
    w.reset_original_image_size()

    Internal methods
    -----------------

    Re-defines methods
    ------------------
    w.update_my_scene() # FWView.update_my_scene() + draw rulers
    w.set_style()       # sets FWView.set_style() + color, font, pen
    w.closeEvent()      # removes rulers, FWView.closeEvent()

Created on December 12, 2017 by Mikhail Dubrovin
"""

from graphqt.FWView  import FWView, QtGui, QtCore, Qt
from graphqt.FWRuler import FWRuler
#from graphqt.GUUtils import print_rect

class FWViewAxis(FWView) :
    
    def __init__(self, parent=None, rscene=QtCore.QRectF(0, 0, 10, 10), origin='UL', orient='U', **kwargs) :

        self.scale_ctl = kwargs.get('scale_ctl', True)
        self.wlength   = kwargs.get('wlength', 200)
        self.wwidth    = kwargs.get('wwidth', 50)

        self.set_origin(origin)
        self.orient = orient
        scale_ctl = orient if self.scale_ctl else ''

        FWView.__init__(self, parent, rscene, origin, scale_ctl='HV')

        self._name = self.__class__.__name__
        #self.set_style() # called in FWView
        self.update_my_scene()


    def set_style(self) :
        FWView.set_style(self)
        self.colax = QtGui.QColor(Qt.white)
        self.fonax = QtGui.QFont('Courier', 12, QtGui.QFont.Normal)
        self.penax = QtGui.QPen(Qt.white, 1, Qt.SolidLine)

        if self.orient in ('U', 'D') :
            self.setMinimumSize(self.wlength, 2)
            self.setFixedHeight(self.wwidth)
        else :
            self.setMinimumSize(2, self.wlength)
            self.setFixedWidth(self.wwidth)

        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

#------------------------------


    def update_my_scene(self) :
        FWView.update_my_scene(self)

        sc = self.scene()
        rs = sc.sceneRect()
        ra = rs
        self.ruler = FWRuler(sc, orient=self.orient, color=self.colax, pen=self.penax, font=self.fonax)

        return

        #print_rect(ra, cmt='YYY FWViewAxis axes rect')

        if self._origin_ul :
            if self.orient=='L' : self.ruler = FWRuler(s, 'L')
            if self.orient=='D' : self.ruler = FWRuler(s, 'D')
            if self.orient=='U' : self.ruler = FWRuler(s, 'U')
            if self.orient=='R' : self.ruler = FWRuler(s, 'R')
        return


        if self._origin_dl :
            pass

        elif self._origin_dr :
            pass

        elif self._origin_ur :
            #print 'UR'
            pass


#------------------------------

    def reset_original_image_size(self) :
         # def in FWView.py with overloaded update_my_scene()
         self.reset_original_size()

#    def reset_original_image_size(self) :
#        self.set_view()
#        self.update_my_scene()
#        self.check_axes_limits_changed()

#------------------------------
 
    def closeEvent(self, e):
        self.rulerl = None
        self.rulerb = None
        self.rulerr = None
        self.rulert = None
        FWView.closeEvent(self, e)
        #print 'FWViewAxis.closeEvent'

#-----------------------------

def test_guiview(tname) :
    print '%s:' % sys._getframe().f_code.co_name
    app = QtGui.QApplication(sys.argv)
    w = None
    rs=QtCore.QRectF(0, 0, 100, 100)
    if   tname == '0': w=FWViewAxis(None, rs, origin='UL', orient='L')
    elif tname == '1': w=FWViewAxis(None, rs, origin='UL', orient='U')
    elif tname == '2': w=FWViewAxis(None, rs, origin='UL', orient='R')
    elif tname == '3': w=FWViewAxis(None, rs, origin='UL', orient='D')
    elif tname == '4': w=FWViewAxis(None, rs, origin='DR', orient='L')
    elif tname == '5': w=FWViewAxis(None, rs, origin='DR', orient='U')
    elif tname == '6': w=FWViewAxis(None, rs, origin='DR', orient='D')
    elif tname == '7': w=FWViewAxis(None, rs, origin='DR', orient='R')
    else :
        print 'test %s is not implemented' % tname
        return

    #w.connect_axes_limits_changed_to(w.test_axes_limits_changed_reception)
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
