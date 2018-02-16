import argparse
from naoqi import ALProxy
import time

name = 'Adrian'
spd = '80'		#Velocidad de habla 20% menor a lo estandar (100), puede ser hasta 400
tiempoDecision = 4.0  	#Tiempo para decidir si ya se puede pasar al siguiente modulo 
tiempoInterno= 2.0 	#Tiempo para pasar a la siguiente accion dentro de cada modulo
repetitions = 1		#Numero de repeticiones


#Codigo para ser utilizado con pMain que lleva a cabo los 8 modulos de autismo.

def Introduccion(entry):
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd] = getRobotInfo(entry)
    motionProxy.wakeUp() 	# Despertar al robot despues de remover el stiffness
    time.sleep(1.0)
    postureProxy.goToPosture("Sit", 0.6) # Poner al robot en su posicion inicial sentado
            
    #1 Mueve la cabeza de un lado a otro - 2 veces
    for x in range(0,2):
	moveHeadRight(motionProxy) 	#Derecha
        moveHeadLeft(motionProxy) 	#Izquierda
        moveHeadCenter(motionProxy) 	#Centro
        time.sleep(3.0)

    postureProxy.goToPosture("Sit", 0.6)
    moveHeadDown(motionProxy)		#Mira en direccion al nino
    time.sleep(1.0)
	
    #2 LEDs de ojos parpadean
    colors = ["white","red","green","blue", "yellow","magenta","cyan"] #Colores de ojos del robot
    for y in range(0,3): 	#Ilumina con todos los colores 3 veces
        for x in colors:
            blinkColors(x) 	#Utiliza "blinkColors" para el parpadeo de cada color
	
    #3 Nombre del nino
    for x in range(0,repetitions):
	talk(name,"") 		#Utiliza la funcion "talk" donde lo que dice el robot es el nombre
	time.sleep(tiempoDecision)


def Saludar(entry):
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd] = getRobotInfo(entry)
    #1 Saluda verbalmente //  #2 Saluda verbalmente + Mov. brazo derecho
 
    #1 Saludo verbal
    talk("Hola", "")
    time.sleep(1.0) 	#Tiempo para concatenar con la siguiente palabra
    talk(name, "")
    time.sleep(tiempoInterno)

    #2 Saludo Verbal + Mov. brazo derecho
    talk("Hola", "")
    time.sleep(1.0) 	#Tiempo para concatenar con la siguiente palabra
    talk(name, "")
    hiHand(motionProxy)
    postureProxy.goToPosture("Sit", 0.6)
    
    time.sleep(tiempoDecision)


def RespuestaAtencion(entry):
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd] = getRobotInfo(entry)
    #1 Mira a la derecha
    #2 Mira a la derecha + voz
    #3 Mira a la derecha + voz + Mov. Mano

    #1 Mira a la derecha 
    turnHead() 		#Funcion para que mire a la derecha y arriba
    time.sleep(tiempoInterno)	#Tiempo interno para la siguiente actividad dentro del modulo (#2)
    
    #2 Voz (Mira eso)   + Mira a la derecha 
    moveHeadDown(motionProxy)
    talk(name, "")		# Dice "nombre" + mira eso
    time.sleep(0.5)
    talk("Mira eso", "")
    time.sleep(0.5)
    turnHead()		#Mira a la derecha y arriba	
    time.sleep(4.0)
    time.sleep(tiempoInterno) 	#Tiempo interno para la siguiente actividad dentro del modulo (#3)
      
    #3 Voz (Mira eso)   + Mira a la derecha  + Mov. Mano: Robot  
    moveHeadDown(motionProxy)		#Regresa a mirar al nino
    justPoint()
    talk(name, "")
    time.sleep(0.5)
    talk("Mira eso", "")

    time.sleep(tiempoDecision)
    #####REVISAR
    names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "LShoulderPitch", "LShoulderRoll","LElbowYaw", "LElbowRoll", "LWristYaw", "HeadPitch","HeadYaw"]
    anglesd = [39.0, -17.3, 29.2, 71.2, -1.5, 39.0, 17.3, -29.2, -71.2, -1.5, 5.0, 0.0]
    fractionMaxSpeed  = 0.15
    move(names, anglesd, fractionMaxSpeed)
    time.sleep(2.5)
    ######
    postureProxy.goToPosture("Sit", 0.6)
		  





def Imitacion(entry):
    #Modulo de imitacion en el cual el robot pide que lo imiten y sube las manos, luego las pone enfrente y luego se toca la cabeza
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd] = getRobotInfo(entry)
    
    motionProxy.wakeUp()

    #Funciones de subir las manos, ponerlas enfrente y tocarse la cabeza con la orden verbal incluida
    armsUp(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd) 
    armsinFront(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd) # NO HAY FLUIDEZ
    touchHead(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd) #NO HAY FLUIDEZ PASA MUCHO TIEMPO 

    # Stiffness removed
    # motionProxy.setStiffnesses("Body", 0.0)

def AnticipacionSocial(entry):
    #Modulo en el que el robot se tapa los ojos y pregunta donde esta el nino, luego los destapa y dice: "aqui esta"
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd] = getRobotInfo(entry)
    
    motionProxy.wakeUp()
    postureProxy.goToPosture("Sit", 0.6)
    intermediate(motionProxy) #esta posicion asegura que el robot no choque sus brazos con las rodillas al realizar la accion
    
    coverEyes(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd)

    # Stiffness removed
    # motionProxy.setStiffnesses("Body", 0.0)


def EntregarRecibir(entry):
    #Modulo en el que el robot le pide al nino que le entregue un objeto, lo agarra y luego se lo entrega al nino
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd] = getRobotInfo(entry)

    motionProxy.wakeUp()
    postureProxy.goToPosture("Sit", 0.6)
    intermediate(motionProxy)

    #El robot pide el objeto utilizando la funcion "robotRecibe"
    robotRecibe(motionProxy, ttsProxy, ledsProxy, name, spd)  

    #El robot le entrega el objeto al nino utilizando la funcion "robotEntrega"
    intermediate(motionProxy)
    robotEntrega(motionProxy, ttsProxy, ledsProxy, name, spd)
    
    goBackInitial(motionProxy, postureProxy, 0) #Esta funcion incluye ir a la posicion intermedia y luego regresar a la inicial

    # Stiffness removed
    #motionProxy.setStiffnesses("Body", 0.0)
   

def getRobotInfo(entry):
    #Funcion que extrae toda la informacion necesaria del input para los modulos y funciones de movimiento, hablado, postura y LEDs
    robotIP = entry["ip"].get()
    PORT = eval(entry["port"].get())
    name = entry["name"].get()
    spd  = entry["vel"].get()
    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    ttsProxy     = ALProxy("ALTextToSpeech", robotIP, PORT)
    ledsProxy    = ALProxy("ALLeds", robotIP, PORT)
    return [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd]

def goBackInitial(motionProxy, postureProxy, sleepTime):
    #Funcion que regresa al robot a su posicion inicial tomando el tiempo entre posicion intermedia y inicial como un argumento
    intermediate(motionProxy)
    time.sleep(sleepTime)
    postureProxy.goToPosture("Sit", 0.6)

def move(motionProxy, names, anglesd, fractionMaxSpeed):
    #Funcion de movimiento general la cual usa los angulos y la velocidad de movimiento como un argumento
    angles = [val/180.*3.14159265 for val in anglesd] #Convierte los angulos en radianes
    motionProxy.setAngles(names, angles, fractionMaxSpeed)

def moveAll(motionProxy, anglesd, fractionMaxSpeed):
    #Funcion que mueve todas las articulaciones superiores al darle los angulos especificos y la velocidad como un argumento
    names = ["RElbowRoll","RShoulderRoll","RShoulderPitch","RElbowYaw","RWristYaw","RHand","HeadPitch", "HeadYaw","LElbowRoll","LShoulderRoll","LShoulderPitch","LElbowYaw","LWristYaw","LHand"]
    move(motionProxy, names, anglesd, fractionMaxSpeed)

def moveRightSide(motionProxy, anglesd, fractionMaxSpeed):
    #Funcion que mueve las articulaciones superiores del lado derecho
    names = ["RElbowRoll","RShoulderRoll","RShoulderPitch","RElbowYaw","RWristYaw","HeadPitch", "HeadYaw"]
    move(motionProxy, names, anglesd, fractionMaxSpeed)

def blinkColors(ledsProxy, color):
    #Funcion que prende los ojos del robot del color especificado en los argumentos
    rDuration = 0.05
    ledsProxy.fadeRGB( "FaceLeds", color, rDuration )
    time.sleep(0.1)
    ledsProxy.fadeRGB( "FaceLeds", 0xffffff, rDuration )

def moveHeadRight(motionProxy):
    #Funcion que mueve la cabeza hacia la derecha utilizando la funcion "move"
    names = ["HeadYaw"]
    anglesd = [-45.0]
    fractionMaxSpeed  = 0.20
    move(motionProxy, names, anglesd, fractionMaxSpeed)
    time.sleep(1.5)
  
def moveHeadLeft(motionProxy):
    # Funcion que mueve la cabeza hacia la izquierda utilizando la funcion "move"
    names = ["HeadYaw"]
    anglesd = [45.0]
    fractionMaxSpeed  = 0.20
    move(motionProxy, names, anglesd, fractionMaxSpeed)
    time.sleep(1.5)    

def moveHeadCenter(motionProxy):
    # Funcion que mueve la cabeza hacia al centro utilizando la funcion "move"
    names = ["HeadPitch","HeadYaw"]
    anglesd = [0.0, 0.0]
    fractionMaxSpeed  = 0.1
    move(names, anglesd, fractionMaxSpeed)
    #time.sleep(1.5)

def moveHeadDown(motionProxy):
    # Funcion que mueve la cabeza en direccion al nino 
    names = ["HeadPitch","HeadYaw"]
    anglesd = [15.0, 0.0]
    fractionMaxSpeed  = 0.05
    move(names, anglesd, fractionMaxSpeed)
    #time.sleep(1.5)



def talk(ttsProxy, ledsProxy, message1, spd, message2):
    #Funcion que recibe dos mensajes y la velocidad de hablado y hace que el robot lo articule como se le especifica
    str1 = "\\rspd=" + spd + "\\" + message1 + " " + message2
    ttsProxy.say(str1)

def intermediate(motionProxy):
    #Funcion en la cual el robot sube un poco sus brazos de la posicion de sentado para evitar choque con las rodillas
    names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "LShoulderPitch", "LShoulderRoll","LElbowYaw", "LElbowRoll", "LWristYaw","HeadPitch"]
    anglesd = [39.0, -17.3, 29.2, 71.2, -1.5, 39.0, 17.3, -29.2, -71.2, -1.5, 13.0]
    fractionMaxSpeed  = 0.15
    move(motionProxy, names, anglesd, fractionMaxSpeed)

def hiHand(motionProxy, postureProxy, ttsProxy, ledsProxy, spd, name):
    #Funcion en que el robot hace un saludo complejo, pitch y yaw son parametros para ajustar el angulo de la cabeza
    pitch = 15.0 #3
    yaw = 20.0 #18
    shortInterval = 0.08 #Ajustar el tiempo que pasa entre accion en el saludo para lograr mas fluidez
    longInterval = 0.25
    neutralInterval = 0.15
    talk(ttsProxy, ledsProxy, "Hola", spd, name)
    #1
    anglesd = [78.5, -14.6, 13.8, -17.7, 9.9, 0.43, -0.1 + pitch, 0.0, -78.9, 20.3, 63.6, -45.9, 0.7, 0.24]
    fractionMaxSpeed = 0.15
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(shortInterval)
    #2
    anglesd = [77.5, -15.2, 11.6, -16.8, 9.9, 0.43, -0.1 + pitch, 0.4, -78.9, 20.3, 63.6, -45.9, 0.1, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(shortInterval)
    #3
    anglesd = [72.4, -18.3, 4.9, -12.4, 9.9, 0.43, -0.1 + pitch, 0.4, -78.9, 20.3, 63.6, -45.9, 0.1, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(longInterval)
    #4
    anglesd = [14.3, -54.5, -67.0, 31.8, -17.8, 0.85, -7.1 + pitch, -16.2 + yaw, -75.0, 14.3, 53.8, -40.4, 7.6, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(shortInterval)
    #5
    anglesd = [14.3, -21.5, -67.1, 31.9, -17.7, 0.85, -8.6 + pitch, -18.5 + yaw, -73.9, 13.6, 52.9, -40.1, 8.3, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(shortInterval)
    #6
    anglesd = [14.9, -1.4, -66.2, 31.5, -17.8, 0.85, -9.6 + pitch, -20.1 + yaw, -73.2, 12.8, 53.4, -39.9, 8.3, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(neutralInterval)
    #7
    anglesd = [19.7, -3.2, -65.5, 29.4, -17.8, 0.85, -11.2 + pitch, -21.3 + yaw, -72.2, 12.8, 53.4, -39.9, 8.3, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(longInterval)
    #8
    anglesd = [53.4, -25.9, -62.5, 22.6, -17.8, 0.85, -18.5 + pitch, -23.4 + yaw, -68.1, 12.2, 53.4, -39.4, 8.3, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(shortInterval)
    #9
    anglesd = [52.8, -30.8, -62.5, 21.9, -17.8, 0.85, -19.3 + pitch, -23.4 + yaw, -68.1, 12.2, 53.4, -39.4, 8.3, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(shortInterval)
    #10
    anglesd = [49.4, -35.7, -64.0, 21.3, -17.8, 0.85, -19.3 + pitch, -23.4 + yaw, -68.1, 12.2, 53.4, -39.4, 8.3, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(neutralInterval)
    #11
    anglesd = [39.1, -46.7, -68.4, 20.7, -17.8, 0.85, -16.3 + pitch, -23.4 + yaw, -68.7, 12.2, 52.3, -37.2, 8.3, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(longInterval)
    #12
    anglesd = [11.0, -54.8, -72.1, 20.7, -17.8, 0.85, -6.6 + pitch, -23.4 + yaw, -70.4, 12.2, 49.9, -35.7, 8.3, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(shortInterval)
    #13
    anglesd = [11.0, -53.7, -72.1, 20.0, -17.8, 0.85, -4.3 + pitch, -23.4 + yaw, -70.4, 12.2, 49.9, -35.7, 8.3, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(shortInterval)
    #14
    anglesd = [11.0, -50.4, -72.1, 20.0, -17.8, 0.85, -3.7 + pitch, -24.0 + yaw, -70.4, 12.2, 49.9, -35.7, 8.3, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(neutralInterval)
    #15
    anglesd = [14.5, -33.5, -71.3, 20.0, -17.8, 0.85, -5.0 + pitch, -25.3 + yaw, -73.3, 13.4, 49.9, -38.6, 7.7, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(longInterval)
    #16
    anglesd = [40.4, -19.0, -66.0, 21.4, -17.8, 0.85, -9.5 + pitch, -28.6 + yaw, -75.2, 14.1, 51.2, -42.8, 7.7, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(shortInterval)
    #18
    anglesd = [48.8, -17.7, -55.7, 34.2, -16.3, 0.84, -10.7 + pitch, -29.5 + yaw, -75.2, 14.1, 51.2, -42.8, 7.7, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(neutralInterval)
    #19
    anglesd = [57.9, -15.6, -25.1, 55.5, -9.3, 0.74, -10.7 + pitch, -29.5 + yaw, -74.4, 14.1, 51.2, -42.3, 7.1, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(longInterval)
    #20
    anglesd = [72.2, -14.4, 58.2, 47.5, 10.3, 0.43, -1.3 + pitch, -22.2 + yaw, -68.1, 13.4, 48.5, -38.8, 7.1, 0.24]
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(1.5)

def justPoint(motionProxy, postureProxy):
    #Funcion en la que el robot senala hacia el lado derecho derecho mientras voltea

    #motionProxy.wakeUp()
    #postureProxy.goToPosture("Sit", 0.6)
    intermediate(motionProxy)

    #El robot senala
    anglesd = [4.0,-50.0,-85.0,-40.0,60.0,-25.2,-60.2]
    fractionMaxSpeed  = 0.15
    #El robot abre la mano derecha para senalar
    motionProxy.post.openHand('RHand')
    time.sleep(0.5)
    moveRightSide(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(0.5)

def turnHead(motionProxy, postureProxy, ttsProxy, ledsProxy):
    #Funcion en la que el robot solo mira hacia el lado derecho y arriba
    names = ["HeadPitch", "HeadYaw"]
    anglesd = [-25.2, -60.2]
    fractionMaxSpeed  = 0.25
    move(motionProxy, names, anglesd, fractionMaxSpeed)


def touchHead(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd):
    #Funcion en la que el robot toca su cabeza y le pide al nino que lo imite
    
    postureProxy.goToPosture("Sit", 0.6)
    intermediate(motionProxy)
    time.sleep(1.5)
    
    #El robot toca su cabeza y dice "has esto"
    talk(ttsProxy, ledsProxy, name, spd, "")
    anglesd = [86.3, -32.7, -75.0, -4.6, 92.1, 0.59, 11.0, 0.0, -86.3, 32.7, -75.0, -4.6, -92.1, 0.59]
    fractionMaxSpeed  = 0.15
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    talk(ttsProxy, ledsProxy, "has", spd, "")
    time.sleep(0.2)
    talk(ttsProxy, ledsProxy, "esto", spd, "")
    time.sleep(6.0)
    
    goBackInitial(motionProxy, postureProxy, 3.0)

def armsUp(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd):
    #Funcion en la que el robot sube sus brazos y le pide al nino que lo imite
    
    postureProxy.goToPosture("Sit", 0.6)
    intermediate(motionProxy)
    time.sleep(1.5)

    #El robot sube sus brazos y dice: "has esto"
    talk(ttsProxy, ledsProxy, name, spd, "")
    anglesd = [40.9, -32.7, -75.0, -4.6, 92.1, 0.59, 11.0, 0.0, -40.9, 32.7, -75.0, -4.6, -92.1, 0.59]
    fractionMaxSpeed  = 0.15
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    talk(ttsProxy, ledsProxy, "has", spd, "")
    time.sleep(0.2)
    talk(ttsProxy, ledsProxy, "esto", spd, "")
    time.sleep(6.0)

    goBackInitial(motionProxy, postureProxy, 3.0)
 
def armsinFront(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd):
    #Funcion en la que el robot pone sus brazos hacia el frente y le pide al nino que lo imite

    postureProxy.goToPosture("Sit", 0.6)

    motionProxy.closeHand('RHand')
    motionProxy.closeHand('LHand')

    #El robot pone sus brazos hacia el frente y dice: "has esto"
    names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "LShoulderPitch", "LShoulderRoll","LElbowYaw", "LElbowRoll", "LWristYaw"] #Angulos de posicion intermedia
    anglesd = [39.0, -25.3, 29.2, 71.2, -1.5, 39.0, 25.3, -29.2, -71.2, -1.5]
    fractionMaxSpeed  = 0.15
    move(motionProxy, names, anglesd, fractionMaxSpeed)
    talk(ttsProxy, ledsProxy, name, spd, "")

    #Brazos mas separados
    anglesd = [39.0, -25.3, 29.2, 66.2, -1.5, 39.0, 25.3, -29.2, -66.2, -1.5]
    fractionMaxSpeed  = 0.15
    move(motionProxy, names, anglesd, fractionMaxSpeed)
    time.sleep(0.5)

    #Brazos casi enfrente pero con los codos flexionados
    anglesd = [15.2, 2.1, 15.1, -32.9, 41.4, 0.57, 11.0, -0.8, -15.2, -2.1, 15.1, 32.1, -41.4, 0.57]
    fractionMaxSpeed = 0.15
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    talk(ttsProxy, ledsProxy, "has", spd, "")
    time.sleep(0.2)
    talk(ttsProxy, ledsProxy, "esto", spd, "")
    time.sleep(0.6)

    #Brazos enfrente
    anglesd = [3.2, 2.1, 15.1, -32.9, 41.4, 0.57, 11.0, -0.8, -3.2, -2.1, 15.1, 32.1, -41.4, 0.57]
    fractionMaxSpeed = 0.15
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(6.0)

    #Brazos girados hacia adentro para empezar el regreso a la posicion inicial
    anglesd = [3.2, 2.1, 15.1, -32.9, 85.4, 0.57, 11.0, -0.8, -3.2, -2.1, 15.1, 32.1, -85.4, 0.57]
    fractionMaxSpeed = 0.15
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(0.4)

    #Brazos flexionados antes de ir hacia la posicion inicial
    anglesd = [25.2, 2.1, 15.1, -10.9, 85.4, 0.57, 11.0, -0.8, -25.2, -2.1, 15.1, 10.9, -85.4, 0.57]
    fractionMaxSpeed = 0.15
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(0.2)

    postureProxy.goToPosture("Sit", 0.6)


def coverEyes(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd):
    #Funcion en la que el robot se cubre los ojos y pregunta donde esta el nino
    
    #El robot cubre sus ojos
    anglesd = [87.6, 15.0, 10.0, 64.7, 82.1, 0.0, -7.0, 0.0, -87.6, -15.0, 10.0, -64.7, -82.1, 0.0,]
    fractionMaxSpeed  = 0.15
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(0.5)
    talk(ttsProxy, ledsProxy, "Donde esta", spd, name)
    time.sleep(5.0)

    #El robot se destapa los ojos y dice: "aqui esta"
    intermediate(motionProxy)
    talk(ttsProxy, ledsProxy, "Aaki", spd, "esta")
    time.sleep(1.5)
    postureProxy.goToPosture("Sit", 0.6)

def robotRecibe(motionProxy, ttsProxy, ledsProxy, name, spd):
    #Funcion en la que el robot le pide al nino un objeto y lo recibe 
    
    #El robot extiende el brazo, abre la mano y dice: "Dame"
    anglesd = [3.0, 4.0, 28.0, 119.0, 60.0, 10.0, 0.0]
    fractionMaxSpeed  = 0.08
    moveRightSide(motionProxy, anglesd, fractionMaxSpeed)

    #Open Hand
    #names = ["RHand"];
    #anglesd = [1.0]
    #move(motionProxy, names, anglesd, fractionMaxSpeed)
    motionProxy.openHand('RHand')
    talk(ttsProxy, ledsProxy, name, spd, "")
    time.sleep(1.0)
    talk(ttsProxy, ledsProxy, "Dame", spd, "")
    time.sleep(5.0)

    #El robot agarra el objeto
    motionProxy.closeHand('RHand')
    time.sleep(1.0)
    intermediate(motionProxy)
    time.sleep(15.0)

# SE DEBE HACER UN BLOQUE SEPARADO PARA ENTREGAR Y RECIBIR 


def robotEntrega(motionProxy, ttsProxy, ledsProxy, name, spd):
    #Funcion en la que el robot le entrega el objeto al nino

    #El robot extiendo su brazo y abre la mano para entregar el objeto
    anglesd = [3.0, 4.0, 28.0, 119.0, 60.0, 10.0, 0.0]
    fractionMaxSpeed  = 0.08
    moveRightSide(motionProxy, anglesd, fractionMaxSpeed)
    talk(ttsProxy, ledsProxy, name, spd, "")
    time.sleep(1.0)
    talk(ttsProxy, ledsProxy, "Toma", spd, "")
    time.sleep(2.0)
    motionProxy.openHand('RHand')
    time.sleep(5.0)

  
