from Graphic import *
from Wuerfel import *
from Spielstein import *
from Spielfeld import *
from Spielbrett import *
from thread import *
from time import sleep
import copy
#from sys import *



class Pygammon:
    def __init__(self):
        self.Wuerfel=[] # enthält beide Würfelinstanzen
        self.Wuerfel.append(Wuerfel(-10.0,6,0.0,1))
        self.Wuerfel.append(Wuerfel( -20.0,6,3.0,0))
        
        self.Spielsteine=[] # Liste der Spielsteininstanzen
        self.Spielfelder=[] # Liste der Spielfeldinstanzen
        self.Spielbrett=Spielbrett() # Erzeugung des Spielbretts
 
        self.Graphic=Graphic(self) # Erzeugung der Graphikinstanz
        

        self.initGame()# Spiel wird initialisiert

        
        self.spieler={"black":Spieler(),"white":Spieler()}
        
        self.actSpieler="black"
        
        self.wuerfeln()
	self.Graphic.initGL() # Initialiserung der OpenGL-Komponente
	
        #self.gameRound()

        
                

    def initGame(self):
        # Wir legen nun erstmal alle nötigen Spielobjekte an
        #self.Spielbrett.laenge=20

	self.einspiel={}
        self.einspiel['black']=Spielfeld(-1.75,0.0,9.0,0)
	self.einspiel['white']=Spielfeld(-1.75,0.0,-9.0,24)
        self.ausspiel={}
        self.ausspiel['black']=Spielfeld(7.75,0.0,-9.0,24)
        self.ausspiel['black'].breite=2.5
	self.ausspiel['white']=Spielfeld(7.75,0.0,9.0,0)
	self.ausspiel['white'].breite=2.5


        self.Spielfelder.append(self.einspiel['white'])
        for i in range(6): 
            self.Spielfelder.append(Spielfeld(5.4+i*-1.20,0.0,9.0,len(self.Spielfelder)))        
        for i in range(6): 
            self.Spielfelder.append(Spielfeld(-2.9+i*-1.20,0.0,9.0,len(self.Spielfelder)))
        for i in range(6): 
            self.Spielfelder.append(Spielfeld(-8.95+i*1.20,0.0,-9.0,len(self.Spielfelder)))
        for i in range(6): 
            self.Spielfelder.append(Spielfeld(-0.6+i*1.20,0.0,-9.0,len(self.Spielfelder)))    
        self.Spielfelder.append(self.einspiel['black'])
            
        weisse=[]
        schwarze=[]
        
        for i in range(15):
            x=Spielstein(0.0,0.0,0.0,"black")
            self.Spielsteine.append(x)
            schwarze.append(x)

        for i in range(15):
            x=Spielstein(0.0,0.0,0.0,"white")
            self.Spielsteine.append(x)
            weisse.append(x)

        def giveWhite():
            i=weisse[0]
            weisse.remove(i)
	    self.Graphic.weisseSteine.append(i)
            return i

        def giveBlack():
            i=schwarze[0]
            schwarze.remove(i)
	    self.Graphic.schwarzeSteine.append(i)
            return i        

        for i in range(2):
            self.Spielfelder[24].insertStein(giveWhite())
        for i in range(5):
            self.Spielfelder[19].insertStein(giveBlack())       
        for i in range(3):
            self.Spielfelder[17].insertStein(giveBlack())
        for i in range(5):
            self.Spielfelder[13].insertStein(giveWhite())   
        for i in range(5):
            self.Spielfelder[12].insertStein(giveBlack())      
        for i in range(3):
            self.Spielfelder[8].insertStein(giveWhite())
        for i in range(5):
            self.Spielfelder[6].insertStein(giveWhite())
        for i in range(2):
            self.ausspiel['black'].insertStein(giveBlack())


    def whichField(self,stein):
    	# Diese Methode prüft anhand der Koordinaten des gedraggten Spielsteins, über welchem Spielfeld er gerade liegt.
	# Die Prüfung, ob der Zug auf dieses Feld erlaubt ist, findet anderswo statt
	# Übergeben wird eine Spielsteininstanz
	print stein.koordinaten
	print stein.X 
        for i in self.Spielfelder:           
           if stein.Z<0 and i.Z<0:
               if stein.X-0.2<i.X and stein.X-0.2>i.X-i.breite:
                    return i
           elif stein.Z>0 and i.Z>0:
               if stein.X-0.2<i.X and stein.X-0.2>i.X-i.breite:
                   return i
        """        
        i=self.ausspiel['black']
        if stein.Z>0 and i.Z>0:        
              if stein.X-0.2<i.X and stein.X-0.2>i.X-i.breite:
                    return i

        i=self.ausspiel['white']
        if stein.Z<0 and i.Z<0:        
              if stein.X-0.2<i.X and stein.X-0.2>i.X-i.breite:
                    return i
        """
        print "Stein wurde über keinem Spielfeld abgelegt"

    def gameRound(self):
            #Diese Methode wird nach jedem Spielzug aufgerufen und prüft diverse Spielbedingungen
	    
	    # Checken wir, ob jemand gewonnen hat
	    if self.spieler[self.actSpieler].wievielAusgespielt>=15:
            # der Kerl hat gewonnen
            	pass
		
	   # Die Runde ist erst zuende, wenn beide Würfel benutzt wurden
	   
	    if self.Wuerfel[0].zahl==0 and self.Wuerfel[1].zahl==0 and not self.Graphic.gewurfelt:
	   	pass
	    else:
	    	print "Gewuerfelt sind "+str(self.Wuerfel[0].zahl)+" und "+str(self.Wuerfel[1].zahl)
	   	return 0
		
	    self.wuerfeln()
	   
	    if self.actSpieler=="black":
            	self.actSpieler="white"
		print "Spieler Weiss ist am Zug"
	    else:
            	self.actSpieler="black"
		print "Spieler Schwarz ist am Zug"

        	
	    
    def checkAll(self,stein,feld):
    	   # Diese Methode wird aufgerufen, bevor ein Spielzug vom System akzeptiert wird.
	   # Sie prüft, ob das Setzen des Steins nach den Spielregeln erlaubt ist
	   
	    if feld==None: return 0
	   
	    if feld.size()>=2: # checkt, ob das Zielfeld belegt ist; dazu muss nur der letzte Stein geprüft werden, wenn das Feld mehr oder gleich zwei Steine bereits beinhaltet
	    	if feld.Spielsteine[feld.size()-1].farbe!=stein.farbe:
			print "Spielfeld von anderem Spieler blockiert"
			return 0               
           
            if self.actSpieler=='black':# je nachdem welcher spieler am zug ist durch negieren links-oder rechtsherum gehen
                wuerfel=[-self.Wuerfel[0].zahl,-self.Wuerfel[1].zahl]
            else:
                wuerfel=[self.Wuerfel[0].zahl,self.Wuerfel[1].zahl]
            
	    zug=[stein.spielfeld.nr,feld.nr]
            
	    print "Zug von Spielfeld "+str(stein.spielfeld.nr)+" nach Spielfeld "+str(feld.nr)
            weg=[]  #liste mit moeglichen kombinationen die mit den gewuerfelten zahlen moeglich sind
            lenwuerfel=len(wuerfel)
            if lenwuerfel==1:                               ###
                weg.append([wuerfel[0]])                    #
            elif lenwuerfel==2:                             #
                weg.append([wuerfel[0]])                    #
                weg.append([wuerfel[1]])                    # erstellen der liste weg, doppelte kombinationen werden nicht 
                weg.append([wuerfel[0],wuerfel[1]])         # ausgeschlossen, dies wird spaeter behandelt
                weg.append([wuerfel[1],wuerfel[0]])         #
            else:                                           # wenn len(wuerfel)>2 ist wird von einem pasch ausgegangen
                for i in range(1,len(wuerfel)+1):           #
                    weg.append(wuerfel[0:i])

            zuglaenge=(zug[0]-zug[1])  # betrag der laenge des weges von start nach ziel
           
            nWeg=[]
            
            for i in wuerfel:            #
                if i==zuglaenge:#  wegkombinationen mit denen das ziel von der laenge her nciht zu erreichen ist entfernen
                     nWeg.append(i)  #
            weg=nWeg                 
	    
            if len(weg):                   ###
                for i in weg:      # sind immer noch erlaubte kombinationen uebrig, so werden die noetigen zuege fuer die 
                   if self.Wuerfel[0].zahl==abs(i):
		   	self.Wuerfel[0].zahl=0
                   else:
		  	self.Wuerfel[1].zahl=0
		   break
            else:
	        print "Zielfeld nicht mit diesen Würfelzahlen erreichbar"
                return 0
            
            self.gameRound()	    
	    return 1

    def wuerfeln(self):
        zahl1=self.Wuerfel[0].wuerfeln()
        zahl2=self.Wuerfel[1].wuerfeln()
	start_new_thread(wurfel_timer,(self.Graphic,))
        self.Graphic.gewurfelt=1
	print "Gewuerfelt wurden "+str(zahl1)+" und "+str(zahl2)
        
     
	    
    def checkAfter(self,stein):
    	# Diese Methode soll einige Fälle prüfen, die nach dem Ziehen eines Steins eintreten können
	
	# Wir prüfen, ob ein Stein rausgeschubst wurde
	if stein.spielfeld.size()==2:
		first=stein.spielfeld.Spielsteine[0]
		if first.farbe!=stein.farbe:
			first.spielfeld.removeStein(first)
			self.einspiel[first.farbe].insertStein(first)
	    
    def isDragable(self,stein): # Diese Funktion überpüft, ob ein Stein bewegt werden kann
    	if not stein.isDragable():
		return 0
	if not self.actSpieler == stein.farbe:
		return 0
	return 1

            
class Spieler:
    def __init__(self):
        self.ausgespielt=0
        self.einzuspielen=0

    def einerAusgespielt(self):
        self.ausgespielt+=1

    def wievielAusgespielt(self):
        return self.ausgespielt

def wurfel_timer(Graphic):
    # Spezifikation:
    # Nach Ablauf der Zeit wird die Variable Graphic.gewurfelt auf 0 gesetzt
    # Nun wird der Wuerfel nach unten verschoben (Graphic.zeichne_Wuerfel_unten())
    sleep(8)
    Graphic.gewurfelt=0
    # wegen Bug: werden zwei steine gespielt bevor die wuerfel nach unten gelangen
    # entsteht ein Fehler. Loesung: wurde gezogen werden die Steine nicht nach unten
    # verschoben sondern neu gewuerfelt
    if Graphic.pygammon.Wuerfel[0].zahl==0 and Graphic.pygammon.Wuerfel[1].zahl==0:
        Graphic.pygammon.wuerfeln()
    
x=Pygammon()

