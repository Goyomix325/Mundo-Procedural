import collections
import entities
import Global as G
#-----{PERLIN VARS}----------

escala = 200.0
valorA = 10000

SEED = 134267920
SEED = int(random(1,1000000))

noiseSeed(SEED)
noiseDetail(6, 0.5)

#----------------------------

ZOOM    = 1
CASILLA = 25
CHUNK   = CASILLA * 16

#----------------------------

chunkList     = []
chunkVisibles = []
textures      = []
grass_decos   = []
water_decos   = []
stone_decos   = []

chunkQueue     = collections.deque()
onDisplay      = 0

#----------------------------

def loadTextures():
    textures.append(loadImage("assets/tiles/water.png"))
    textures[0].resize(CASILLA,CASILLA)
    textures.append(loadImage("assets/tiles/sand.png"))
    textures[1].resize(CASILLA,CASILLA)
    textures.append(loadImage("assets/tiles/grass.png"))
    textures[2].resize(CASILLA,CASILLA)
    textures.append(loadImage("assets/tiles/stone.png"))
    textures[3].resize(CASILLA,CASILLA)
    textures.append(loadImage("assets/tiles/snow.png"))
    textures[4].resize(CASILLA,CASILLA)
    
    stone_decos.append(loadImage("assets/deco/stone/0.png"))
    stone_decos[0].resize(CASILLA,CASILLA)
    
    grass_decos.append(loadImage("assets/deco/grass/0.png"))
    grass_decos[0].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/1.png"))
    grass_decos[1].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/2.png"))
    grass_decos[2].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/3.png"))
    grass_decos[3].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/4.png"))
    grass_decos[4].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/5.png"))
    grass_decos[5].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/6.png"))
    grass_decos[6].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/7.png"))
    grass_decos[7].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/8.png"))
    grass_decos[8].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/9.png"))
    grass_decos[9].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/10.png"))
    grass_decos[10].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/11.png"))
    grass_decos[11].resize(CASILLA,CASILLA)
    grass_decos.append(loadImage("assets/deco/grass/12.png"))
    grass_decos[12].resize(CASILLA,CASILLA)
    
    
    water_decos.append(loadImage("assets/deco/water/0.png"))
    water_decos[0].resize(CASILLA,CASILLA)
    water_decos.append(loadImage("assets/deco/water/1.png"))
    water_decos[1].resize(CASILLA,CASILLA)
    water_decos.append(loadImage("assets/deco/water/2.png"))
    water_decos[2].resize(CASILLA,CASILLA)
    water_decos.append(loadImage("assets/deco/water/3.png"))
    water_decos[3].resize(CASILLA,CASILLA)
    water_decos.append(loadImage("assets/deco/water/4.png"))
    water_decos[4].resize(CASILLA,CASILLA)
    
    
    
    
########################################{ FUNCIONES BASE }##########################################

def updateVisibleChunks():
    global chunkVisibles, chunkList
    chunkVisibles = []
    for chunk in chunkList:
        if isVisible(chunk):
            chunkVisibles.append(chunk)

def isVisible(chunk, margin=200):
    return ((G.DISPLAY[0] - margin) <= chunk.x2 and
            (G.DISPLAY[2] + margin) >= chunk.x1 and
            (G.DISPLAY[1] - margin) <= chunk.y2 and
            (G.DISPLAY[3] + margin) >= chunk.y1)

#------------------------------------------------------------------------------------------------

def processChunkQueue():
    """Cola de procesos para generar un efecto PEPS"""
    global chunkList
    if chunkQueue: 
        x, y = chunkQueue.popleft() 
        chunkList.append(Chunk(x, y))
    
    updateVisibleChunks()
    entities.updateVisibleEntities()

#------------------------------------------------------------------------------------------------

def ruidoInCasilla(casillaID):
    ruido = noise((valorA + casillaID[0]) / escala, (valorA + casillaID[1]) / escala)
    i = 0 
    
    if ruido > 0.66:   i = 4  # Nieve
    elif ruido > 0.62: i = 3  # Piedra 
    elif ruido > 0.39: i = 2  # Tierra
    elif ruido > 0.37: i = 1  # Arena
    else:              i = 0  # Agua
    
    return i

#------------------------------------------------------------------------------------------------

def IDcasilla(pos_X, pos_Y): 
    """Calcula el chunk en el que se encuentra una posicion"""
    return (pos_X//CASILLA, pos_Y//CASILLA)

#------------------------------------------------------------------------------------------------

def PosicionCasilla(casillaID):
    """Calcula la posicion de un chunk en el mapa para dibujarlo """ 
    x1 = casillaID[0] * CASILLA
    y1 = casillaID[1] * CASILLA
    x2 = x1 + CASILLA
    y2 = y1 + CASILLA
    return (x1, y1, x2, y2)

#------------------------------------------------------------------------------------------------

def IDchunk(pos_X, pos_Y): 
    """Calcula el chunk en el que se encuentra una posicion"""
    return (pos_X//CHUNK, pos_Y//CHUNK)

#------------------------------------------------------------------------------------------------

def PosicionChunk(chunkID):
    """Calcula la posicion de un chunk en el mapa para dibujarlo """ 
    
    x1 = chunkID[0] * CHUNK
    y1 = chunkID[1] * CHUNK
    x2 = x1 + CHUNK
    y2 = y1 + CHUNK
    return (x1, y1, x2, y2)

########################################{ FUNCIONES BASE }##########################################

def updateChunks():
    global chunkList, chunkQueue

    chunk_inicial = IDchunk(G.DISPLAY[0], G.DISPLAY[1])
    chunk_final   = IDchunk(G.DISPLAY[2], G.DISPLAY[3])
    
    chunk_dict = {chunk.ID: chunk for chunk in chunkList}
    queue_dict = {str(x)+","+str(y) for x, y in chunkQueue}
    
    for y in range(chunk_inicial[1], chunk_final[1] + 1):
        for x in range(chunk_inicial[0], chunk_final[0] + 1):
            id_chunk = str(x)+","+str(y)
            
            if id_chunk not in chunk_dict and id_chunk not in queue_dict:
                chunkQueue.append((x, y))
    
#------------------------------------------------------------------------------------------------

def runChunks():
    """Arranca el programa cargando N chunks al rededor"""
    global chunkList
    N = 2
    chunk_inicial = (-N, -N)
    chunk_final   = ( N,  N)

    chunk_dict = {chunk.ID: chunk for chunk in chunkList}
    
    for y in range(chunk_inicial[1], chunk_final[1] + 1):
        for x in range(chunk_inicial[0], chunk_final[0] + 1):
            id_chunk = str(x)+","+str(y)
            
            if id_chunk not in chunk_dict:
                chunk_dict[id_chunk] = Chunk(x, y)

    chunkList = list(chunk_dict.values())

#------------------------------------------------------------------------------------------------

def chunksInScreen(x1, y1, x2, y2):
    Chunk_inicial = IDchunk(x1, y1)
    Chunk_final   = IDchunk(x2, y2)
    ChunksArray   = []
    
    for y in range(Chunk_inicial[1], Chunk_final[1] + 1):
        for x in range(Chunk_inicial[0], Chunk_final[0] + 1):
            ID_chunk = (x,y)
            P_CHUNK = PosicionChunk(ID_chunk)
            ChunksArray.append(P_CHUNK)
            
##############################################{ CLASE CHUNK }################################################

class Chunk():
    ID_X = 0
    ID_Y = 0
    ID   = ""
    x1   = 0
    y1   = 0
    x2   = 0
    y2   = 0
    IMG  = ""

    
    def __init__(self,id_x,id_y):
        self.ID_X = id_x
        self.ID_Y = id_y
        self.ID   = str(id_x)+","+str(id_y)
        self.A    = 0

        self.x1,self.y1,self.x2,self.y2 = PosicionChunk((id_x,id_y))
        
        self.IMG = createGraphics(CHUNK, CHUNK, P2D)
                        
        self.IMG.beginDraw()
        
        for y in range(0,CHUNK,CASILLA):
            for x in range(0,CHUNK,CASILLA):
                casilla = IDcasilla(self.x1 + x , self.y1 + y )
                ruido = noise((valorA + casilla[0]) / escala, (valorA + casilla[1]) / escala)
                i = 0 
                detail = False
                
                if ruido > 0.66:  #--------- Nieve
                    i = 4                
                elif ruido > 0.62:#--------- Piedra 
                    i = 3
                    j = int(random(0,1000))
                    if    j == 0: detail = stone_decos[0]
                                      
                elif ruido > 0.39:#--------- Tierra
                    i = 2
                    
                    j = int(random(0,1000))
                    if    j ==  0: detail = grass_decos[0]
                    elif  j ==  1: detail = grass_decos[1]
                    elif  j ==  2: detail = grass_decos[2]
                    elif  j ==  3: detail = grass_decos[3]  
                    elif  j ==  4: detail = grass_decos[4]
                    elif  j ==  5: detail = grass_decos[5]
                    elif  j ==  6: detail = grass_decos[6]  
                    elif  j ==  7: detail = grass_decos[7]
                    elif  j < 128: detail = grass_decos[8]
                    elif  j ==129: detail = grass_decos[9]
                    elif  j ==130: detail = grass_decos[10]
                    elif  j ==131: detail = grass_decos[11]
                    elif  j ==132: detail = grass_decos[12]
          
                 
                elif ruido > 0.37:#--------- Arena
                    i = 1  
                else:#---------------------- Agua
                    i = 0  
                    j = int(random(0,1000))
                    if   j  == 0:   detail = water_decos[0]
                    elif j  == 1:   detail = water_decos[1]
                    elif j  == 2:   detail = water_decos[2]
                    elif j  == 3:   detail = water_decos[3]
                    elif j   < 5:   detail = water_decos[4]
                    

                self.IMG.image(textures[i],x,y)
                if detail:
                    self.IMG.image(detail,x,y)
                
        self.IMG.endDraw()
        
        n = int(random(0,20))

        for _ in range(n):
            ex = int(random(self.x1,self.x2))
            ey = int(random(self.y1,self.y2))
            ruido = ruidoInCasilla(IDcasilla(ex,ey))
            if ruido == 2:
                entities.plant(ex,ey,"Tree")
            if ruido == 1:
                if int(random(0,2))==1:
                    entities.plant(ex,ey,"Platano")
        
        
    def drawChunk(self):
        if self.A < 255:
            self.A += 1
            
        tint(255,self.A)
        
 
        if G.DEBUG_MODE:
            strokeWeight(1.5)
            stroke("#FFFF00")
            noFill()
            rect(self.x1,self.y1,self.x2,self.y2)
            noStroke()
        image(self.IMG, self.x1, self.y1)
        
