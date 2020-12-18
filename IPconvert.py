from os import times
from PyQt5 import QtWidgets, uic
import sys, datetime



            #---------------------------#
            #          Klassen          #
            #---------------------------#

#Diese Klasse beinhaltet alle für uns wichtigen Informationen der IP-Adresse und des PC's
class PC():
    def __init__(self, gebaeude, etage, raum, nummer):
        self.gebaeude   = gebaeude
        self.etage      = etage
        self.raum       = raum
        self.nummer     = nummer
    
    def gibPcAus(self):
        return str(self.gebaeude) + ' ' + str(self.etage)  + str(self.raum) + ' - ' + str(self.nummer)

class Hostanteil():
    def __init__(self, hGebaeude, hEtage, hRaum, hNummer):
        self.hGebaeude  = hGebaeude
        self.hEtage     = hEtage
        self.hRaum      = hRaum
        self.hNummer    = hNummer
    
    def ipTeileZuHostanteil(self):
        self.tuple1 = int(str(self.hGebaeude).rjust(3, "0") + str(self.hEtage).rjust(3, "0") + str(self.hRaum).rjust(4, '0')[0:2], 2)
        self.tuple2 = int(str(self.hRaum).rjust(4, '0')[2:4] + str(self.hNummer).rjust(6, '0'), 2)
        return 'IP: 10.0.' + str(self.tuple1) + '.' + str(self.tuple2)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()                  # Rufe die Klasse auf
        uic.loadUi('userinterface.ui', self)        # Lade die UI Datei
        self.show()                                 # GUI anzeigen


app = QtWidgets.QApplication(sys.argv)              # Erzeuge eine Instanz von QtWidgets.QApplication
window = Ui()                                       # Erzeuge eine Instanz unserer Klasse (Ui)


#Funktion, um die IP/PC in das jeweils andere umzuwandeln
def umrechnen(wert):
    if(window.ipzupc.isChecked() == True):                                          #Je nach angeklicktem Radio Button wird ein Teil von if ausgeführt

        parts =         window.angefragteIP.text().split('.')                       #eingegebene IP wird an den Punkten in Abschnitte eingeteilt
        hostanteil =    bin(int(parts[2])).replace("0b", "").rjust(8, "0")             
                        + bin(int(parts[3])).replace("0b", "").rjust(8, "0")

        neuerPC = PC(   hostanteil[0:3],
                        str(int(hostanteil[4:6], 2)),
                        str(int(hostanteil[7:10].lstrip('0'), 2)),
                        str(int(hostanteil[11:16], 2))
                    )
        print(hostanteil)
        print(neuerPC.etage)
      
        def switch(gebaeude):
            return {
                '000': 'A',
                '001': 'B',
                '010': 'C',
                '011': 'D',
                '100': 'E'
                }.get(neuerPC.gebaeude, "Falsche eingabe")

        if(int(neuerPC.raum) < 10):
            neuerPC.raum = '0' + neuerPC.raum


        ergebnis = 'PC-Standort: ' + switch(neuerPC.gebaeude) + ' ' + neuerPC.etage  + neuerPC.raum + ' - ' + neuerPC.nummer
        
        window.teErgebnis.setText(ergebnis)
        

    elif(window.pczuip.isChecked() == True):
        
            
            neuerPC = PC(   window.angefragterPCgebaeude.currentText(),
                            window.angefragterPCetage.currentText(),
                            window.angefragterPCraum.text(),
                            window.angefragterPCnummer.text()
                        )

            if(neuerPC.etage == 'E'):           # Wandelt Eingabe "E" in 0 um
                neuerPC.etage = 0

            
            #---------------------------#
            #    GEBäUDE SWITCH CASE    #
            #---------------------------#

            def gebaeude_switch(gebauede):                  # Start Switch-Case
                return{         
                        'A':'000',                          # Gebäude A  
                        'B':'001',                          # Gebäude B
                        'C':'010',                          # Gebäude C
                        'D':'011',                          # Gebäude D 
                        'E':'100'                           # Gebäude E
                    }.get(neuerPC.gebaeude, "Invalid input.")       # Wenn keins der Werte ausgewählt wird, "Invalid input." ausgeben.

            #---------------------------#
            #    IN BINäR UMWANDELN     #
            #---------------------------#

            neuerPC.gebaeude    = str(gebaeude_switch(neuerPC.gebaeude))
            neuerPC.etage    = str(bin(int(neuerPC.etage))).replace("0b", "")
            neuerPC.raum        = str(bin(int(neuerPC.raum))).replace("0b", "")
            neuerPC.nummer      = str(bin(int(neuerPC.nummer))).replace("0b", "")
            
            #----------------------------#
            # ZUSAMMENSETZEN & REPLACEN  #
            #----------------------------#

            #neueIP = IP (neuerPC.gebaeude, neuerPC.etage, neuerPC.raum, neuerPC.nummer)
            nH = Hostanteil(neuerPC.gebaeude, neuerPC.etage, neuerPC.raum, neuerPC.nummer)
    
            window.teErgebnis.setText(nH.ipTeileZuHostanteil())
        
    now = datetime.datetime.now()
        
    file = open("log.txt","a")
    file.write("/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ \n")
    file.write("Zeitstempel: " + now.strftime("%d.%m.%Y %H:%M:%S") + "\n\n")
    if(window.ipzupc.isChecked() == True):
        file.write("eingegebene ")
        file.write('IP: ' + window.angefragteIP.text() + "\n\n")
    else:
        file.write(window.teErgebnis.toPlainText() + "\n\n")

    if(window.pczuip.isChecked() == True):
        file.write("eingegebener ")
        file.write("PC: " + window.angefragterPCgebaeude.currentText()
        + ' '
        + window.angefragterPCetage.currentText()
        + window.angefragterPCraum.text().rjust(2, '0')
        + ' - '
        + window.angefragterPCnummer.text()
        + "\n\n")
    else:
         file.write("PC: " + window.teErgebnis.toPlainText() + "\n\n")
    file.write("Von Moritz und Luca \n")
    file.write('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ \n\n\n')
    file.close()

window.btnUmrechnen.clicked.connect(umrechnen)      # Legt fest, dass bei Knopfdruck die Funktion "umrechnen()" ausgeführt wird
app.exec_()                                         # Starte die Anwendung

