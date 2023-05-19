#!@PYTHON@

"""
Class :py:class:`QWSpectrum` - supports widget for spectrum
===========================================================

Usage ::

    Create GUViewHist object within pyqt QApplication
    --------------------------------------------------
    import sys
    from PyQt5 import QtGui, QtCore, QtWidgets
    from graphqt.QWSpectrum import QWSpectrum

    arr = image_with_random_peaks((50, 50))
    app = QtWidgets.QApplication(sys.argv)
    w = QWSpectrum(None, arr, show_frame=False) #, show_buts=False)

    Connect/disconnecr recipient to signals
    ---------------------------------------

    ### w.connect_color_table_is_changed_to(recipient)
    ### w.disconnect_color_table_is_changed_from(recipient) :
    ### w.test_color_table_is_changed_reception(self)

    For self.hist:
    self.hist.connect_axes_limits_changed_to(recipient)
    self.hist.connect_histogram_updated_to(recipient)
    self.hist.disconnect_histogram_updated_from(recipient)


    Methods
    -------
    w.on_but_save()
    w.on_but_reset()
    ctab = w.color_table(self)
    w.on_colorbar() # emits signal color_table_is_changed
    w.draw_mean_std(mean, std)
    w.draw_stat(mean, rms, err_mean, err_rms, neff, skew, kurt, err_err, sum_w)
    w.draw_cursor_locator(x, y, ibin, value)
    w.set_tool_tips()
    w.set_style()

    Internal methods
    -----------------

    Re-defines methods
    ------------------
    closeEvent

    Global scope methods
    --------------------
    test_guspectrum(tname)

See:
    * :py:class:`IVMain`
    * :py:class:`IVMainTabs`
    * :py:class:`IVConfigParameters`
    * :py:class:`IVImageCursorInfo`
    * :py:class:`IVMainTabs`
    * :py:class:`IVTabDataControl`
    * :py:class:`IVTabFileName`

Created on 2017-02-06 by Mikhail Dubrovin
"""

import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
Qt = QtCore.Qt
from graphqt.Styles import style

from graphqt.FWViewImage import image_with_random_peaks
from graphqt.FWViewColorBar import FWViewColorBar
from graphqt.GUViewHist import GUViewHist
import graphqt.ColorTable as ct
from graphqt.QWPopupSelectColorBar import popup_select_color_table

class QWSpectrum(QtWidgets.QWidget): # QtWidgets.QWidget, Frame
    """Widget for file name input."""
    def __init__(self, parent=None, arr=None,\
                 coltab = ct.color_table_rainbow(ncolors=1000, hang1=250, hang2=-20),
                 show_frame=True, show_buts=True):

        QtWidgets.QWidget.__init__(self, parent)
        self._name = self.__class__.__name__
        self.show_frame = show_frame
        self.show_buts  = show_buts

        self.but_save = QtWidgets.QPushButton('&Save')
        self.but_reset= QtWidgets.QPushButton('&Reset')

        self.lab_stat = QtWidgets.QLabel('    Histogram\n    statistics')
        self.lab_ibin = QtWidgets.QLabel('Bin info')

        rectax=QtCore.QRectF(0, 0, 1, 1)

        self.hist = GUViewHist(None, rectax, origin='DL', scale_ctl='H', rulers='DL',
                               margl=0.12, margr=0.01, margt=0.01, margb=0.15)
        self.hist.connect_mean_std_updated_to(self.draw_mean_std)
        self.hist.connect_statistics_updated_to(self.draw_stat)
        self.hist.connect_cursor_bin_changed_to(self.draw_cursor_locator)
        self.hist._ymin = None

        hcolor = Qt.yellow # Qt.green Qt.yellow Qt.blue
        self.hist.add_array_as_hist(arr, pen=QtGui.QPen(hcolor, 0), brush=QtGui.QBrush(hcolor))

        self.cbar = FWViewColorBar(None, coltab=coltab, orient='H')

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.hist,      0,  0, 100, 100)
        grid.addWidget(self.cbar,     96, 12,   4,  88)
        grid.addWidget(self.lab_stat,  0, 80,  10,  20)
        grid.addWidget(self.lab_ibin,  0, 12,   5,  20)

        grid.addWidget(self.but_reset, 92, 0,   4,  10)
        grid.addWidget(self.but_save,  96, 0,   4,  10)
        self.setLayout(grid)

        self.set_tool_tips()
        self.set_style()

        self.cbar.connect_mouse_press_event_to(self.on_colorbar)

        #self.hist.disconnect_mean_std_updated_from(self.draw_stat)
        #self.hist.disconnect_statistics_updated_from(self.draw_stat)
        #self.cbar.disconnect_click_on_color_bar_from(self.on_colorbar)
        #self.connect_color_table_is_changed_to(self.test_color_table_is_changed_reception)

        if self.show_buts:
          self.but_save.clicked.connect(self.on_but_save)
          self.but_reset.clicked.connect(self.on_but_reset)


    def on_but_save(self):
        fltr='*.png *.gif *.jpg *.jpeg\n *'
        fname = 'fig-spectrum.png'
        fname = str(QtWidgets.QFileDialog.getSaveFileName(self, 'Output file', fname, filter=fltr))[0]
        if fname == '': return
        print('QWSpectrum.on_but_save: save image in file: %s' % fname)
        p = QtGui.QPixmap.grabWidget(self, self.rect())
        p.save(fname, 'jpg')


    def on_but_reset(self):
        #print 'QWSpectrum.on_but_reset TBD'
        self.hist.reset_original_hist()


    def color_table(self):
        return self.ctab


    def on_colorbar(self, e):
        #print('QWSpectrum.on_colorbar')
        ctab_ind = popup_select_color_table(None)
        print('select_color_table index: %d' % ctab_ind)
        if ctab_ind is None: return
        self.ctab = ct.next_color_table(ctab_ind)
#        arr = ct.array_for_color_bar(self.ctab, orient='H')
#        self.cbar.set_pixmap_from_arr(arr)
#        self.emit(QtCore.SIGNAL('color_table_is_changed()'))

#    def connect_color_table_is_changed_to(self, recip):
#        self.connect(self, QtCore.SIGNAL('color_table_is_changed()'), recip)

#    def disconnect_color_table_is_changed_from(self, recip):
#        self.disconnect(self, QtCore.SIGNAL('color_table_is_changed()'), recip)

#    def test_color_table_is_changed_reception(self):
#        print 'QWSpectrum.color_table_is_changed:', self.ctab.shape


    def draw_mean_std(self, mean, std):
        txt = '    Mean: %.2f\n    RMS: %.2f' % (mean, std)
        #print txt
        self.lab_stat.setText(txt)


    def draw_stat(self, mean, rms, err_mean, err_rms, neff, skew, kurt, err_err, sum_w):
        #print 'XXX: mean, rms, err_mean, err_rms, neff, skew, kurt, err_err, sum_w',\
        #            mean, rms, err_mean, err_rms, neff, skew, kurt, err_err, sum_w
        txt = u'  Entries: %d\n  Mean: %.2f \u00B1 %.2f\n  RMS: %.2f \u00B1 %.2f\n  \u03B31=%.2f   \u03B32=%.2f'%\
              (neff, mean, err_mean, rms, err_rms, skew, kurt)
        #print txt
        self.lab_stat.setText(txt)


    def draw_cursor_locator(self, x, y, ibin, value):
        txt = '  Bin:%d  value=%.2f' % (ibin, value)
        #print txt
        self.lab_ibin.setText(txt)


    def set_tool_tips(self):
        #self.hist.setToolTip('Spectrum histogram')
        self.cbar.setToolTip('Color bar')


    def set_style(self):
        self.setWindowTitle('Spectrum with color bar')

        self.setMinimumSize(400,150)
        self.setGeometry(50, 50, 500, 300)
        self.cbar.setMinimumSize(200, 2)
        self.cbar.setFixedHeight(22)
        self.setContentsMargins(-9,-9,-9,-9)

        self.lab_stat.setStyleSheet(style.styleStat)
        self.lab_ibin.setStyleSheet(style.styleStat)
        self.lab_ibin.setFixedSize(150,20)

        self.but_reset.setFixedSize(50,30)
        self.but_save .setFixedSize(50,30)

        self.but_reset.setVisible(self.show_buts)
        self.but_save .setVisible(self.show_buts)


    def closeEvent(self, e):
        #log.info('closeEvent', self._name)
        #print '%s.closeEvent' % self._name

        try: self.hist.close()
        except: pass

        try: self.cbar.close()
        except: pass

        QtWidgets.QWidget.closeEvent(self, e)


if __name__ == "__main__":

  def test_guspectrum(tname):
    print(sys._getframe().f_code.co_name)

    arr = image_with_random_peaks((50, 50))
    app = QtWidgets.QApplication(sys.argv)
    w = QWSpectrum(None, arr, show_frame=False) #, show_buts=False)

    w.cbar.connect_new_color_table_to(w.cbar.test_new_color_table_reception)
    w.hist.connect_axes_limits_changed_to(w.hist.test_axes_limits_changed_reception)
    w.hist.connect_histogram_updated_to(w.hist.test_histogram_updated_reception)

    w.show()
    app.exec_()


if __name__ == "__main__":
    import sys; global sys
    import numpy as np; global np
    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print(50*'_', '\nTest %s' % tname)
    test_guspectrum(tname)
    sys.exit('End of Test %s' % tname)

# EOF
