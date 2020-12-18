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
    
    def gibPcAus(self):                             #gibt in einem String den Standort des PC's im gängigen Format der Raumbenennung der FDS aus
        return str(self.gebaeude) + ' ' + str(self.etage)  + str(self.raum) + ' - ' + str(self.nummer)

#Diese Klasse beinhaltet alles, damit der Hostanteil der IP verarbeitet werden kann
class Hostanteil():
    def __init__(self, hGebaeude, hEtage, hRaum, hNummer):
        self.hGebaeude  = hGebaeude
        self.hEtage     = hEtage
        self.hRaum      = hRaum
        self.hNummer    = hNummer
    
    def ipTeileZuHostanteil(self):                  #Wandelt die vier Teile der IP in zusammenhängende Tupel um. (PC zu IP)
        self.tuple1 = int(str(self.hGebaeude).rjust(3, "0") + str(self.hEtage).rjust(3, "0") + str(self.hRaum).rjust(4, '0')[0:2], 2)
        self.tuple2 = int(str(self.hRaum).rjust(4, '0')[2:4] + str(self.hNummer).rjust(6, '0'), 2)
        return 'IP: 10.0.' + str(self.tuple1) + '.' + str(self.tuple2)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()                  # Rufe die Klasse auf
        uic.loadUi('userinterface.ui', self)        # Lade die UI Datei
        self.show()                                 # GUI anzeigen
    
class InfoFenster(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()                          # Rufe die Klasse auf
        uic.loadUi('info.ui', self)                 # Lade die UI Datei
        self.show()                                 # GUI anzeigen

app = QtWidgets.QApplication(sys.argv)              # Erzeuge eine Instanz von QtWidgets.QApplication
window = Ui()                                       # Erzeuge eine Instanz unserer Klasse (Ui)


#Funktion, um die IP/PC in das jeweils andere umzuwandeln
def umrechnen(wert):
    if(window.ipzupc.isChecked() == True):                                          #Je nach angeklicktem Radio Button wird ein Teil von if ausgeführt

        parts =         window.angefragteIP.text().split('.')                       #eingegebene IP wird an den Punkten in Abschnitte eingeteilt
        hostanteil =    (bin(int(parts[2])).replace("0b", "").rjust(8, "0")         #die letzten beiden Tupel der IP werden mit fehlenden Nullen gefüllt    
                        + bin(int(parts[3])).replace("0b", "").rjust(8, "0"))       #und dann aneinandergehängt, dann weiter verarbeitet

        #neues Objekt der Klasse "PC" erzeugen und Werte zuweisen
        neuerPC = PC(   hostanteil[0:3],
                        str(int(hostanteil[4:6], 2)),
                        str(int(hostanteil[7:10].lstrip('0'), 2)),
                        str(int(hostanteil[11:16], 2))
                    )
      
        def switch(gebaeude):                   # Start Switch-Case
            return {                
                '000': 'A',                     # Gebäude A 
                '001': 'B',                     # Gebäude B
                '010': 'C',                     # Gebäude C 
                '011': 'D',                     # Gebäude D
                '100': 'E'                      # Gebäude E 
                }.get(neuerPC.gebaeude, "Falsche eingabe")  # Wenn keiner der Werte ausgewählt wird, "Falsche Eingabe" ausgeben.

        if(int(neuerPC.raum) < 10):
            neuerPC.raum = '0' + neuerPC.raum


        ergebnis = 'PC-Standort: ' + switch(neuerPC.gebaeude) + ' ' + neuerPC.etage  + neuerPC.raum + ' - ' + neuerPC.nummer
        
        window.teErgebnis.setText(ergebnis)
        

    elif(window.pczuip.isChecked() == True):                                #Je nach angeklicktem Radio Button wird ein Teil von if ausgeführt
        
            #neues Objekt der Klasse "PC" erzeugen und Werte zuweisen
            neuerPC = PC(   window.angefragterPCgebaeude.currentText(),
                            window.angefragterPCetage.currentText(),
                            window.angefragterPCraum.text(),
                            window.angefragterPCnummer.text()
                        )

            if(neuerPC.etage == 'E'):           # Wandelt Eingabe "E" in 0 um, weil 'E' nicht in Binär umgewandelt werden kann
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
                    }.get(neuerPC.gebaeude, "Falsche Eingabe")       # Wenn keiner der Werte ausgewählt wird, "Falsche Eingabe" ausgeben.

            #---------------------------#
            #    IN BINäR UMWANDELN     #
            #---------------------------#

            neuerPC.gebaeude    = str(gebaeude_switch(neuerPC.gebaeude))        #hier muss nicht umgewandelt werden, da die im Switch darüber erledigt wird
            neuerPC.etage       = str(bin(int(neuerPC.etage))).replace("0b", "")
            neuerPC.raum        = str(bin(int(neuerPC.raum))).replace("0b", "")
            neuerPC.nummer      = str(bin(int(neuerPC.nummer))).replace("0b", "")
            

            #neueIP = IP (neuerPC.gebaeude, neuerPC.etage, neuerPC.raum, neuerPC.nummer)
            nH = Hostanteil(neuerPC.gebaeude, neuerPC.etage, neuerPC.raum, neuerPC.nummer)
    
            window.teErgebnis.setText(nH.ipTeileZuHostanteil())
        

            #----------------------------#
            #     LOGDATEI SCHREIBEN     #
            #----------------------------#

    now = datetime.datetime.now()                       #ruft aktuelle Zeit ab
        
    file = open("log.txt","a")                          #öffnet Datei "log.txt" oder erstellt diese, falls nicht vorhanden. "a" sagt aus, dass es neuen Text anhängt,
                                                        #was für ein Log vorteilhaft ist
    file.write("/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ \n")   #optischer Trenner ohne Funktion
    file.write("Zeitstempel: " + now.strftime("%d.%m.%Y %H:%M:%S") + "\n\n")    #Legt fest, in welchem Format die Zeit ausgegeben werden soll
    if(window.ipzupc.isChecked() == True):                              #Falls von IP zu PC umgewandelt wird, wird dieser abgearbeitet Block
        file.write("eingegebene ")
        file.write('IP: ' + window.angefragteIP.text() + "\n\n")
    else:
        file.write(window.teErgebnis.toPlainText() + "\n\n")

    if(window.pczuip.isChecked() == True):                              #Falls von PC zu IP umgewandelt wird, wird dieser abgearbeitet Block
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
    file.close()                                                          #beendet die Bearbeitung der Datei und schließt sie

def zeigeInfo():        #Zeigt das Info-Fenster
    global infos
    infos = InfoFenster()

window.btnUmrechnen.clicked.connect(umrechnen)      # Legt fest, dass bei Knopfdruck auf "umrechnen" die Funktion "umrechnen()" ausgeführt wird
window.pushButton.clicked.connect(zeigeInfo)        # Legt fest, dass bei Knopfdruck auf "Info" die Funktion "zeigeInfo" ausgeführt wird
app.exec_()                                         # Starte die Anwendung

