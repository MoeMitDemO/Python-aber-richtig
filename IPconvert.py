from PyQt5 import QtWidgets, uic
import sys



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('userinterface_moe.ui', self) # Load the .ui file
        self.show() # Show the GUI

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class


class PC():
    def __init__(self, gebauede, stock, raum, nummer):
        self.gebauede = gebauede
        self.stock = stock
        self.raum = raum
        self.nummer = nummer

class IP():
    def __init__(self, tuple1, tuple2, tuple3, tuple4):
        self.tuple1 = tuple1
        self.tuple2 = tuple2
        self.tuple3 = tuple3
        self.tuple4 = tuple4

def umrechnen(wert):
    if window.ipzupc.isChecked() == True:
        angefragteIP = window.angefragteIP.text()
        parts = angefragteIP.split('.')
        hostanteil = bin(int(parts[2])).replace("0b", "").rjust(8, "0") + bin(int(parts[3])).replace("0b", "").rjust(8, "0")
        gebaeude = hostanteil[0:3]
        etage = hostanteil[4:6].replace('0', '')
        raum = hostanteil[7:10].lstrip('0')
        pcnummer = str(int(hostanteil[11:16], 2))

        def switch(gebaeude):
            return {
                '000': 'A',
                '001': 'B',
                '010': 'C',
                '011': 'D',
                '100': 'E'
                }.get(gebaeude, "Falsche eingabe")

        ergebnis = 'Gebäude: ' + switch(gebaeude) + ', Etage: ' + etage + ', Raum: ' + raum + ', PC: ' + pcnummer
        
        window.lblErgebnis.setText(ergebnis)

    elif window.pczuip.isChecked() == True:
        print('gay2')

window.angefragteIP.setText("1")
window.btnUmrechnen.clicked.connect(umrechnen)


app.exec_() # Start the application

