class Spielstein:
    def __init__(self,X,Y,Z,farbe):
        self.X=X
        self.Y=Y
        self.Z=Z
	self.koordinaten=(X,Y,Z)
        self.farbe=farbe
        self.spielfeld=0

        self.status=""

    def move(self,koordinaten):
        self.X=koordinaten[0]
        self.Y=koordinaten[1]
        self.Z=koordinaten[2]
	self.koordinaten=koordinaten

    def setField(self,field):
        self.spielfeld=field

    def isDragable(self):
        if self.spielfeld.Spielsteine[len(self.spielfeld.Spielsteine)-1]!=self:
            return 0
        return 1
        

        
