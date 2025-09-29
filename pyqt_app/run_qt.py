from gui.gui_qt import Main
import sys
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Main()
    m.resize(1000, 600)
    m.show()
    sys.exit(app.exec_())
