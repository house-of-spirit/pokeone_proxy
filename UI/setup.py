from typing import *
import sys
import UI.ui_main
import UI.startup
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QHeaderView
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import json

class MainUI(QMainWindow):
    """
    Class to start up the GUI
    """

    def __init__(self):
        self.app = UI.startup.Startup(sys.argv)
        super(MainUI, self).__init__()

        
    def setup(self):
        self.ui = UI.ui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        self.startup_ui()
        
    def startup_ui(self):
        self.ui.tableWidget.horizontalHeader().setVisible(True)
        self.ui.tableWidget.resizeRowsToContents()

        for n in (1, 2, 4, 5, 6):
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(n, QHeaderView.Stretch);
        
    def run(self, startup: Optional[Callable]):
        if startup:
            self.packet_data = []
            self.selected_packet = -1

            self.app.set_signal(lambda: startup(self.ui.tableWidget, self.packet_data))

            self.ui.tableWidget.cellActivated.connect(self.table_select)
            self.ui.tableWidget.cellClicked.connect(self.table_select)
            self.show()
            self.app.exec_()

    def table_select(self, x, y):
        if x == self.selected_packet:
            return
        self.selected_packet = x 

        self.ui.textEdit.document().setPlainText(
                        json.dumps(
                            self.packet_data[x], 
                            indent=4, 
                            separators=(',', ': ')
                        )
        )
        
        