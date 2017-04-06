#!@PYTHON@
"""
Created on February 1, 2017

@author: Mikhail Dubrovin

Class IVMainButtons is a QWidget for interactive image.

Usage ::
"""
#import os
#import math

from PyQt4 import QtGui, QtCore
#from PyQt4.QtCore import Qt

from graphqt.Logger import log
#from graphqt.Frame  import Frame
#from graphqt.QIcons import icon
#from graphqt.Styles import style

from graphqt.IVConfigParameters import cp
#from expmon.QWInsExpRun import QWInsExpRun

#class IVMainButtons(Frame) :
class IVMainButtons(QtGui.QWidget) :

    def __init__(self, parent=None) :
        #Frame.__init__(self, parent=None, mlw=1)
        QtGui.QWidget.__init__(self, parent=None)
        self._name = self.__class__.__name__

        self.show_buts = True

        self.but_save = QtGui.QPushButton('&Save')
        self.but_reset= QtGui.QPushButton('&Reset')

        #self.qwinsexprun = QWInsExpRun(cp, parent=None, orient='V') # QtGui.QPushButton('button')
        
        #self.lab_stat = QtGui.QLabel('    Histogram\n    statistics')
        #self.lab_ibin = QtGui.QLabel('Bin info')

        #grid = QtGui.QGridLayout()
        #grid.addWidget(self.qwinsexprun, 0, 0,   1,  10)
        #grid.addWidget(self.but_reset,   1, 0)
        #grid.addWidget(self.but_save,    1, 1)
        #self.setLayout(grid) 

        self.hbox = QtGui.QHBoxLayout() 
        self.hbox.addWidget(self.but_reset) 
        self.hbox.addWidget(self.but_save) 
        self.hbox.addStretch(1)
        self.setLayout(self.hbox) 

        self.set_tool_tips()
        self.set_style()

        self.connect(self.but_save,  QtCore.SIGNAL('clicked()'), self.on_but)
        self.connect(self.but_reset, QtCore.SIGNAL('clicked()'), self.on_but)

#------------------------------

    def set_tool_tips(self) :
        self.setToolTip('Control buttons') 

#------------------------------

    def set_style(self) :
        self.setMinimumSize(300,40)
        self.setContentsMargins(-9,-9,-9,-9)
 
        #self.setGeometry(50, 50, 500, 300)
        #self.cbar.setMinimumSize(300, 22)
        #self.cbar.setMinimumSize(200, 2)
        #self.cbar.setFixedHeight(22)
        #self.setMinimumWidth(300)
        #self.edi.setMinimumWidth(210)
        #self.lab_stat.setStyleSheet(style.styleStat)
        #self.lab_ibin.setStyleSheet(style.styleStat)
        #self.lab_ibin.setFixedSize(150,20)

        self.but_reset.setFixedSize(60,30)
        self.but_save .setFixedSize(60,30)

        self.but_reset.setVisible(self.show_buts)
        self.but_save .setVisible(self.show_buts)

#------------------------------

    def on_but(self) :
        but = self.but_save if self.but_save.hasFocus()\
              else self.but_reset  if self.but_reset.hasFocus()\
              else None
        #print str(but.text())
        log.info('%s.on_but %s' % (self._name, str(but.text())))

#------------------------------

if __name__ == "__main__" :
    import sys
    log.setPrintBits(0377) 
    app = QtGui.QApplication(sys.argv)
    w  = IVMainButtons(parent=None)
    w.setContentsMargins(-9,-9,-9,-9)
    w.show()
    app.exec_()

#------------------------------
