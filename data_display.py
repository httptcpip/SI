from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from inf import Ui_MainWindow
from main import *
from threading import Thread
import numpy as np
import pyqtgraph as pg
import time


class InfmationForm(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(InfmationForm, self).__init__(parent)
        self.setupUi(self)  # 生成界面
        self.pushButton_start.clicked.connect(self.startTheSim)
        self.Sim = None
        self.rec = np.array(list(range(30)))  # type:np.ndarray
        self.rec.resize((10, 3))
        pg.setConfigOptions(leftButtonPan=False)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

    def startTheSim(self):
        self.Sim = Thread(target=Main)
        self.Sim.start()
        start_time = time.time()
        while per_s + per_i + per_s > 0 and (int(round(time.time() * 1000)) - start_time) >= 1000:
            for i, row in enumerate(self.rec):
                self.rec[i] = self.rec[i + 1] if i < self.rec.shape[1] - 2 else np.array([per_s, per_i, per_r])
                print(self.rec)


def real_main():
    app = QApplication(sys.argv)
    w = InfmationForm()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    real_main()
