import sys
import time

from naoqi import ALModule
from naoqi import ALBroker
from naoqi import ALProxy
import argparse

# Global variable to store the ReactToTouch module instance
ReactToTouch = None
memory = None
counter = 0

name = 'Adrian'
spd = '78'		#Velocidad de habla 20% menor a lo estandar (100), puede ser hasta 400
tiempoInterno= 3.0 	#Tiempo para pasar a la siguiente accion dentro de cada modulo
repetitions = 1		#Numero de repeticiones

checkIntro = False

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

	
      # Condiciones para pasar los estados
        if value == 1.0:
            counter = counter + 1
            if counter == 1:
                checkIntro 	= True
                #self.Intro()

            elif counter == 2:
                checkIntro	= False
                checkSaludar 	= True
                self.Saludar()

            elif counter == 3:
                checkSaludar = False
                checkRespuesta = True
                self.RespuestaAtencion()
            elif counter == 4:
                checkRespuesta = False
                checkarmsUp = True
                self.armsUp()
            elif counter == 5:
                checkarmsUp = False
                checkarmsinFront = True
                self.armsinFront()
            elif counter == 6:
                checkarmsinFront = False
                checktouchHead = True
                self.touchHead()
            elif counter == 7:
                checktouchHead = False                
                checkAnticipacion = True
                self.AnticipacionSocial()
            elif counter == 8:
                checkAnticipacion = False
                checkrobotPide = True
                self.robotPide()
            elif counter == 9:
                checkrobotPide = False
                checkrobotRecibe = True
                self.robotRecibe()
            elif counter == 10:
                checkrobotRecibe = False
                checkrobotEntrega = True
                self.robotEntrega()
            else:
                checkrobotEntrega = False
                checkninoRecibio = True
                self.ninoRecibio()

     
    def Intro(self):
        if checkIntro == True:
           self.motionProxy.wakeUp() 	#Despertar al robot agrega rigidez
           time.sleep(1.0)
           self.postureProxy.goToPosture("Sit", 0.6) # Poner al robot en su posicion inicial sentado
            
        #1 Mueve la cabeza de un lado a otro - 2 veces
        for x in range(1):
            if checkIntro == True:
                self.moveHeadRight() 	#Derecha
                self.moveHeadLeft() 	#Izquierda
                self.moveHeadCenter() 	#Centro
                time.sleep(2.0)

                self.moveHeadDown()		#Mira en direccion al nino
                time.sleep(1.0)

        #2 LEDs de ojos parpadean
        colors = ["white","red","green","blue", "yellow","magenta","cyan"] #Colores de ojos del robot
        for y in range(0,3): 	#Ilumina con todos los colores 3 veces
            if checkIntro == True:
                for x in colors:
                    self.blinkColors(x) #Utiliza "blinkColors" para el parpadeo de cada color

        #3 Nombre del nino
        for x in range(0,repetitions):
            if checkIntro == True:
                self.talk(name,"") 	#Utiliza la funcion "talk" donde lo que dice el robot es el nombre
                time.sleep(tiempoInterno) 


    def Saludar(self):
        #1 Saluda verbalmente
        #2 Saluda verbalmente + Mov. brazo derecho

        self.motionProxy.wakeUp()

        #1 Saludo verbal 
        if checkSaludar == True:
           self.motionProxy.openHand('RHand')        
           self.talk("Hola", name)
           time.sleep(tiempoInterno)

        #2 Saludo Verbal + Mov. brazo derecho
        if checkSaludar == True:
           self.talk("Hola", name)
           self.hiHand()
           self.motionProxy.closeHand('RHand')
           self.motionProxy.rest() 	#Apaga los motores 	
           time.sleep(tiempoInterno)


    def RespuestaAtencion(self):
        #1 Mira a la derecha
        #2 Mira a la derecha + voz
        #3 Mira a la derecha + voz + Mov. Mano
        self.motionProxy.wakeUp() 	#Despertar al robot agrega rigidez

        #1 Mira a la derecha 
        if checkRespuesta == True:
            self.turnHead() 		#Funcion para que mire a la derecha y arriba
            time.sleep(tiempoInterno)	#Tiempo interno para la siguiente actividad dentro del modulo (#2)
            self.moveHeadDown()
            time.sleep(1.0)


        #2 Voz (Mira eso)   + Mira a la derecha 
        if checkRespuesta == True:
            self.turnHead()		# Mira a la derecha y arriba	
            self.talk(name, "Mira eso")	# Dice "nombre" + mira eso
            time.sleep(tiempoInterno) 	# Tiempo interno para la siguiente actividad dentro del modulo (#3)
            self.moveHeadDown()		# Regresa a mirar al nino
            time.sleep(1.0)

        #3 Voz (Mira eso)   + Mira a la derecha  + Mov. Mano: Robot        
        if checkRespuesta == True:
            self.justPoint()
            self.talk(name, "Mira eso")
            time.sleep(tiempoInterno)
            self.brazosinicial()
            time.sleep(2.0)
            self.motionProxy.rest()
            

    def armsUp(self):
        #Funcion en la que el robot sube sus brazos y le pide al nino que lo imite
        self.motionProxy.wakeUp()
        for x in range(0,repetitions):
            if checkarmsUp == True:
                self.talk(name, "Has")
                time.sleep(0.1)
                self.talk("esto","")
                self.intermediate()		#Posicion intermedia para completar 
                time.sleep(1.0)
                
                anglesd = [40.9, -32.7, -75.0, -4.6, 92.1, 0.59, 11.0, 0.0, -40.9, 32.7, -75.0, -4.6, -92.1, 0.59]
                fractionMaxSpeed  = 0.15
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(2.5) 		#Tiempo para completar el movimiento
                time.sleep(tiempoInterno) 	#Tiempo en el que se queda con las manos extendidas
                self.brazosinicial()  		#Mueve solo los brazos a su posicion inicial evitando usar sitdown
                time.sleep(2.0)                
                self.motionProxy.rest()
            

    def armsinFront(self):
        #Funcion en la que el robot pone sus brazos hacia el frente y le pide al nino que lo imite
        self.motionProxy.wakeUp()
        for x in range(0,repetitions):
            if checkarmsinFront == True:
                #El robot pone sus brazos hacia el frente y dice: "has esto"                               
                self.talk(name, "has")
                time.sleep(0.1)
                self.talk("esto", "")
     
                #Brazos enfrente
                anglesd = [2.0, 2.0, 10.0, 21.3, -19.6, 1, 11.0, -0.8, -2.0, -2.0, 10.0 , -21.3 , 19.6, 1]
                fractionMaxSpeed = 0.15
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(1.5) 		#Tiempo para completar el movimiento
                time.sleep(tiempoInterno)	#Tiempo en el que se queda con las manos extendidas

                #Brazos flexionados antes de ir hacia la posicion inicial
                anglesd = [70.2, 2.1, 15.1, 26.6, -3.0, 0.50, 11.0, -0.8, -70.2, -2.1, 15.1, -26.6, 3.0, 0.50]
                fractionMaxSpeed = 0.15
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(1.5)

                self.brazosinicial()		#Mueve solo los brazos a su posicion inicial evitando usar sitdown
                time.sleep(1.0)		
                self.motionProxy.rest()

    def touchHead(self):
        #Funcion en la que el robot toca su cabeza y le pide al nino que lo imite
        self.motionProxy.wakeUp()
        for x in range(0,repetitions):
            if checktouchHead == True:
                
                #El robot toca su cabeza y dice "has esto"
                self.talk(name, "has")
                time.sleep(0.1)
                self.talk("esto", "")
                
                #Paso previo		
                anglesd = [70.1, -15.0, 15.0 , 27.0, -1.2, 0.3, 15.0, 0.0, -70.1, 15.0, 15.0, -27.0 , 1.2, 0.3]
                fractionMaxSpeed  = 0.2
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(0.3)		        #Pequeno tiempo importante para que realice esta accion

                #Se toca la cabeza
                anglesd = [69.5, -17.8, -71.5, 5.0 , 90.0, 0.65 , 5.0, 0.0, -69.5, 17.8, -71.5, -5.0, -91.0, 0.65]                
                fractionMaxSpeed  = 0.15
                self.moveAll(anglesd, fractionMaxSpeed)
                time.sleep(2.0)
                time.sleep(tiempoInterno)
                
                self.brazosinicial()		#Mueve solo los brazos a su posicion inicial evitando usar sitdown
                time.sleep(2.5)		
                self.motionProxy.rest()

    def AnticipacionSocial(self):
        #Robot se tapa los ojos y pregunta donde esta el nino, luego los destapa y dice: "aqui esta"
        self.motionProxy.wakeUp()
        for x in range(0,repetitions):
            if checkAnticipacion == True:
                
                self.coverEyes()
                self.talk("Donde esta", name)
                time.sleep(tiempoInterno)

                #El robot se destapa los ojos y dice: "aqui esta"
                self.brazosinicial()
                self.talk("aqui", "") # es necesario perfeccionar esta pronunciacion
                self.talk("esta", "") # es necesario perfeccionar esta pronunciacion
                time.sleep(1.0)
                self.motionProxy.rest()

    def robotPide(self):
        #Funcion en la que el robot le pide al nino un objeto y lo recibe

        if checkrobotPide == True:
            self.motionProxy.wakeUp()
                        
            #El robot extiende el brazo, abre la mano y dice: "Dame"
            anglesd = [3.0, 4.0, 28.0, 119.0, 60.0, 10.0, 0.0]
            fractionMaxSpeed  = 0.1
            self.moveRightSide(anglesd, fractionMaxSpeed)
            self.motionProxy.openHand('RHand')
            self.talk(name, "")
            time.sleep(1.0)
            self.talk("Dame", "")

    def robotRecibe(self):
        #El robot agarra el objeto
        if checkrobotRecibe == True:        
            self.motionProxy.closeHand('RHand') #Debe ser cambiado a un angulo
            time.sleep(0.5)
            self.brazoalzado()
            time.sleep(0.5)
            self.brazosinicial()		
            

    def robotEntrega(self):
        #Funcion en la que el robot le entrega el objeto al nino
        self.motionProxy.wakeUp()
        if checkrobotEntrega == True:
            #El robot extiendo su brazo y abre la mano para entregar el objeto
            anglesd = [3.0, 4.0, 28.0, 119.0, 60.0, 10.0, 0.0]
            fractionMaxSpeed  = 0.1
            self.moveRightSide(anglesd, fractionMaxSpeed)
            self.talk(name, "")
            time.sleep(1.0)
            self.talk("Toma", "")
            self.motionProxy.openHand('RHand')
        
    def ninoRecibio(self):
        if checkninoRecibio == True:
            self.motionProxy.closeHand('RHand')
            self.brazoalzado()
            time.sleep(0.5)
            self.brazosinicial()
            self.motionProxy.setStiffnesses("Body", 0.0)



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

    def moveHeadCenter(self):
        # Funcion que mueve la cabeza hacia al centro utilizando la funcion "move"
        names = ["HeadPitch","HeadYaw"]
        anglesd = [0.0, 0.0]
        fractionMaxSpeed  = 0.1
        self.move(names, anglesd, fractionMaxSpeed)
        #time.sleep(1.5)

    def moveHeadDown(self):
        # Funcion que mueve la cabeza en direccion al nino 
        names = ["HeadPitch","HeadYaw"]
        anglesd = [15.0, 0.0]
        fractionMaxSpeed  = 0.12
        self.move(names, anglesd, fractionMaxSpeed)
        time.sleep(1.0)


    def talk(self, message1, message2):
        #Funcion que recibe dos mensajes y la velocidad de hablado y hace que el robot lo articule como se le especifica
        #global spd

	# Say the sentence 50% slower than normal speed
	# tts.say("\\rspd=50\\hello my friends")

        str1 = "\\rspd=" + spd + " \\   " + message1 + "    " + message2
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
        anglesd = [70.1, -15.0, 53.4, 26.6, -2.1, 0.3, -1.3 + pitch, -22.2 + yaw, -68.3, 13.8, 53.0, -27.2 , 4.3, 0.29]
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(1.5)


#  names = ["RElbowRoll","RShoulderRoll","RShoulderPitch","RElbowYaw","RWristYaw","RHand","HeadPitch", "HeadYaw","LElbowRoll","LShoulderRoll","LShoulderPitch","LElbowYaw","LWristYaw","LHand"]


    def justPoint(self):
        #Funcion en la que el robot senala hacia el lado derecho derecho mientras voltea

        self.intermediate()
            
        #El robot abre la mano derecha para senalar
        self.motionProxy.post.openHand('RHand')
        time.sleep(0.5)

        #El robot senala
        anglesd = [4.0,-50.0,-85.0,-40.0,60.0,-25.2,-60.2]
        fractionMaxSpeed  = 0.15
        self.moveRightSide(anglesd, fractionMaxSpeed)
        time.sleep(0.5)
        

    def turnHead(self):
        #Funcion en la que el robot solo mira hacia el lado derecho y luego hacia arriba
             
        names = ["HeadPitch", "HeadYaw"]
        anglesd = [-25.2, -60.2]
        fractionMaxSpeed  = 0.2
        self.move(names, anglesd, fractionMaxSpeed)
        time.sleep(0.7)


    def coverEyes(self):
        #Funcion en la que el robot se cubre los ojos y pregunta donde esta el nino 


        for x in range(0,repetitions):
            #El robot cubre sus ojos
            anglesd = [87.6, 15.0, 10.0, 64.7, 82.1, 0.0, -7.0, 0.0, -87.6, -15.0, 10.0, -64.7, -82.1, 0.0,]
            fractionMaxSpeed  = 0.15
            self.moveAll(anglesd, fractionMaxSpeed)
            time.sleep(0.5)
            

    def brazosinicial(self):
        pitch = 15.0
        yaw = 20.0
        anglesd = [70.1, -15.0, 53.4, 26.6, -2.1, 0.3, -1.3 + pitch, -22.2 + yaw, -68.3, 13.8, 53.0, -27.2 , 4.3, 0.29]
        fractionMaxSpeed  = 0.2
        self.moveAll(anglesd, fractionMaxSpeed)
        time.sleep(1.0)		#Tiempo que toma hacer el movimiento
        


    def brazoalzado(self):
        anglesd=[58.6, -3.4, 31.6, 110.4, 72.2, 13.7,-2.2]
        fractionMaxSpeed  = 0.2
        self.moveRightSide(anglesd, fractionMaxSpeed)	


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
    parser.add_argument("--ip", type=str, default="10.100.144.34",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)
