from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('userinterface_moe.ui', self) # Load the .ui file
        self.show() # Show the GUI

class IP():
    def __init__(self, tuple1, tuple2, tuple3, tuple4):
        self.tuple = tuple1
        self.tuple = tuple2
        self.tuple = tuple3
        self.tuple = tuple4

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application

