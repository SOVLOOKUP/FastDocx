from PySide2 import QtGui
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtUiTools import QUiLoader
import PySide2

class CommonHelper:
  def __init__(self):
    pass
 
  @staticmethod
  def readQss(style):
    with open(style, 'r') as f:
        return f.read()

class fastdocx(QWidget):
    def __init__(self,parent = None):
        super(fastdocx, self).__init__(parent)
        self.ui = QUiLoader().load('form.ui')
        self.ui.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.ui.setWindowTitle('分布式报表协作系统')

if __name__ == "__main__":
    app = QApplication([])

    widget = fastdocx()
    qssStyle = CommonHelper.readQss('./qss/white.qss')
    widget.ui.setStyleSheet(qssStyle)
    widget.ui.show()
    app.exec_()


