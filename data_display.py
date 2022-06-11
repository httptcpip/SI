from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from inf import Ui_MainWindow
import sys
from main import main
from threading import Thread


class InfmationForm(QtWidgets.QMainWindow, Ui_MainWindow):  # 括号中的Ui_Form要跟ui.py文件里的class同名
    def __init__(self, parent=None):
        super(InfmationForm, self).__init__(parent)
        self.setupUi(self)  # 生成界面
        self.pushButton.clicked.connect(self.startTheSim)
        self.Sim = None

    def startTheSim(self):
        self.Sim = Thread(target=main())
        self.Sim.start()


def real_main():
    app = QApplication(sys.argv)
    w = InfmationForm()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    real_main()
