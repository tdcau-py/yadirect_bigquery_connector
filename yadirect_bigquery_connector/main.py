from PyQt6 import QtWidgets, uic


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(parent=None)
        # QtWidgets.QWidget.__init__(self, parent=None)
        gui, base = uic.loadUiType('gui_qt.ui')
        self.ui = gui()
        self.ui.setupUi(self)


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = MainWidget()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
