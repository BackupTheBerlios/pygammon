import random
class Wuerfel:
    def __init__(self,x,y,z, id):
        #aktuelle Zahl
        self.zahl=6
        # Position
        self.X=x
        self.Y=y
        self.Z=z
        #Texturen
        self.wurfels_ID=id
        self.image_names=["eins.jpg","zwei.jpg","drei.jpg","vier.jpg","fuenf.jpg","sechs.jpg"]
        self.dice_koor=[]
        s=0.5 #seitenlaenge
        self.dice_koor.append([[-s, -s,  s],[ s, -s,  s],[ s,  s,  s],[-s,  s,  s]])# Front Face     = 1
        self.dice_koor.append([[-s, -s, -s],[-s, -s,  s],[-s,  s,  s],[-s,  s, -s]])# Top Face       = 2
        self.dice_koor.append([[-s, -s, -s],[ s, -s, -s],[ s, -s,  s],[-s, -s,  s]])# Right face     = 3
        self.dice_koor.append([[-s,  s, -s],[-s,  s,  s],[ s,  s,  s],[ s,  s, -s]])# Left Face      = 4
        self.dice_koor.append([[ s, -s, -s],[ s,  s, -s],[ s,  s,  s],[ s, -s,  s]])# Bottom Face    = 5
        self.dice_koor.append([[-s, -s, -s],[-s,  s, -s],[ s,  s, -s],[ s, -s, -s]])# Back Face      = 6
        #Rotationskontrolle
        self.rot    =0
        self.zahlen=[0,33.5/3,21.2/3,43.2/3,90.0/3,69.5/3,57.5/3]
        # erste umdrehung 4 90.0/3# 2 118.2
        self.rotart=1
    
    def wuerfeln(self):
        self.rot    =0
        self.zahl=random.randint(1,6)
        if [1,2,5,6].count(self.zahl) == 1: self.rotart = 1
        else: self.rotart = 0

        self.X=-self.zahlen[self.zahl]
        self.Y=6

        if self.wurfels_ID:
            self.Z=3
        else:
            self.Z=0
        return self.zahl
