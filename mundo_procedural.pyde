import Global as G
import GUI
import entities
import chunks

frame_counter = 0
drag_counter  = 0 
wheel_counter = 0

###############################################{ START }####################################################

def setup():
    fullScreen(P3D)
    frameRate(G.FRAMERATE)
    
    noSmooth()
    
    chunks.loadTextures()
    entities.loadTextures()
    G.updateDisplay()
    chunks.updateChunks()

    camera(-G.TRANSLATE_X, -G.TRANSLATE_Y, (height/2.0) / tan(PI*30.0 / 180.0), -G.TRANSLATE_X, -G.TRANSLATE_Y, 0, 0, 1, 0)
    
    background(0)
    G.updateMouse()

#################################################{ LOOP }####################################################

def draw():
    global frame_counter,nube
    scale(G.SCALE,G.SCALE)
    frame_counter += 1
    
    if frame_counter >= 10:  
        chunks.processChunkQueue()  
        frame_counter = 0 
    
    background(0)

    for chunk in chunks.chunkVisibles:
        chunk.drawChunk()
   
    for Entitie in entities.entitiesVisibles:
        alpha(1)
        Entitie.drawMe()
        alpha(1)
    
    entities.genCloud()
    for cloud in entities.ArrayClouds:
        cloud.drawMe()
        

    if G.DEBUG_MODE:    
        GUI.info()
    G.updateMouse()


########################################{ EVENTOS DE ENTRADA }##############################################

def mouseWheel(event): 
    global wheel_counter
    if event.count == -1:
        if G.SCALE < 1.25:
            G.SCALE +=0.01*G.SCALE
    if event.count ==  1:
        if G.SCALE > 0.8:
            G.SCALE -= 0.01*G.SCALE
    wheel_counter += 1
  
    if wheel_counter >= 5:
        
        G.updateDisplay()
        chunks.updateChunks()
        wheel_counter = 0  
   
def keyReleased():
    print("KeyCode: ", keyCode)
    if keyCode == 99: G.DEBUG_MODE = not(G.DEBUG_MODE)
    if keyCode == 97: G.SCALE = 1

def mouseDragged():
    global drag_counter
    G.updateCamera()
    
    drag_counter += 1
    if drag_counter >= 5:
        G.updateDisplay()
        chunks.updateChunks()
        entities.updateVisibleEntities()
        drag_counter = 0

#####
