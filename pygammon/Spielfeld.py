import copy

class Spielfeld:
    def __init__(self,X,Y,Z,nr):
        self.X=X
        self.Y=Y
        self.Z=Z
        self.nr=nr
        self.laenge=9.0
        self.breite=1.2
        
        self.farbe=0
        self.Spielsteine=[]

    def insertStein(self,stein):
    	offset=len(self.Spielsteine)
        if offset/5>=1:
            y=0.2*(offset/5)
	    offset-=5*(offset/5)
	else:
		y=0
	
        self.Spielsteine.append(stein)
        stein.setField(self)
        if self.Z>0:
            stein.move((self.X,0.2+y,self.Z-offset*1.5))
        else:
            stein.move((self.X,0.2+y,self.Z+offset*1.5))

    def removeStein(self,stein):
        self.Spielsteine.remove(stein)
        new=[]
        for i in self.Spielsteine:
            new.append(i)
        self.Spielsteine=[]

        for i in new:
            self.insertStein(i)

    def getSteine(self):
        return copy.deepcopy(self.Spielsteine)

    def isFull(self):
        if len(self.Spielsteine)>=5:
            return 1
        else:
            return 0
	    
    def size(self):
     	return len(self.Spielsteine)
        
        
