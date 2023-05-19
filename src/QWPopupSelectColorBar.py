
"""Popup GUI for (str) item selection from the list of items
   Created early than 2017-01-31
"""

import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import graphqt.ColorTable as ct
from graphqt.Styles import style


class QWPopupSelectColorBar(QtWidgets.QDialog):

    def __init__(self, parent=None):

        QtWidgets.QDialog.__init__(self, parent)

        # Confirmation buttons
        self.but_cancel = QtWidgets.QPushButton('&Cancel')

        self.ctab_selected = None
        self.list = QtWidgets.QListWidget(parent)

        self.fill_list()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.list)
        self.setLayout(vbox)

        self.but_cancel.clicked.connect(self.onCancel)
        self.list.itemClicked.connect(self.onItemClick)

        self.showToolTips()
        self.setStyle()


    def fill_list(self):
        for i in range(1,9):
           item = QtWidgets.QListWidgetItem('%02d'%i, self.list)
           item.setSizeHint(QtCore.QSize(200,30))
           item._coltab_index = i
           #item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
           lab = QtWidgets.QLabel(parent=None)
           lab.setPixmap(ct.get_pixmap(i, size=(200,30)))
           self.list.setItemWidget(item, lab)

        item = QtWidgets.QListWidgetItem('cancel', self.list)
        self.list.setItemWidget(item, self.but_cancel)


    def onItemClick(self, item):
        self.ctab_selected = item._coltab_index
        #print('self.ctab_selected', self.ctab_selected)
        self.accept()


    def setStyle(self):
        self.setWindowTitle('Select')
        self.setFixedWidth(215)
        lst_len = self.list.__len__()
        self.setMinimumHeight(30*lst_len+10)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setContentsMargins(QtCore.QMargins(-9,-9,-9,-9))
        self.but_cancel.setStyleSheet(style.styleButton)
        self.but_cancel.setFixedSize(200,30)
        self.move(QtGui.QCursor.pos().__add__(QtCore.QPoint(-110,-50)))


    def showToolTips(self):
        self.setToolTip('Select color table')


    def mousePressEvent(self, e):
        #print 'mousePressEvent'
        child = self.childAt(e.pos())

        if isinstance(child, QtWidgets.QLabel):
            #print 'Selected color table index: %d' % child._coltab_index
            self.ctab_selected = child._coltab_index
            print('XXXX ctab_selected', self.ctab_selected)
            self.accept()


    def event(self, e):
        #print 'event.type', e.type()
        if e.type() == QtCore.QEvent.WindowDeactivate:
            self.reject()
        return QtWidgets.QDialog.event(self, e)


    def closeEvent(self, e):
        #logger.info('closeEvent', __name__)
        self.reject()


    def selectedColorTable(self):
        return self.ctab_selected


    def onCancel(self):
        #logger.debug('onCancel', __name__)
        self.reject()


def popup_select_color_table(parent):
    w = QWPopupSelectColorBar(parent)
    ##w.show()
    resp=w.exec_()

#    if   resp == QtWidgets.QDialog.Accepted: return w.selectedColorTable()
#    elif resp == QtWidgets.QDialog.Rejected: return None
#    else: return None

    return w.selectedColorTable()


#----------- TESTS ------------

def test_select_color_table(tname):
    app = QtWidgets.QApplication(sys.argv)
    ctab_ind = popup_select_color_table(None)
    print('Selected color table index = %s' % ctab_ind)


if __name__ == "__main__":
    import sys; global sys
    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print(50*'_', '\nTest %s' % tname)
    if   tname == '0': test_select_color_table(tname)
    #elif tname == '1': test_select_icon(tname)
    else: sys.exit('Test %s is not implemented' % tname)
    sys.exit('End of Test %s' % tname)

# EOF
