############################################################
# Luca Schmitz und Moritz Wildenhain                       #
# Python Programm #1                                       #
# Erstellt: 18.09.2020                                     #
# Letzte änderung: 20.09.2020                              #
# IP und PC suche                                          #
# https://moodle.fds-limburg.de/mod/page/view.php?id=49949 # 
############################################################

   #-----------------------------#
   #           Imports           #
   #-----------------------------#

import sys
#from sys import *
#from sys import argv
from pathlib import Path
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLabel,QLineEdit,QApplication, QComboBox, QMainWindow,QPushButton,QRadioButton
from PyQt5 import QtGui
from PyQt5.QtGui import QFont


def main():

    angefragterPC = ""
    
  

    def clicked():
        if ipzupc.isChecked() == True:
            angefragteIP = angefragteIPL.text()
            parts = angefragteIP.split('.')
            hostanteil = bin(int(parts[2])).replace("0b", "").rjust(8, "0") + bin(int(parts[3])).replace("0b", "").rjust(8, "0")
            gebäude = hostanteil[0:3]
            etage = hostanteil[4:6].replace('0', '')
            raum = hostanteil[7:10].lstrip('0')
            pcnummer = str(int(hostanteil[11:16], 2))


            def switch(gebäude):
                return {
                    '000': 'A',
                    '001': 'B',
                    '010': 'C',
                    '011': 'D',
                    '100': 'E'
                    }.get(gebäude, "Falsche eingabe")

            #ergebnis = str("Ergebnis: " + angefragterPCGebäude.currentText() + angefragterPCStock.currentText() + angefragterPCRaum.text() + angefragterPCPC.text())
            ergebnis = 'Gebäude: ' + switch(gebäude) + ', Etage: ' + etage + ', Raum: ' + raum + ', PC: ' + pcnummer
            
            print(ergebnis)
            
            
        elif pczuip.isChecked() == True:
        
            #---------------------------#
            #     Eingabe verwerten     #
            #---------------------------#
            angefragterPC = angefragterPCGebäude.currentText() + '.' + angefragterPCStock.currentText() + '.' + angefragterPCRaum.text() + '.' + angefragterPCPC.text()
            parts = angefragterPC.split('.')
            gebäude = parts[0]
            stockwerk = parts[1]
            raum = parts[2]
            pc = parts[3]

            #---------------------------#
            #  SWITCH CASE PREPARATION  #
            #---------------------------#

            if gebäude == "A":                         # If Else um die gegeben Werte in Zahlen für das folgende Switch Case umwandeln.
                nGeb = 1
            elif gebäude == "B":
                nGeb = 2
            elif gebäude == "C":
                nGeb = 3
            elif gebäude == "D":
                nGeb = 4
            elif gebäude == "E":
                nGeb = 5
                
            #---------------------------#
            #    GEBäUDE SWITCH CASE    #
            #---------------------------#

            def gebäude_switch(nGeb):                  # Start Switch-Case
                return{         
                        1:'000',                        # Gebäude A  
                        2:'001',                        # Gebäude B
                        3:'010',                        # Gebäude C
                        4:'011',                        # Gebäude D 
                        5:'100'                         # Gebäude E
                    }.get(nGeb, "Invalid input.")       # Wenn keins der Werte ausgewählt wird, "Invalid input." ausgeben.

            #---------------------------#
            #    IN BINäR UMWANDELN     #
            #---------------------------#

            stockwerkIP = bin(int(stockwerk))
            raumIP = bin(int(raum))
            pcIP= bin(int(pc))

            #----------------------------#
            # ZUSAMMENSETZEN & REPLACEN  nigga u gay#
            #----------------------------#

            ergebnis = (str(gebäude_switch(nGeb))) + (str(stockwerkIP)) + (str(raumIP)) + (str(pcIP))
            ergebnis = 'Ergebnis: ' + ergebnis.replace('0b', "")
            print(ergebnis)
        
            
        try:
            ergebnisL.setText(ergebnis)
            ergebnisL.adjustSize()
        except:
            ergebnisL.setText("Ungültige Eingabe")
            ergebnisL.setObjectName('ergebnisL')
            ergebnisL.setStyleSheet("QLabel#ergebnisL {color: red}")
            ergebnisL.adjustSize()




    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200,200,300,160) 
    #print(str(Path(__file__).parent.absolute()) + '\laptop.png')
    win.setWindowIcon(QtGui.QIcon(str(Path(__file__).parent.absolute()) + '\laptop.ico'))
    win.setWindowTitle("Aufgabe: IP-Konverter") 

    
    #Erste Zeile
    labelIP = QLabel(win)
    labelIP.setText("IP")
    labelIP.move(10, 10)  
    
    angefragteIPL = QLineEdit(win)
    angefragteIPL.setInputMask('000.000.000.000')
    angefragteIPL.setGeometry(100,10,100,30)
    
    #Zweite Zeile
    labelPC = QLabel(win)
    labelPC.setText("Zu suchender PC")
    labelPC.move(10, 40)  
    
    angefragterPCGebäude = QComboBox(win)
    angefragterPCGebäude.addItem("A")
    angefragterPCGebäude.addItem("B")
    angefragterPCGebäude.addItem("C")
    angefragterPCGebäude.addItem("D")
    angefragterPCGebäude.addItem("E")
    angefragterPCGebäude.setGeometry(100,40,30,30)
    
    angefragterPCStock = QComboBox(win)
    angefragterPCStock.addItem("3")
    angefragterPCStock.addItem("2")
    angefragterPCStock.addItem("1")
    angefragterPCStock.addItem("E")
    angefragterPCStock.addItem("U")
    angefragterPCStock.setGeometry(130,40,30,30)
    
    angefragterPCRaum = QLineEdit(win)
    angefragterPCRaum.setInputMask('0000000')
    angefragterPCRaum.setGeometry(160,40,30,30)
    
    angefragterPCPC = QLineEdit(win)
    angefragterPCPC.setInputMask('0000000')
    angefragterPCPC.setGeometry(190,40,30,30)
    
    
    #Dritte Zeile
    b1 =  QPushButton('Suche', win)
    b1.setGeometry(200,80,70,30)
    b1.clicked.connect(clicked)
    
    ipzupc = QRadioButton("IP zu PC", win);
    ipzupc.move(10,80)
    pczuip = QRadioButton("PC zu IP", win);
    pczuip.move(110,80)
    
    
    #Vierte Zeile
    ergebnisL = QLabel("Ergebnis:", win)
    ergebnisL.setFont(QFont('Arial', 10))
    ergebnisL.adjustSize()
    ergebnisL.move(10,120)
    
    
    
   
    win.show()
    sys.exit(app.exec_())
    


main()











   # ---------------------------#
            # Eingabe          #
   # ---------------------------#

# angefragteIP = input("Bitte geben Sie eine IP[XXX.XXX.XXX.XXX] oder einen PC [GEBäUDE].[STOCKWERK].[RAUM].[PC]: ")



# if angefragteIP1.isnumeric(): #Falls es sich darum handelt einen PC anhand einer IP zu finden

    
    
# elif angefragteIP1.isnumeric() == False: #Falls es sich darum handelt eine IP zu finden anhand des PCs

    # #---------------------------#
    # #     Eingabe verwerten     #
    # #---------------------------#

    # parts = angefragteIP.split('.')
    # gebäude = parts[0]
    # stockwerk = parts[1]
    # raum = parts[2]
    # pc = parts[3]

    # #---------------------------#
    # #  SWITCH CASE PREPARATION  #
    # #---------------------------#

    # if gebäude == "A":                         # If Else um die gegeben Werte in Zahlen für das folgende Switch Case umwandeln.
        # nGeb = 1
    # elif gebäude == "B":
        # nGeb = 2
    # elif gebäude == "C":
        # nGeb = 3
    # elif gebäude == "D":
        # nGeb = 4
    # elif gebäude == "E":
        # nGeb = 5
        
    # #---------------------------#
    # #    GEBäUDE SWITCH CASE    #
    # #---------------------------#

    # def gebäude_switch(nGeb):                  # Start Switch-Case
        # return{         
                # 1:'000',                        # Gebäude A  
                # 2:'001',                        # Gebäude B
                # 3:'010',                        # Gebäude C
                # 4:'011',                        # Gebäude D 
                # 5:'100'                         # Gebäude E
            # }.get(nGeb, "Invalid input.")       # Wenn keins der Werte ausgewählt wird, "Invalid input." ausgeben.

    # #---------------------------#
    # #    IN BINäR UMWANDELN     #
    # #---------------------------#

    # stockwerkIP = bin(int(stockwerk))
    # raumIP = bin(int(raum))
    # pcIP= bin(int(pc))

    # #----------------------------#
    # # ZUSAMMENSETZEN & REPLACEN  #
    # #----------------------------#

    # hostanteil = (str(gebäude_switch(nGeb))) + (str(stockwerkIP)) + (str(raumIP)) + (str(pcIP))
    # hostanteil = hostanteil.replace('0b', "")
    # print(hostanteil)
# else:
    # print("Wert konnte nicht gefunden werden")