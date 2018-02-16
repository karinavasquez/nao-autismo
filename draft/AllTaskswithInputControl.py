import sys
import time

from naoqi import ALModule
from naoqi import ALBroker
from naoqi import ALProxy
import argparse

#FALTA PROBAR LA FUNCIONALIDAD DE ESTE PROGRAMA, PERFECCIONAR LOS DETALLES DE HABLADO Y ANGULOS DE LA MANO E INCLUIR EL VIDEO
#PUEDE SER NECESARIO INCLUIR UN TIME.SLEEP ENTRE REPETICIONES PARA QUE EL PSICOLOGO TENGA MAS TIEMPO DE PENSAR SI QUIERE REPETIR LA ACCION O NO

# Global variable to store the ReactToTouch module instance
ReactToTouch = None
memory = None
counter = 0

name = 'Adrian'
spd = '80'
tiempoDecision = 5.0
 #Cambiar este numero si se necesita menos o mas tiempo para decidir si ya se puede pasar al siguiente modulo

repetitions = 3
checkIntro = False
checkSayName = False

checkSaludar = False

checkRespuesta = False
	
checkarmsUp = False
checkarmsinFront = False
checktouchHead = False

checkAnticipacion = False

checkrobotPide = False
checkrobotRecibe = False

checkrobotEntrega = False
checkninoRecibio = False


class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create proxy for later use
        self.motionProxy = ALProxy("ALMotion")
        self.postureProxy = ALProxy("ALRobotPosture")
        self.ttsProxy = ALProxy("ALTextToSpeech")
        self.ledsProxy = ALProxy("ALLeds")

        # Subscribe to LeftBumperPressed event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("LeftBumperPressed",
            "ReactToTouch",
            "onTouched")

    def onTouched(self, subscriber, value):
        """ This will be called each time a touch
        is detected.

        """

        global counter
        global checkIntro
        global checkSayName
        global checkSaludar
        global checkRespuesta
        global checkarmsUp
        global checkarmsinFront
        global checktouchHead
        global checkAnticipacion
        global checkrobotPide
        global checkrobotRecibe
        global checkrobotEntrega
        global checkninoRecibio

        if value == 1.0:
            counter = counter + 1
            if counter == 1:
                checkIntro = True
                self.Intro()
            elif counter == 2:
                checkIntro = False
                checkSayName = True
                self.SayName()
            elif counter == 3:
                checkSayName = False
                checkSaludar = True
                self.Saludar()
            elif counter == 4:
                checkSaludar = False
                checkRespuesta = True
                self.RespuestaAtencion()
            elif counter == 5:
                checkRespuesta = False
                checkarmsUp = True
                self.armsUp()
            elif counter == 6:
                checkarmsUp = False
                checkarmsinFront = True
                self.armsinFront()
            elif counter == 7:
                checkarmsinFront = False
                checktouchHead = True
                self.touchHead()
            elif counter == 8:
                checktouchHead = False                
                checkAnticipacion = True
                self.AnticipacionSocial()
            elif counter == 9:
                checkAnticipacion = False
                checkrobotPide = True
                self.robotPide()
            elif counter == 10:
                checkrobotPide = False
                checkrobotRecibe = True
                self.robotRecibe()
            elif counter == 11:
                checkrobotRecibe = False
                checkrobotEntrega = True
                self.robotEntrega()
            else:
                checkrobotEntrega = False
                checkninoRecibio = True
                self.ninoRecibio()

     
    def Intro(self):
        if checkIntro == True:
            self.motionProxy.wakeUp() # Despertar al robot despues de remover el stiffness
            time.sleep(1.0)
            self.postureProxy.goToPosture("Sit", 0.6) # Poner al robot en su posicion inicial sentado
            
        # Move head
        names = ["HeadPitch","HeadYaw"]
        anglesd = [0.0, 0.0]
        fractionMaxSpeed  = 0.05 #Esta variable varia de 0 a 1 donde 1 es mas rapido y 0 mas lento
        #Mover la cabeza 2 veces
        for x in range(0,2):
            if checkIntro == True:
                self.moveHeadRight() #Derecha
                self.moveHeadLeft() #Izquierda
                self.move(names, anglesd, fractionMaxSpeed) #Centro: llama a funcion "move"
                time.sleep(4.0)

        if checkIntro == True:
            self.postureProxy.goToPosture("Sit", 0.6)
            names = ["HeadPitch","HeadYaw"]
            anglesd = [15.0, 0.0] #Angulos para que el robot mire hacia el nino
            fractionMaxSpeed  = 0.05
            self.move(names, anglesd, fractionMaxSpeed)
            time.sleep(1.0)

            colors = ["white","red","green","blue", "yellow","magenta","cyan"] #Colores con los cuales se iluminaran los ojos del robot
            for y in range(0,3): #Ilumina con todos los colores 3 veces
                if checkIntro == True:
                    for x in colors:
                        self.blinkColors(x) #Utiliza la funcion "blinkColors" para el parpadeo de cada color


    def SayName(self):
        #Modulo en el que el robot dice el nombre del nino
        for x in range(0,repetitions):
            if checkSayName == True:
                self.talk(name,"") #Utiliza la funcion "talk" donde lo que dice el robot es el nombre
                time.sleep(tiempoDecision) #Cambiar este numero si se necesita mas o menos tiempo de decision


    def Saludar(self):
        #Modulo en el que el robot saluda verbalmente, luego saluda con su mano derecha y verbalmente
        if checkSaludar == True:
            self.postureProxy.goToPosture("Sit", 0.6)
            #Saludo verbal
            self.talk("Hola", "")
            time.sleep(1.0) #Cambiar este tiempo si dice Hola Adrian muy seguido o muy separado
            self.talk(name, "")
            time.sleep(tiempoDecision) #Cambiar este numero si se necesita mas o menos tiempo de decision

        if checkSaludar == True:
            #Saludo con el gesto
            self.hiHand()
            self.postureProxy.goToPosture("Sit", 0.6)


    def RespuestaAtencion(self):
        #Modulo en el que el robot mira hacia un lado, luego mira y dice "mira eso" y luego mira senala y dice "mira eso"

        if checkRespuesta == True:
            #Posicion inicial
            self.postureProxy.goToPosture("Sit", 0.6)
            #El robot solo voltea utilizando la funcion "turnHead"
            self.turnHead()
            time.sleep(4.0)
            self.postureProxy.goToPosture("Sit", 0.6)
            time.sleep(tiempoDecision) #Cambiar este numero si se necesita menos o mas tiempo de decision
        
        if checkRespuesta == True:
            #El robot mira y le dice al nino que mire verbalmente   
            self.turnHead()
            time.sleep(0.5)
            self.talk(name, "")
            time.sleep(0.5)
            self.talk("Mira eso", "")
            time.sleep(4.0)
            self.postureProxy.goToPosture("Sit", 0.6)
            time.sleep(tiempoDecision) #Cambiar este numero si se necesita menos o mas tiempo de decision
      
        if checkRespuesta == True:
            # El robot senala utilizando la funcion "justPoint" y le dice al nino que mire verbalmente  
            self.justPoint()
            self.talk(name, "")
            time.sleep(0.5)
            self.talk("Mira eso", "")
            time.sleep(5.0)
            names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "LShoulderPitch", "LShoulderRoll","LElbowYaw", "LElbowRoll", "LWristYaw", "HeadPitch","HeadYaw"]
            anglesd = [39.0, -17.3, 29.2, 71.2, -1.5, 39.0, 17.3, -29.2, -71.2, -1.5, 5.0, 0.0]
            fractionMaxSpeed  = 0.15
            self.move(names, anglesd, fractionMaxSpeed)
            time.sleep(2.5)
            self.postureProxy.goToPosture("Sit", 0.6)


    def armsUp(self):
        #Funcion en la que el robot sube sus brazos y le pide al nino que lo imite

        for x in range(0,repetitions):
            if checkarmsUp == True:
                self.postureProxy.goToPosture("Sit", 0.6)
                self.intermediate()
                time.sleep(1.5)

                #El robot sube sus brazos y dice: "has esto"
                self.talk(name, "")
                time.sleep(0.1)
                self.talk("has", "")
                time.sleep(0.1)
                self.talk("esto", "")
                anglesd = [40.9, -32.7, -75.0, -4.6, 92.1, 0.59, 11.0, 0.0, -40.9, 32.7, -75.0, -4.6, -92.1, 0.59]
                fractionMaxSpeed  = 0.15
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(6.0)

                self.goBackInitial(3.0) #Funcion para ir a la posicion intermedia y luego regresar a la inicial
                time.sleep(tiempoDecision) #Cambiar este numero si se necesita menos o mas tiempo de decision

     
    def armsinFront(self):
        #Funcion en la que el robot pone sus brazos hacia el frente y le pide al nino que lo imite

        for x in range(0,repetitions):
            if checkarmsinFront == True:
                self.postureProxy.goToPosture("Sit", 0.6)

                self.motionProxy.closeHand('RHand')
                self.motionProxy.closeHand('LHand')

                #El robot pone sus brazos hacia el frente y dice: "has esto"
                names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "LShoulderPitch", "LShoulderRoll","LElbowYaw", "LElbowRoll", "LWristYaw"] #Angulos de posicion intermedia
                anglesd = [39.0, -25.3, 29.2, 71.2, -1.5, 39.0, 25.3, -29.2, -71.2, -1.5]
                fractionMaxSpeed  = 0.15
                self.move(names, anglesd, fractionMaxSpeed)
                self.talk(name, "")
                time.sleep(0.1)
                self.talk("has", "")
                time.sleep(0.1)
                self.talk("esto", "")

                #Brazos mas separados
                anglesd = [39.0, -25.3, 29.2, 66.2, -1.5, 39.0, 25.3, -29.2, -66.2, -1.5]
                fractionMaxSpeed  = 0.15
                self.move(names, anglesd, fractionMaxSpeed)
                time.sleep(0.5)

                #Brazos casi enfrente pero con los codos flexionados
                anglesd = [15.2, 2.1, 15.1, -32.9, 41.4, 0.57, 11.0, -0.8, -15.2, -2.1, 15.1, 32.1, -41.4, 0.57]
                fractionMaxSpeed = 0.15
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(0.8)

                #Brazos enfrente
                anglesd = [3.2, 2.1, 15.1, -32.9, 41.4, 0.57, 11.0, -0.8, -3.2, -2.1, 15.1, 32.1, -41.4, 0.57]
                fractionMaxSpeed = 0.15
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(6.0)

                #Brazos girados hacia adentro para empezar el regreso a la posicion inicial
                anglesd = [3.2, 2.1, 15.1, -32.9, 85.4, 0.57, 11.0, -0.8, -3.2, -2.1, 15.1, 32.1, -85.4, 0.57]
                fractionMaxSpeed = 0.15
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(0.4)

                #Brazos flexionados antes de ir hacia la posicion inicial
                anglesd = [25.2, 2.1, 15.1, -10.9, 85.4, 0.57, 11.0, -0.8, -25.2, -2.1, 15.1, 10.9, -85.4, 0.57]
                fractionMaxSpeed = 0.15
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(0.2)

                self.postureProxy.goToPosture("Sit", 0.6)
                time.sleep(tiempoDecision) #Cambiar este numero si se necesita menos o mas tiempo de decision


    def touchHead(self):
        #Funcion en la que el robot toca su cabeza y le pide al nino que lo imite
        
        for x in range(0,repetitions):
            if checktouchHead == True:
                self.postureProxy.goToPosture("Sit", 0.6)
                self.intermediate()
                time.sleep(1.5)
                
                #El robot toca su cabeza y dice "has esto"
                self.talk(name, "")
                time.sleep(0.1)
                self.talk("has", "")
                time.sleep(0.1)
                self.talk("esto", "")
                anglesd = [86.3, -32.7, -75.0, -4.6, 92.1, 0.59, 5.0, 0.0, -86.3, 32.7, -75.0, -4.6, -92.1, 0.59]
                fractionMaxSpeed  = 0.15
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(6.0)
                
                self.goBackInitial(3.0)
                time.sleep(tiempoDecision) #Cambiar este numero si se necesita menos o mas tiempo de decision


    def AnticipacionSocial(self):
        #Modulo en el que el robot se tapa los ojos y pregunta donde esta el nino, luego los destapa y dice: "aqui esta"
        
        for x in range(0,repetitions):
            if checkAnticipacion == True:
                self.postureProxy.goToPosture("Sit", 0.6)
                self.intermediate() #esta posicion asegura que el robot no choque sus brazos con las rodillas al moverse
                self.coverEyes()
                time.sleep(tiempoDecision) #Cambiar este numero si se necesita menos o mas tiempo de decision

    def robotPide(self):
        #Funcion en la que el robot le pide al nino un objeto y lo recibe

        if checkrobotPide == True:
            self.postureProxy.goToPosture("Sit", 0.6)
            self.intermediate()
            
            #El robot extiende el brazo, abre la mano y dice: "Dame"
            anglesd = [3.0, 4.0, 28.0, 119.0, 60.0, 10.0, 0.0]
            fractionMaxSpeed  = 0.08
            self.moveRightSide(anglesd, fractionMaxSpeed)
            self.motionProxy.openHand('RHand')
            self.talk(name, "")
            time.sleep(1.0)
            self.talk("Dame", "")


    def robotRecibe(self):
        #El robot agarra el objeto
        if checkrobotRecibe == True:        
            self.motionProxy.closeHand('RHand') #Debe ser cambiado a un angulo especifico depende del objeto que sera utilizado
            time.sleep(1.0)
            names = ["RElbowRoll", "RShoulderRoll", "RShoulderPitch", "RElbowYaw", "RWristYaw"]
            anglesd = [71.8, -16.6, 53.7, 29.3, -1.7]
            fractionMaxSpeed  = 0.08
            move(names, anglesd, fractionMaxSpeed)


    def robotEntrega(self):
        #Funcion en la que el robot le entrega el objeto al nino
        
        if checkrobotEntrega == True:
            #El robot extiendo su brazo y abre la mano para entregar el objeto
            anglesd = [3.0, 4.0, 28.0, 119.0, 60.0, 10.0, 0.0]
            fractionMaxSpeed  = 0.08
            self.moveRightSide(anglesd, fractionMaxSpeed)
            self.talk(name, "")
            time.sleep(1.0)
            self.talk("Toma", "")
            time.sleep(2.0)
            self.motionProxy.openHand('RHand')

    
    def ninoRecibio(self):
        if ninoRecibio == True:
            self.goBackInitial(3.0)
            self.motionProxy.setStiffnesses("Body", 0.0)

    
    def goBackInitial(self, sleepTime):
        #Funcion que regresa al robot a su posicion inicial tomando el tiempo entre posicion intermedia y inicial como un argumento
        self.intermediate()
        time.sleep(sleepTime)
        self.postureProxy.goToPosture("Sit", 0.6)

    def move(self, names, anglesd, fractionMaxSpeed):
        #Funcion de movimiento general la cual usa los angulos y la velocidad de movimiento como un argumento
        angles = [val/180.*3.14159265 for val in anglesd] #Convierte los angulos en radianes
        self.motionProxy.setAngles(names, angles, fractionMaxSpeed)

    def moveAll(self, anglesd, fractionMaxSpeed):
        #Funcion que mueve todas las articulaciones superiores al darle los angulos especificos y la velocidad como un argumento
        names = ["RElbowRoll","RShoulderRoll","RShoulderPitch","RElbowYaw","RWristYaw","RHand","HeadPitch", "HeadYaw","LElbowRoll","LShoulderRoll","LShoulderPitch","LElbowYaw","LWristYaw","LHand"]
        self.move(names, anglesd, fractionMaxSpeed)




    def moveRightSide(self, anglesd, fractionMaxSpeed):
        #Funcion que mueve las articulaciones superiores del lado derecho
        names = ["RElbowRoll","RShoulderRoll","RShoulderPitch","RElbowYaw","RWristYaw","HeadPitch", "HeadYaw"]
        self.move(names, anglesd, fractionMaxSpeed)

    def blinkColors(self, color):
        #Funcion que prende los ojos del robot del color especificado en los argumentos
        rDuration = 0.05
        self.ledsProxy.fadeRGB( "FaceLeds", color, rDuration )
        time.sleep(0.1)
        self.ledsProxy.fadeRGB( "FaceLeds", 0xffffff, rDuration )

    def moveHeadRight(self):
        #Funcion que mueve la cabeza hacia la derecha utilizando la funcion "move"
        names = ["HeadYaw"]
        anglesd = [-45.0]
        fractionMaxSpeed  = 0.20
        self.move(names, anglesd, fractionMaxSpeed)
        time.sleep(1.5)
      
    def moveHeadLeft(self):
        # Funcion que mueve la cabeza hacia la izquierda utilizando la funcion "move"
        names = ["HeadYaw"]
        anglesd = [45.0]
        fractionMaxSpeed  = 0.20
        self.move(names, anglesd, fractionMaxSpeed)
        time.sleep(1.5)

    def talk(self, message1, message2):
        #Funcion que recibe dos mensajes y la velocidad de hablado y hace que el robot lo articule como se le especifica
        #global spd
        str1 = "\\rspd=" + spd + "\\" + message1 + " " + message2
        self.ttsProxy.say(str1)

    def intermediate(self):
        #Funcion en la cual el robot sube un poco sus brazos de la posicion de sentado para evitar choque con las rodillas
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "LShoulderPitch", "LShoulderRoll","LElbowYaw", "LElbowRoll", "LWristYaw","HeadPitch"]
        anglesd = [39.0, -17.3, 29.2, 71.2, -1.5, 39.0, 17.3, -29.2, -71.2, -1.5, 13.0]
        fractionMaxSpeed  = 0.15
        self.move(names, anglesd, fractionMaxSpeed)

    def hiHand(self):
        #Funcion en que el robot hace un saludo complejo, pitch y yaw son parametros para ajustar el angulo de la cabeza
        #global name
        pitch = 15.0
        yaw = 20.0
        shortInterval = 0.07 #Ajustar el tiempo que pasa entre accion en el saludo para lograr mas fluidez
        longInterval = 0.25
        neutralInterval = 0.15

        self.talk("Hola", "")
        time.sleep(1.0)
        self.talk(name, "")
        #1
        anglesd = [78.5, -14.6, 13.8, -17.7, 9.9, 0.43, -0.1 + pitch, 0.0, -78.9, 20.3, 63.6, -45.9, 0.7, 0.24]
        fractionMaxSpeed = 0.15
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(shortInterval)
        #2
        anglesd = [77.5, -15.2, 11.6, -16.8, 9.9, 0.43, -0.1 + pitch, 0.4, -78.9, 20.3, 63.6, -45.9, 0.1, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(shortInterval)
        #3
        anglesd = [72.4, -18.3, 4.9, -12.4, 9.9, 0.43, -0.1 + pitch, 0.4, -78.9, 20.3, 63.6, -45.9, 0.1, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(longInterval)
        #4
        anglesd = [14.3, -54.5, -67.0, 31.8, -17.8, 0.85, -7.1 + pitch, -16.2 + yaw, -75.0, 14.3, 53.8, -40.4, 7.6, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(shortInterval)
        #5
        anglesd = [14.3, -21.5, -67.1, 31.9, -17.7, 0.85, -8.6 + pitch, -18.5 + yaw, -73.9, 13.6, 52.9, -40.1, 8.3, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(shortInterval)
        #6
        anglesd = [14.9, -1.4, -66.2, 31.5, -17.8, 0.85, -9.6 + pitch, -20.1 + yaw, -73.2, 12.8, 53.4, -39.9, 8.3, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(neutralInterval)
        #7
        anglesd = [19.7, -3.2, -65.5, 29.4, -17.8, 0.85, -11.2 + pitch, -21.3 + yaw, -72.2, 12.8, 53.4, -39.9, 8.3, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(longInterval)
        #8
        anglesd = [53.4, -25.9, -62.5, 22.6, -17.8, 0.85, -18.5 + pitch, -23.4 + yaw, -68.1, 12.2, 53.4, -39.4, 8.3, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(shortInterval)
        #9
        anglesd = [52.8, -30.8, -62.5, 21.9, -17.8, 0.85, -19.3 + pitch, -23.4 + yaw, -68.1, 12.2, 53.4, -39.4, 8.3, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(shortInterval)
        #10
        anglesd = [49.4, -35.7, -64.0, 21.3, -17.8, 0.85, -19.3 + pitch, -23.4 + yaw, -68.1, 12.2, 53.4, -39.4, 8.3, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(neutralInterval)
        #11
        anglesd = [39.1, -46.7, -68.4, 20.7, -17.8, 0.85, -16.3 + pitch, -23.4 + yaw, -68.7, 12.2, 52.3, -37.2, 8.3, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(longInterval)
        #12
        anglesd = [11.0, -54.8, -72.1, 20.7, -17.8, 0.85, -6.6 + pitch, -23.4 + yaw, -70.4, 12.2, 49.9, -35.7, 8.3, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(shortInterval)
        #13
        anglesd = [11.0, -53.7, -72.1, 20.0, -17.8, 0.85, -4.3 + pitch, -23.4 + yaw, -70.4, 12.2, 49.9, -35.7, 8.3, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(shortInterval)
        #14
        anglesd = [11.0, -50.4, -72.1, 20.0, -17.8, 0.85, -3.7 + pitch, -24.0 + yaw, -70.4, 12.2, 49.9, -35.7, 8.3, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(neutralInterval)
        #15
        anglesd = [14.5, -33.5, -71.3, 20.0, -17.8, 0.85, -5.0 + pitch, -25.3 + yaw, -73.3, 13.4, 49.9, -38.6, 7.7, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(longInterval)
        #16
        anglesd = [40.4, -19.0, -66.0, 21.4, -17.8, 0.85, -9.5 + pitch, -28.6 + yaw, -75.2, 14.1, 51.2, -42.8, 7.7, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(shortInterval)
        #18
        anglesd = [48.8, -17.7, -55.7, 34.2, -16.3, 0.84, -10.7 + pitch, -29.5 + yaw, -75.2, 14.1, 51.2, -42.8, 7.7, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(neutralInterval)
        #19
        anglesd = [57.9, -15.6, -25.1, 55.5, -9.3, 0.74, -10.7 + pitch, -29.5 + yaw, -74.4, 14.1, 51.2, -42.3, 7.1, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(longInterval)
        #20
        anglesd = [72.2, -14.4, 58.2, 47.5, 10.3, 0.43, -1.3 + pitch, -22.2 + yaw, -68.1, 13.4, 48.5, -38.8, 7.1, 0.24]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(1.5)

    def justPoint(self):
        #Funcion en la que el robot senala hacia el lado derecho derecho mientras voltea

        self.postureProxy.goToPosture("Sit", 0.6)
        self.intermediate()

        #El robot senala
        anglesd = [4.0,-50.0,-85.0,-40.0,60.0,-25.2,-60.2]
        fractionMaxSpeed  = 0.15
        #El robot abre la mano derecha para senalar
        self.motionProxy.post.openHand('RHand')
        time.sleep(0.5)
        self.moveRightSide(anglesd, fractionMaxSpeed)
        time.sleep(0.5)

    def turnHead(self):
        #Funcion en la que el robot solo mira hacia el lado derecho

        self.postureProxy.goToPosture("Sit", 0.6)
        
        # Move Head
        names = ["HeadPitch", "HeadYaw"]
        anglesd = [-25.2, -60.2]
        fractionMaxSpeed  = 0.25
        self.move(names, anglesd, fractionMaxSpeed)


    def coverEyes(self):
        #Funcion en la que el robot se cubre los ojos y pregunta donde esta el nino 


        for x in range(0,repetitions):
            #El robot cubre sus ojos
            anglesd = [87.6, 15.0, 10.0, 64.7, 82.1, 0.0, -7.0, 0.0, -87.6, -15.0, 10.0, -64.7, -82.1, 0.0,]
            fractionMaxSpeed  = 0.15
            self.moveAll(anglesd, fractionMaxSpeed)
            time.sleep(0.5)
            self.talk("Donde esta", name)
            time.sleep(5.0)

            #El robot se destapa los ojos y dice: "aqui esta"
            self.intermediate()
            self.talk("Aaki", "eest a") # es necesario perfeccionar esta pronunciacion
            time.sleep(1.5)
            self.postureProxy.goToPosture("Sit", 0.6)
            time.sleep(3.0)


def main(ip, port):
    """ Main entry point
    """
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       ip,          # parent broker IP
       port)        # parent broker port
   

    global ReactToTouch
    ReactToTouch = ReactToTouch("ReactToTouch")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="10.100.144.42",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)
