import os
import chunks
import bisect
import Global as G

ArrayEntities    = []
ArrayClouds      = []
entitiesVisibles = []
onDisplay        = 0
Images           = {}

#------------------------------------ {FUNCIONES DE CLASES} ------------------------------------
TREE_IMAGES = [[], [], [], [], []] 

def loadTextures():
    # plantas de Grass
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree0.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree1.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree2.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree3.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree4.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree5.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree6.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree7.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree8.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree9.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree10.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree11.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree12.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree13.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree14.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree15.png"))
    TREE_IMAGES[2].append(loadImage("assets/deco/grass/tree16.png"))

    # plantas de Sand
    TREE_IMAGES[1].append(loadImage("assets/deco/sand/tree0.png"))
    TREE_IMAGES[1].append(loadImage("assets/deco/sand/tree1.png"))
    
    
    print("Grass Trees: "+str(len(TREE_IMAGES[2])))
    print("Sand  Trees: "+str(len(TREE_IMAGES[1])))

#---- {Funcion isVisible}

def updateVisibleEntities():
    global entitiesVisibles, ArrayEntities
    entitiesVisibles = []
    for entitie in ArrayEntities:
        if isVisible(entitie):
            entitiesVisibles.append(entitie)


def isVisible(entitie,margin=200):
    return (G.DISPLAY[0] - margin <= entitie.centerX <= G.DISPLAY[2] + margin and
            G.DISPLAY[1] - margin <= entitie.centerY <= G.DISPLAY[3] + margin)

#---- {Funcion encontrar_entidad_mas_cercana}

def encontrar_entidad_mas_cercana(entitie_Ref):
    entidad_mas_cercana = None
    distancia_minima = float('inf') 
    
    for entidad in ArrayEntities:
        if entidad == entitie_Ref: continue
        dx = entidad.centerX - entitie_Ref.centerX
        dy = entidad.centerY - entitie_Ref.centerY
        distancia_sq = dx**2 + dy**2
        
        if distancia_sq < distancia_minima:
            distancia_minima = distancia_sq
            entidad_mas_cercana = entidad
    
    return entidad_mas_cercana


def genCloud():
    if len(ArrayClouds) < 20:
        val = int(random(1,1000))
        if val == 1:
            cloud()

class cloud():
    centerX = 0
    centerY = 0
    wwidth  = 0
    hheight = 0

    def __init__(self):
        self.centerX = int(random(G.DISPLAY[0]-500, G.DISPLAY[0]-200))
        self.centerY = int(random(G.DISPLAY[1],G.DISPLAY[3]))
        self.wwidth  = int(random(200,600))
        self.hheight = int(random(50,300)) 
        self.vel     = random(0.1,0.3)
        self.a       = int(random(40,100)) 
        
        ArrayClouds.append(self)

    def drawMe(self):
        self.centerX += self.vel 
        rectMode(CENTER)
        fill(255, 255, 255, 40)
        noStroke()
        rect(self.centerX, self.centerY, self.wwidth, self.hheight)
        rectMode(CORNERS)
        if self.centerX > G.DISPLAY[2]+1500:
            ArrayClouds.remove(self)
            del self
            

    
 
        

#------------------------------------ {CLASE ENTITIE} ------------------------------------
class entitie():
    centerX = 0
    centerY = 0
    chunk   = (0,0)
    hb_minX = 0
    hb_minY = 0
    hb_maxX = 0
    hb_maxY = 0
    
    listening_distance = 0
    Vision_distance    = 0
    
    def __init__(self, x=0, y=0, name="null", listening_distance = 0, Vision_distance = 0):
        self.centerX = int(x)
        self.centerY = int(y) 
        self.chunk   = chunks.IDchunk(self.centerX, self.centerY)
        self.name    = name 
        self.RADIO   = 32
        self.listening_distance = listening_distance
        self.Vision_distance = Vision_distance
        
        self.calcularHB()
        index = 0
        while index < len(ArrayEntities) and ArrayEntities[index].centerY < self.centerY:
            index += 1
        ArrayEntities.insert(index, self) 
        
    def calcularHB(self):
        self.hb_minX = int(self.centerX - self.RADIO/2)
        self.hb_minY = int(self.centerY - (self.RADIO))
        self.hb_maxX = int(self.centerX + self.RADIO/2)
        self.hb_maxY = int(self.centerY + self.RADIO/8)
    def drawMe(self):
       
        fill(1,100)
        noStroke()
        ellipse(self.centerX,self.centerY,self.RADIO,self.RADIO/4)
        alpha(1)
        
        fill("#FFFFFF")
        circle(self.centerX,(self.centerY)-self.RADIO/2,self.RADIO)
        fill("#000000")
        textAlign(CENTER)
        textSize(20)
        text(self.name,self.centerX+1,(self.centerY+6)-self.RADIO)
        fill("#FFFFFF")
        
        
        if G.DEBUG_MODE:
            stroke("#FF0000")
            strokeWeight(5)
            point(self.centerX,self.centerY)
            strokeWeight(1)
            stroke("#000000")
            rectMode(CORNERS)
            noFill()
            stroke("#FF0000")
            rect(self.hb_minX,self.hb_minY,self.hb_maxX,self.hb_maxY)
            stroke("#FF0000")
            fill("#FFFFFF")
            
#------------------------------------ {CLASE NPC} ------------------------------------

class NPC(entitie):
    name = ""
    
    centerX = 0
    centerY = 0
    hb_minX = 0
    hb_minY = 0
    hb_maxX = 0
    hb_maxY = 0
    
    
    Vision_distance = 600
    listening_distance = 300
    
    def __init__(self, x=0, y=0, name="null_NPC", listening_distance=0, Vision_distance=0):
        entitie.__init__(self, x, y, name,listening_distance,Vision_distance)
    
    def drawMe(self):
    
        self.calcularHB()  
        fill(1,100)
        noStroke()
        ellipse(self.centerX,self.centerY,self.RADIO,self.RADIO/4)
        alpha(1)
        
        fill("#FFFFFF")
        circle(self.centerX,(self.centerY)-self.RADIO/2,self.RADIO)
        fill("#000000")
        textAlign(CENTER)
        textSize(20)
        text(self.name,self.centerX+1,(self.centerY+6)-self.RADIO)
        fill("#FFFFFF")
        
        if G.DEBUG_MODE:
            stroke("#FF0000")
            strokeWeight(5)
            point(self.centerX+10,self.centerY)
            stroke("#FF0000")
            strokeWeight(5)
            point(self.centerX,self.centerY)
            strokeWeight(1)
            stroke("#000000")
            rectMode(CORNERS)
            noFill()
            stroke("#FF0000")
            rect(self.hb_minX,self.hb_minY,self.hb_maxX,self.hb_maxY)
            stroke("#FF0000")
            fill("#FFFFFF")
            
#------------------------------------ {CLASE OBJETO} ------------------------------------

class objeto(entitie):
    name = ""
    
    centerX = 0
    centerY = 0
    hb_minX = 0
    hb_minY = 0
    hb_maxX = 0
    hb_maxY = 0
    
    #SENTIDOS
    Vision_distance = 0
    listening_distance = 0
    
    def __init__(self, x=0, y=0, name="null_obj"):
        global Images
        entitie.__init__(self, x, y, name)

        if os.path.exists("assets/"+self.name+".png"):
            
            if (self.name in Images.keys()):
                self.img =  Images[self.name]
            else:
                Images[self.name] = loadImage("assets/"+self.name+".png")
                self.img =  loadImage("assets/"+self.name+".png")
                
            hint(12)
            imageMode(CENTER)
            self.img.resize(self.RADIO,self.RADIO) 
            
        else:
            self.img = "null"
            
    
    def drawMe(self):
        valor = cos((frameCount*0.1))*5
        stroke("#000000")
        
        if self.img != "null":
            image(self.img,self.centerX,(self.centerY+valor)-self.RADIO)

        else:
            fill("#FFFFFF")
            circle(self.centerX,(self.centerY+valor)-self.RADIO,self.RADIO)
            fill("#000000")
            textAlign(CENTER)
            textSize(20)
            text(self.name,self.centerX+1,(self.centerY+6+valor)-self.RADIO)
            fill("#FFFFFF")
        
        fill(1,100)
        noStroke()
        ellipse(self.centerX,self.centerY,self.RADIO+valor,self.RADIO/4)
        alpha(1)
        
        if G.DEBUG_MODE:
            stroke("#FF0000")
            strokeWeight(5)
            point(self.centerX,self.centerY)
            strokeWeight(1)
            stroke("#000000")
            rectMode(CORNERS)
            noFill()
            stroke("#FF0000")
            rect(self.hb_minX,self.hb_minY,self.hb_maxX,self.hb_maxY)
            stroke("#FF0000")
            fill("#FFFFFF")

#------------------------------------ {CLASE PLANT} ------------------------------------
class plant(entitie):
    name = ""
    
    centerX = 0
    centerY = 0
    hb_minX = 0
    hb_minY = 0
    hb_maxX = 0
    hb_maxY = 0
    A       = 0
    
    #SENTIDOS
    Vision_distance = 0
    listening_distance = 0
    
    def __init__(self, x=0, y=0, name="null_obj"):
        global Images
        entitie.__init__(self, x, y, name)
        
        if name == "Tree":
            r = int(random(0,len(TREE_IMAGES[2])))
            self.img = TREE_IMAGES[2][r]
        if name == "Platano":
            r = int(random(0,len(TREE_IMAGES[1])))
            self.img = TREE_IMAGES[1][r]
            
        self.A    = 0
        

    def drawMe(self):
        if self.A < 255:
            self.A += 1
            
            
        tint(self.A,255)

        textSize(12)
        stroke("#000000") 
        
        if self.img != "null":
            imageMode(CENTER)
            image(self.img,self.centerX,(self.centerY)-75)
            imageMode(CORNER)
        
        else:
            fill("#FFFFFF")
            circle(self.centerX,(self.centerY)-self.RADIO,self.RADIO)
            fill("#000000")
            textAlign(CENTER)
            textSize(16)
            text(self.name,self.centerX+1,(self.centerY+6)-self.RADIO)
            fill("#FFFFFF")
        
        fill(1,100)
        noStroke()
        alpha(1)
        strokeWeight(1)
        textSize(15)
        
        if G.DEBUG_MODE:
            stroke("#FF0000")
            strokeWeight(5)
            point(self.centerX,self.centerY)
            strokeWeight(1)
            stroke("#000000")
            rectMode(CORNERS)
            noFill()
            stroke("#FF0000")
            rect(self.hb_minX,self.hb_minY,self.hb_maxX,self.hb_maxY)
            stroke("#FF0000")
            fill("#FFFFFF")          
