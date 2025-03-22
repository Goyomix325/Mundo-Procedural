#------ {Variables Globales} --------------------------

DEBUG_MODE = False                                                          #- Variable para opciones de depuracion.
FRAMERATE  = 244                                                             #x Framerate.
SCALE = 1                                                                   #- zoom.

#--- {Variables de la Pantalla} -----------------------

TRANSLATE_X = 0                                                             #- Desplazamiento de la pantalla en X.
TRANSLATE_Y = 0                                                             #- Desplazamiento de la pantalla en Y.
OFFSET      = 0                                                             #- Incremento/Decremento de la pantalla.
DISPLAY     = (0, 0, 0, 0)                                              

#--- {Funciones de la Pantalla} -----------------------

def updateDisplay():                                                        #- Actualiza la posicion de la pantalla en el mundo.
    global DISPLAY  
    x1 = STW_X(0)-OFFSET
    y1 = STW_Y(0)-OFFSET
    x2 = STW_X(width) +OFFSET
    y2 = STW_Y(height)+OFFSET
    DISPLAY = (x1, y1, x2, y2)
    
def STW_X(x): return int((x - (TRANSLATE_X) - width/2)/SCALE)               #- dada una posicion en X en la pantalla, devuelve su valor entero en el mundo.
def STW_Y(y): return int((y - (TRANSLATE_Y) - height/2)/SCALE)              #- dada una posicion en Y en la pantalla, devuelve su valor entero en el mundo.

def updateCamera():                                                         #- Actualiza la camara siguiendo el movimiento del Mouse.
    global TRANSLATE_X, TRANSLATE_Y
    TRANSLATE_X = TRANSLATE_X + (mouseX-pmouseX)
    TRANSLATE_Y = TRANSLATE_Y + (mouseY-pmouseY)
    
    camera(-TRANSLATE_X, -TRANSLATE_Y, (height/2.0) / tan(PI*30.0 / 180.0), 
           -TRANSLATE_X, -TRANSLATE_Y, 0, 
           0, 1, 0)
    
#--- {Variables del Mouse} ----------------------------

MOUSE_X = 0                                                                 #- Posicion X del Mouse en el Mundo.
MOUSE_Y = 0                                                                 #- Posicion Y del Mouse en el Mundo.

#--- {Funciones del Mouse} ----------------------------

def updateMouse():                                                          #- Actualiza la posicion del Mouse en el mundo.
    global MOUSE_X, MOUSE_Y
    MOUSE_X = (mouseX - TRANSLATE_X - width/2) 
    MOUSE_Y = (mouseY - TRANSLATE_Y - height/2)

#------------------------------------------------------

def pointInBox(point_x, point_y, entitie):                                  #- enviar valores X y Y para comparar si esta dentro de una entidad
    """Verifica si un punto esta dentro dela HB de una entidad"""
    return (entitie.hb_minX <= point_x <= entitie.hb_maxX and
            entitie.hb_minY <= point_y <= entitie.hb_maxY)
    
#------------------------------------------------------

def boxInBox(A, B):
    """Verifica si una entidad tiene contacto con otra"""
    return (A.hb_minX <= B.hb_maxY and
            A.hb_maxX >= B.hb_minX and
            A.hb_minY <= B.hb_maxY and
            A.hb_maxY >= B.hb_minY)
