#------------------------------
"""
@version $Id: IVTabDataControl.py 2017-04-12 dubrovin@SLAC.STANFORD.EDU$

@author Mikhail S. Dubrovin
"""
#------------------------------

from expmon.QWInsExpRun import QWInsExpRun

#------------------------------

class IVTabDataControl(QWInsExpRun) :
    """ Data control parameters window for tab "Data"
    """
    def __init__(self, cp, log, parent=None, show_mode=7) :
        QWInsExpRun.__init__(self, cp, log, parent=None, orient='V', show_mode=show_mode)
        self._name = self.__class__.__name__

        if cp.ivmain is None : return
        self.w_evt.connect_new_event_number_to_recipient(cp.ivmain.on_new_event_number)


    def test_on_new_event_number_reception(self, num) :
        print '%s.%s: num=%s' % (self._name, sys._getframe().f_code.co_name, num)

#------------------------------
#------------------------------
#------------------------------
#------------------------------

if __name__ == "__main__" :
    import sys
    from PyQt4 import QtGui, QtCore

    from graphqt.IVConfigParameters import cp
    from graphqt.Logger import log

    app = QtGui.QApplication(sys.argv)
    w = IVTabDataControl(cp, log, show_mode=0377)
    w.move(QtCore.QPoint(50,50))
    w.setWindowTitle(w._name)
    w.w_evt.connect_new_event_number_to_recipient(w.test_on_new_event_number_reception)
    w.show()
    app.exec_()

#------------------------------
