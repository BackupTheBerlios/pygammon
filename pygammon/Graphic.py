from OpenGL.GL import *
#from OpenGL.GLE import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Image import *
from sys import *
import string,math

quad=gluNewQuadric()
quadratic=gluNewQuadric()
movement=1

bewegen = 0     #bewegen ist eine Kontrollvariable fuer die mouse_motion-Funktion (0->nichts bewegen,1->actObjekt bewegen)
actObject=None  #enthaelt den Index des zu bewegenden Objekts


class Graphic:
    def __init__(self,pygammon):
        self.pygammon=pygammon # Referenz auf die Pygammon-Instanz
        self.Spielbrett=self.pygammon.Spielbrett
        self.Spielsteine=self.pygammon.Spielsteine # Referenz auf die Spielsteinliste
        self.weisseSteine=[]
        self.schwarzeSteine=[]
        self.Spielfelder=self.pygammon.Spielfelder # Referenz auf die Spielfeldliste
        self.Wuerfel=self.pygammon.Wuerfel # Referenz auf die beiden Würfel

        self.mainLookAt=[0.0,0.0,0.0]
        self.mainLookFrom=[0.0,25.0,25.0]
        
        self.lookAt=[0.0,0.0,0.0] # Koordinaten, auf die die Kamera blickt
        self.lookFrom=[0.0,25.0,25.0] # Position der Kamera
	
	self.textdisplay=""
        self.ordtextdisplay=""
	
        self.cursor=[0,0.2,0]
        self.cursorfarbe=(1,0,0)
        self.gewurfelt=None
        self.height=500
        self.width=500

        self.writeText("Hallo\n Du da")
        


    def drag(self): # callback methode für die Maussteuerung (mouseclick)
        global bewegen,actObject
        actObject   =   self.testIf_Object(self.cursor)
        if actObject==-1:
		bewegen=0
        else:
	    if self.pygammon.isDragable(self.Spielsteine[actObject]):
		bewegen=1   # Ab jetzt kann das Objekt bewegt werden
		self.cursorfarbe=(0,1,0)
            

    def drop(self): # weitere callback Methode für die Maussteuerung (mouseup)
        global bewegen
	if bewegen==1:
		activeObject=self.Spielsteine[actObject]
		feld=self.pygammon.whichField(activeObject)
		
		if feld!=None and self.pygammon.checkAll(activeObject,feld):
			activeObject.spielfeld.removeStein(activeObject)
			feld.insertStein(activeObject)
			self.pygammon.checkAfter(activeObject)
		else:
			activeObject.spielfeld.removeStein(activeObject)
			activeObject.spielfeld.insertStein(activeObject)
		
		bewegen=0
		self.cursorfarbe=(1,0,0)

    def writeText(self,text):
    	self.textdisplay=text
	self.ordtextdisplay=map(ord,text)
	    
    def zeichneAlles(self):
        glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Bildschirm löschen
        glEnable(GL_DEPTH_TEST)
        # Kommen wir zum Spielinhalt
        self.zeichneSpielbrett()
        self.zeichneSpielsteine()
        if self.gewurfelt: 
            self.zeichneWuerfel()
        elif self.gewurfelt==0:
            self.wurfel_unten_zeichnen()
        self.zeichneText()
        self.zeichneCursor()
	# Zeichnen wir's auf den Bildschirm        
        glutSwapBuffers()

        

    def zeichneSpielbrett(self):
        glLoadIdentity()
        
        gluLookAt(self.lookFrom[0],self.lookFrom[1],self.lookFrom[2], self.lookAt[0],self.lookAt[1],self.lookAt[2] ,0.0,1.0,0.0)
        #das feld selbst:
        quadralaenge=self.Spielbrett.laenge/2.0
        nquadralaenge=-quadralaenge
        glBindTexture(GL_TEXTURE_2D, self.texturen["brett.jpg"])   
        glBegin(GL_POLYGON)
	glTC2f=glTexCoord2f
	glV3f=glVertex3f
        glTC2f(0.0, 0.0); glV3f(nquadralaenge,0.0,nquadralaenge)
        glTC2f(1.0, 0.0); glV3f(quadralaenge,0.0,nquadralaenge)
        glTC2f(1.0, 1.0); glV3f(quadralaenge,0.0,quadralaenge)
        glTC2f(0.0, 1.0); glV3f(nquadralaenge,0.0,quadralaenge)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, self.texturen["holz.jpg"]) 
        #der untere rahmen:
        glBegin(GL_POLYGON)
        glTC2f(0.0, 0.0); glV3f(nquadralaenge,0.0,quadralaenge)
        glTC2f(1.0, 0.0); glV3f(quadralaenge,0.0,quadralaenge)
        glTC2f(1.0, 1.0); glV3f(quadralaenge,-1.0,quadralaenge)
        glTC2f(0.0, 1.0); glV3f(nquadralaenge,-1.0,quadralaenge)
        glEnd()
        

    def zeichneSpielsteine(self):      
        def drawIt(i):
            glPushMatrix()
            glTrans(*i.koordinaten)            
            glRotatef(90.0,1.0,0.0,0.0)            
            gluCylinder(quadrat,0.5,0.5,0.2,16,16)     # Zylinder
            #glTrans(0.0,0.0,-0.2)
            gluDisk(quadrat,0.0,0.5,16,16)
            glPopMatrix()

	glTrans=glTranslatef
	quadrat=quad
            
        glBindTexture(GL_TEXTURE_2D, self.texturen["granitWeiss.jpg"])    
    	map(drawIt, self.weisseSteine)
        glBindTexture(GL_TEXTURE_2D, self.texturen["granitSchwarz.jpg"])
        map(drawIt, self.schwarzeSteine)
	

    
    def zeichneWuerfel(self):
        # Spezifikation:
        # "Einflug" und Rollen der Wuerfel bis zum Stillstand
        for dice in self.Wuerfel:
            glPushMatrix() 
            glTranslatef(dice.X,dice.Y,dice.Z)
            
            glutPostRedisplay()
            #glDisable(GL_ALPHA_TEST)
            if dice.rotart == 1: # Fuer die Zahlen 1, 5 und 6
                glRotatef(dice.rot,1.,0.,0.)
                glRotatef(dice.rot,5.,0.,0.)
                glRotatef(dice.rot,0.,0.,1.)
            else: # Fuer die Zahlen 2, 3 und 4
                glRotatef(dice.rot,1.,0.,0.)
                glRotatef(dice.rot,0.,5.,0.)
                glRotatef(dice.rot,0.,1.,0.)            
	    
            glTC2f=glTexCoord2f
            glV3f=glVertex3f
            
            for i in range(len(dice.dice_koor)):
                glBindTexture(GL_TEXTURE_2D, self.texturen[dice.image_names[i]])
                glBegin(GL_QUADS); 
                actDice=dice.dice_koor[i]   
                glTC2f(0., 0.); glV3f(actDice[0][0],actDice[0][1],actDice[0][2]);
                glTC2f(1., 0.); glV3f(actDice[1][0],actDice[1][1],actDice[1][2]);
                glTC2f(1., 1.); glV3f(actDice[2][0],actDice[2][1],actDice[2][2]);
                glTC2f(0., 1.); glV3f(actDice[3][0],actDice[3][1],actDice[3][2]);
                glEnd();
            glPopMatrix() 
            if dice.X < 1:
                dice.X+=0.09
                dice.rot+=1
                if dice.Y >0.7 and dice.X>-13:
                    dice.Y-=0.08  
                glutPostRedisplay()
            #elif dice.X!=1 and dice.wurfels_ID:                
               

    def wurfel_unten_zeichnen(self):
        # Spezifikation:
        # Verschieben der Wuerfel nach Stillstand nach unten
        wurfel_z=13
        wurfel_x=4
        for dice in self.Wuerfel:
            glPushMatrix()
            if dice.Z<wurfel_z:
                    dice.Z+=0.5
            if dice.X<wurfel_x:
                dice.X+=0.1
            glTranslatef(dice.X,dice.Y,dice.Z)

            if dice.rotart == 1: # Fuer die Zahlen 1, 5 und 6
                glRotatef(dice.rot,1.,0.,0.)
                glRotatef(dice.rot,5.,0.,0.)
                glRotatef(dice.rot,0.,0.,1.)
            else: # Fuer die Zahlen 2, 3 und 4
                glRotatef(dice.rot,1.,0.,0.)
                glRotatef(dice.rot,0.,5.,0.)
                glRotatef(dice.rot,0.,1.,0.)       
            glTC2f=glTexCoord2f
            glV3f=glVertex3f

 
            for i in range(len(dice.dice_koor)):
                glBindTexture(GL_TEXTURE_2D, self.texturen[dice.image_names[i]])
                glBegin(GL_QUADS); 
                actDice=dice.dice_koor[i]   
                glTC2f(0., 0.); glV3f(actDice[0][0],actDice[0][1],actDice[0][2]);
                glTC2f(1., 0.); glV3f(actDice[1][0],actDice[1][1],actDice[1][2]);
                glTC2f(1., 1.); glV3f(actDice[2][0],actDice[2][1],actDice[2][2]);
                glTC2f(0., 1.); glV3f(actDice[3][0],actDice[3][1],actDice[3][2]);
                glEnd();
            glPopMatrix()
            wurfel_z=13
            wurfel_x=2
        
        

    def zeichneCursor(self):
        glPushMatrix()
        glTranslatef(*self.cursor)
        #glRotatef(-135.0,1.0,0.0,0.0)
        
        glDisable(GL_TEXTURE_2D)
        glBegin(GL_POLYGON)
        glColor3f(*self.cursorfarbe)
        glVertex3f( -0.5, 0.8, 0.0)
        glVertex3f(0.5,0.8,0.0)
        glVertex3f(0.0,0.0,0.0)
	
        glEnd()

        #gluCylinder(quadratic,0.,0.2,0.2,8,8)
        glEnable(GL_TEXTURE_2D)
        
        glPopMatrix()
        
    def zeichneText(self):
        glDisable(GL_TEXTURE_2D)
	glColor3f(1,1,1)
	glRasterPos2f(-16,-25)
	for i in self.ordtextdisplay:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, i)
        glPushMatrix()
        glLoadIdentity()
        glEnable(GL_TEXTURE_2D)    
        glPopMatrix()
        
    def mouseMotion(self,winX,winY):
        objX,objZ,objY  =   self.mousecoords2objectcoords((float(winX),float(winY),0.4))
        objX=objX/20        # X-Geschwindigkeit anpassen
        objZ=objZ/20        # Y-Geschwindigkeit-Richtung anpassen
	
        self.cursor=(objX,objY,objZ)
        if bewegen:
            # Umgerechnete Koordinaten dem Objekt uebergeben
	    stein=self.Spielsteine[actObject]
            objY=1.0#-0.2 Achtung
            if self.testIfObject_OutOfArea(objX, objZ)==-1:
                stein.move((objX,objY,objZ))
        else:
	    object=self.testIf_Object(self.cursor)
            if object!=-1:
	    	if self.pygammon.isDragable(self.Spielsteine[object]): 
                	self.cursorfarbe=(0,1,0)
		else:
			self.cursorfarbe=(1,0,0)
            else:
                self.cursorfarbe=(1,0,0)
        glutPostRedisplay()


        

    """
        Die folgenden Funktionen sind für die OpenGL-Funktionalitäten
    """



    def keyboard(self,key, x, y): # Eventhandling
        global movement
        print key
        # Kleines Experiment mit der Kamerasteuerung
        if key==" ":
            if self.lookFrom[1]<30 and self.lookFrom[1]>-30:
                self.lookFrom[1]=self.lookFrom[1]+movement
            else:
                movement=-movement
        elif key=="w"and not self.gewurfelt:
            self.pygammon.wuerfeln()

        elif key=="o":
            self.lookFrom[1]+=0.5
        elif key=="l":
            self.lookFrom[1]-=0.5

        elif key=="g":
            self.text_erstellen("lol!")
        glutPostRedisplay()
            
    def mouse(self,button,state,winX,winY):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:   #Linke Taste gedrueckt
            self.drag()
            self.mouseMotion(winX,winY)
        elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:     #Linke Taste losgelassen
            self.drop()
        glutPostRedisplay()
	    
    def mousecoords2objectcoords(self,mousecoords):
            x,y,z = mousecoords
            y-=self.height/2
            x-=self.width/2
            z=0.2
            return x,y,z

    def PunktInKreis(self,kreismitte, radius, maus):
        abstand = abs(math.sqrt((kreismitte[0]-maus[0])**2+(kreismitte[2]-maus[2])**2))
        #print "Abstand:",abstand
        if abstand <= radius:
            return 1
        return -1
    
    def testIf_Object(self,maus):
        for i in range(0,len(self.Spielsteine)): #Maus- mit Objektkoords vergleichen
            kreismitte= self.Spielsteine[i].koordinaten
            radius=0.5
            if self.PunktInKreis(kreismitte,radius,maus) == 1:
                return i #Maus im Bereich des Objekts i
        return -1
    
    def testIfObject_OutOfArea(self,X,Z):
        laenge=(self.Spielbrett.laenge/2.0)-0.5
        if X<-laenge or X>laenge or Z<-laenge or Z>laenge:#Maus- mit Objektkoords vergleichen
            return 1 #Objekt ausserhalb der erlaubten Area
        return -1 #Objekt innerhalb der erlaubten Area

    def reshape (self, w, h):
        self.width=w
        self.height=h
        if h==0:h=1
        glViewport (0, 0, w, h)
        glMatrixMode (GL_PROJECTION)
        glLoadIdentity ()
        gluPerspective(45.0,w/ h, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        #glTranslatef (-1.8, 0.0, -5.0)



    def load_texture(self,textur):
        image = open(textur)
        ix = image.size[0]
        iy = image.size[1]
        image = image.tostring("raw", "RGBX", 0, -1)
        id=glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, id)   # 2d texture (x and y size)
            
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        return id

    def initGL(self):

        glutInit(argv)
        glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize (500, 500)
        glutInitWindowPosition (0, 0)
        glutCreateWindow ('Pygammon - LK Informatik 2003-2005')

        glClearColor (0.0, 0.0, 0.0,0.0)
        glEnable(GL_TEXTURE_2D)
        #glEnable(GL_BLEND)
        #glEnable(GL_LINE_SMOOTH)
        #glShadeModel (GL_FLAT)
	
	# Deaktiviere den Cursor
        glutSetCursor(GLUT_CURSOR_NONE)
        self.texturen={}
        self.texturen["brett.jpg"]=self.load_texture("brett.jpg")
        self.texturen["holz.jpg"]=self.load_texture("holz.jpg")
        self.texturen["granitWeiss.jpg"]=self.load_texture("granitWeiss.jpg")
        self.texturen["granitSchwarz.jpg"]=self.load_texture("granitSchwarz.jpg")
        self.texturen["eins.jpg"]=self.load_texture("eins.jpg")
        self.texturen["zwei.jpg"]=self.load_texture("zwei.jpg")
        self.texturen["drei.jpg"]=self.load_texture("drei.jpg")
        self.texturen["vier.jpg"]=self.load_texture("vier.jpg")
        self.texturen["fuenf.jpg"]=self.load_texture("fuenf.jpg")
        self.texturen["sechs.jpg"]=self.load_texture("sechs.jpg")
        gluQuadricTexture(quad,1)
        #glMatrixMode(GL_PROJECTION)
        glutDisplayFunc(self.zeichneAlles)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)
        glutIdleFunc(self.zeichneAlles)
        glutMouseFunc(self.mouse)
        glutPassiveMotionFunc(self.mouseMotion)
        glutMotionFunc(self.mouseMotion)
        glutMainLoop()

    #def standard_text(self):        
        


        
