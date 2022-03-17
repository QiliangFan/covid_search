from PyQt5 import QtWidgets
from loc_widget import LocWidght
import sys
from qt_material import apply_stylesheet

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    apply_stylesheet(app, "dark_teal.xml")
    widget = LocWidght()
    widget.show()

    sys.exit(app.exec())
