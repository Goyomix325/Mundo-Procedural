import Global as G
import entities
import chunks

def gen():
    n = 1
    while True:
        yield n * 15
        n += 1


def info():
    global visibles
    margin = gen()
    pushMatrix()
    scale(1/G.SCALE,1/G.SCALE)
    
    stroke(255)
    strokeWeight(10)
    point(0,0)
    stroke("#FFFF00")
    rectMode(CORNERS)
    #noFill()
    strokeWeight(2)
    
    point(G.STW_X(0)*G.SCALE, G.STW_Y(0)*G.SCALE)
    point(G.STW_X(width)*G.SCALE,G.STW_Y(height)*G.SCALE)
    
    #crear un codigo que detecte el chunk en la pocicion central de la pantalla
    #crear un codigo que detecte los chunks que estan a la redonda del chunk central(default= 22)
    #en base a estos chunks centrales que solo mantenga cargados los que estan a la redonda
    #al macenar los que ya no esten
    #mantener cargados los que esten en ese perimetro
    
                
    fill(255)
    textSize(10)
    text("(X: "+str(screenX(0,0))+", Y:"+str(screenY(0,0))+")", 0, 0)
    
    
    
    pushMatrix()
    translate((-G.TRANSLATE_X-width/2), (-G.TRANSLATE_Y-height/2))
    textSize(10)
    noStroke()
    fill(0,0,0,100)
    rect(3,3,160,200)
    fill(255)
    
    text("TRANSLATE: X: "+str(round(-G.TRANSLATE_X))+",Y: "+str(round(-G.TRANSLATE_Y)),5,next(margin))
    
    if frameRate >= 144:
        fill("#00FF00")
    elif frameRate< 144:
        fill("#FFFF00")
    elif frameRate< 100: 
        fill("#FF0000")
    textSize(10)

    text("FrameRate: "+str(round(frameRate)),5,next(margin))
    text("Estres: "+str(100-round(((round(frameRate)/255)*100)))+"%",5,next(margin))
    fill("#FFFFFF")
    
    text("SCALE: "+str(G.SCALE),5,next(margin))
    text("SEED: "+str(chunks.SEED),5,next(margin))
    
    text("=================",5,next(margin))
    
    text("Chunks Queue: "+str(len(chunks.chunkQueue)),5,next(margin))
    text("Chunks: "+str(len(chunks.chunkList)),5,next(margin))
    text("Chunks Visibles: "+str(len(chunks.chunkVisibles)),5,next(margin))
    
    text("=================",5,next(margin))
    
    text("Entities: "+str(len(entities.ArrayEntities)),5,next(margin))
    text("Entities Visibles: "+str(len(entities.entitiesVisibles)),5,next(margin))

    
    
    text("By: Jair Abraham Aguilar Martinez ",5,height-10)
    popMatrix()
    
    
    pushMatrix()
    textSize(11)
    text("(X: "+str(G.MOUSE_X)+", Y:"+str(G.MOUSE_Y)+")", G.MOUSE_X, G.MOUSE_Y)
    ID = chunks.IDcasilla(G.MOUSE_X, G.MOUSE_Y)
    text("(casilla: (X: "+str(G.STW_X(ID[0]))+", Y:"+str(G.STW_Y(ID[1]))+")", (G.MOUSE_X), (G.MOUSE_Y)-12)
    text("Ruido: "+str(chunks.ruidoInCasilla(ID)), (G.MOUSE_X), (G.MOUSE_Y)-24)
    popMatrix()
    
    
    
    popMatrix()
