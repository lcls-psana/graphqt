
"""Popup GUI for (str) item selection from the list of items
   Created early than 2017-01-26
"""

import os

from PyQt5 import QtCore, QtGui, QtWidgets

class QWPopupSelectItem(QtWidgets.QDialog):

    def __init__(self, parent=None, lst=[]):

        QtWidgets.QDialog.__init__(self, parent)

        self.name_sel = None
        self.list = QtWidgets.QListWidget(parent)

        self.fill_list(lst)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.list)
        #vbox.addLayout(self.hbox)
        self.setLayout(vbox)

        self.list.itemClicked.connect(self.onItemClick)

        self.showToolTips()
        self.setStyle()


    def fill_list(self, lst):
        for exp in sorted(lst):
            item = QtWidgets.QListWidgetItem(exp, self.list)
        self.list.sortItems(QtCore.Qt.AscendingOrder)


    def setStyle(self):
        self.setWindowTitle('Select')
        self.setFixedWidth(100)
        self.setMinimumHeight(600)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setContentsMargins(QtCore.QMargins(-9,-9,-9,-9))
        self.move(QtGui.QCursor.pos().__add__(QtCore.QPoint(-110,-50)))


    def showToolTips(self):
        self.setToolTip('Select item from the list')


    def onItemClick(self, item):
        self.name_sel = item.text()
        self.accept()


    def event(self, e):
        #print 'event.type', e.type()
        if e.type() == QtCore.QEvent.WindowDeactivate:
            self.reject()
        return QtWidgets.QDialog.event(self, e)


    def closeEvent(self, e):
        #logger.info('closeEvent', __name__)
        self.reject()


    def selectedName(self):
        return self.name_sel


    def onCancel(self):
        #logger.debug('onCancel', __name__)
        self.reject()


    def onApply(self):
        #logger.debug('onApply', __name__)
        self.accept()


def popup_select_item_from_list(parent, lst):
    w = QWPopupSelectItem(parent, lst)
    ##w.show()
    resp=w.exec_()
#    if   resp == QtWidgets.QDialog.Accepted: return w.selectedName()
#    elif resp == QtWidgets.QDialog.Rejected: return None
#    else: return None
    return w.selectedName()


#----------- TESTS ------------

def test_select_exp(tname):
    lst = sorted(os.listdir('/reg/d/psdm/CXI/'))
    print('lst:', lst)
    app = QtWidgets.QApplication(sys.argv)
    exp_name = popup_select_item_from_list(None, lst)
    print('exp_name = %s' % exp_name)


if __name__ == "__main__":
    import sys; global sys
    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print(50*'_', '\nTest %s' % tname)
    if   tname == '0': test_select_exp(tname)
    #elif tname == '1': test_select_icon(tname)
    else: sys.exit('Test %s is not implemented' % tname)
    sys.exit('End of Test %s' % tname)

# EOF
