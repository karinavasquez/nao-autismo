import argparse
from naoqi import ALProxy
import time

# USAR EL CODIGO PARA GRABAR VIDEO Y SONIDO Y ADAPTARLO A AllTaskswithInputControl.py CUANDO ESTE FINALIZADO

def Introduccion(entry):
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd, robotIP, PORT] = getRobotInfo(entry)

    ############################# USE THE FUNCTION TO RECORD VIDEO AND SOUND #####################################
    [videoRecorderProxy, audioRecorderProxy] = recordVideoSound(robotIP, PORT, "Introduccion")   

    # Wake up robot
    motionProxy.wakeUp()
    # Send robot to initial position: sitting down
    postureProxy.goToPosture("Sit", 0.6)

    for x in range(0,2):
        moveHeadRight(motionProxy)
        moveHeadLeft(motionProxy)
    
    postureProxy.goToPosture("Sit", 0.6)

    names = ["HeadPitch","HeadYaw"]
    anglesd = [20.0, 0.0]
    fractionMaxSpeed  = 0.05
    # Move head and arms
    move(motionProxy, names, anglesd, fractionMaxSpeed)
    time.sleep(1.0)

    blinkColors(ledsProxy, "red")
    time.sleep(1.0)
    blinkColors(ledsProxy, "green")
    time.sleep(1.0)
    blinkColors(ledsProxy, "blue")
    time.sleep(1.0)
    blinkColors(ledsProxy, "yellow")
    time.sleep(1.0)
    blinkColors(ledsProxy, "magenta")
    time.sleep(1.0)
    blinkColors(ledsProxy, "cyan")
    time.sleep(1.0)
    blink(ledsProxy)
    
    for x in range(0,2):
        talk(ttsProxy, ledsProxy, name, spd, "")
        time.sleep(2.0)

    ############################# STOP RECORDING VIDEO AND SOUND ##########################################
    videoInfo = videoRecorderProxy.stopRecording()
    audioRecorderProxy.stopMicrophonesRecording()


def Saludar(entry):
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd, robotIP, PORT] = getRobotInfo(entry)

    [videoRecorderProxy, audioRecorderProxy] = recordVideoSound(robotIP, PORT, "Saludar")   

    # Wake up robot
    motionProxy.wakeUp()
    
    # Send robot to initial position: sitting down
    postureProxy.goToPosture("Sit", 0.6)

    # intermediate position
    intermediate(motionProxy)
    motionProxy.post.openHand('RHand')

    sayHi1(motionProxy, postureProxy, ttsProxy, ledsProxy)
    talk(ttsProxy, ledsProxy, "Hola", spd, name)
    sayHi2(motionProxy, postureProxy, ttsProxy, ledsProxy)
    sayHi1(motionProxy, postureProxy, ttsProxy, ledsProxy)
    time.sleep(1.0)

    goBackInitial(motionProxy, postureProxy, 1.5)
    
    # Video
    videoInfo = videoRecorderProxy.stopRecording()
    audioRecorderProxy.stopMicrophonesRecording()


def RespuestaAtencion(entry):
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd, robotIP, PORT] = getRobotInfo(entry)
    
    [videoRecorderProxy, audioRecorderProxy] = recordVideoSound(robotIP, PORT, "RespuestaAtencion")

    turnHead(motionProxy, postureProxy, ttsProxy, ledsProxy)
    
    justPoint(motionProxy, postureProxy)
    time.sleep(2.5)
    goBackInitial(motionProxy, postureProxy, 1.5)

    justPoint(motionProxy, postureProxy)
    talk(ttsProxy, ledsProxy, name, spd, "Mira eso")
    time.sleep(5.0)
    goBackInitial(motionProxy, postureProxy, 1.5)

    # Video
    videoInfo = videoRecorderProxy.stopRecording()
    audioRecorderProxy.stopMicrophonesRecording()
  

def Imitacion(entry):
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd, robotIP, PORT] = getRobotInfo(entry)

    [videoRecorderProxy, audioRecorderProxy] = recordVideoSound(robotIP, PORT, "Imitacion")   
    
    # Wake up robot
    motionProxy.wakeUp()

    armsUp(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd)
    armsinFront(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd)
    touchHead(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd)

    # Video
    videoInfo = videoRecorderProxy.stopRecording()
    audioRecorderProxy.stopMicrophonesRecording()


def AnticipacionSocial(entry):
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd, robotIP, PORT] = getRobotInfo(entry)

    [videoRecorderProxy, audioRecorderProxy] = recordVideoSound(robotIP, PORT, "AnticipacionSocial")   
    
    # Wake up robot
    motionProxy.wakeUp()
    
    # Send robot to initial position: sitting down
    postureProxy.goToPosture("Sit", 0.6)

    # intermediate position
    intermediate(motionProxy)
    
    coverEyes(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd)

    goBackInitial(motionProxy, postureProxy, 1.5)

    # Video
    videoInfo = videoRecorderProxy.stopRecording()
    audioRecorderProxy.stopMicrophonesRecording()


def EntregarRecibir(entry):
    [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd, robotIP, PORT] = getRobotInfo(entry)

    [videoRecorderProxy, audioRecorderProxy] = recordVideoSound(robotIP, PORT, "EntregarRecibir")   

    # Wake up robot
    motionProxy.wakeUp()
    
    # Send robot to initial position: sitting down
    postureProxy.goToPosture("Sit", 0.6)

    intermediate(motionProxy)
    robotRecibe(motionProxy, ttsProxy, ledsProxy, name, spd)  
    intermediate(motionProxy)
    time.sleep(3.0)
    intermediate(motionProxy)
    robotEntrega(motionProxy, ttsProxy, ledsProxy, name, spd)
    
    goBackInitial(motionProxy, postureProxy, 0)

    # Video
    videoInfo = videoRecorderProxy.stopRecording()
    audioRecorderProxy.stopMicrophonesRecording()
   

def getRobotInfo(entry):
    robotIP = entry["ip"].get()
    PORT = eval(entry["port"].get())
    name = entry["name"].get()
    spd  = entry["vel"].get()
    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    ttsProxy     = ALProxy("ALTextToSpeech", robotIP, PORT)
    ledsProxy    = ALProxy("ALLeds", robotIP, PORT)
    return [motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd, robotIP, PORT]


############################# FUNCION QUE EMPIEZA A GRABAR EL VIDEO Y SONIDO #####################################

def recordVideoSound(robotIP, PORT, filename):
    try:
	    videoRecorderProxy = ALProxy("ALVideoRecorder",robotIP,PORT)
    except Exception, e:
	    print "Error when creating ALVideoRecorder proxy:"
	    print str(e)
	    exit(1)

    try:
	    audioRecorderProxy = ALProxy("ALAudioRecorder",robotIP,PORT)
    except Exception, e:
	    print "Error when creating ALAudioRecorder proxy:"
	    print str(e)
	    exit(1)

    channels = (0,1,0,0)
        
    strRecording = "/home/nao/recordings/tests/" + filename + ".wav"

    audioRecorderProxy.startMicrophonesRecording(strRecording,"wav", 16000,channels)

    videoRecorderProxy.setCameraID(0)
    videoRecorderProxy.setFrameRate(10.0)
    videoRecorderProxy.setResolution(2)
    videoRecorderProxy.startRecording("/home/nao/recordings/tests", filename)
    return [videoRecorderProxy, audioRecorderProxy]


def goBackInitial(motionProxy, postureProxy, sleepTime):
    intermediate(motionProxy)
    time.sleep(sleepTime)
    postureProxy.goToPosture("Sit", 0.6)

def move(motionProxy, names, anglesd, fractionMaxSpeed):
    angles = [val/180.*3.14159265 for val in anglesd]
    motionProxy.setAngles(names, angles, fractionMaxSpeed)

def moveAll(motionProxy, anglesd, fractionMaxSpeed):
    names = ["RElbowRoll","RShoulderRoll","RShoulderPitch","RElbowYaw","RWristYaw","RHand","HeadPitch", "HeadYaw","LElbowRoll","LShoulderRoll","LShoulderPitch","LElbowYaw","LWristYaw","LHand"]
    move(motionProxy, names, anglesd, fractionMaxSpeed)

def moveRightSide(motionProxy, anglesd, fractionMaxSpeed):
    names = ["RElbowRoll","RShoulderRoll","RShoulderPitch","RElbowYaw","RWristYaw","HeadPitch", "HeadYaw"]
    move(motionProxy, names, anglesd, fractionMaxSpeed)

def blink(ledsProxy):
    rDuration = 0.05
    ledsProxy.post.fadeRGB( "FaceLed0", 0x000000, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed1", 0x000000, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed2", 0xffffff, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed3", 0x000000, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed4", 0x000000, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed5", 0x000000, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed6", 0xffffff, rDuration )
    ledsProxy.fadeRGB( "FaceLed7", 0x000000, rDuration )
    time.sleep( 0.1 )
    ledsProxy.fadeRGB( "FaceLeds", 0xffffff, rDuration )

def blinkColors(ledsProxy, color):
    rDuration = 0.1
    ledsProxy.post.fadeRGB( "FaceLed0", color, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed1", color, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed2", color, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed3", color, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed4", color, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed5", color, rDuration )
    ledsProxy.post.fadeRGB( "FaceLed6", color, rDuration )
    ledsProxy.fadeRGB( "FaceLed7", color, rDuration )
    time.sleep( 0.1 )
    #ledsProxy.fadeRGB( "FaceLeds", 0xffffff, rDuration )

def moveHeadRight(motionProxy):   
    # Move
    names = ["HeadYaw"]
    anglesd = [-45.0]
    fractionMaxSpeed  = 0.20
    # Move head and arms
    move(motionProxy, names, anglesd, fractionMaxSpeed)
    time.sleep(1.5)
  
def moveHeadLeft(motionProxy):
    # Move
    names = ["HeadYaw"]
    anglesd = [45.0]
    fractionMaxSpeed  = 0.20
    # Move head and arms
    move(motionProxy, names, anglesd, fractionMaxSpeed)
    time.sleep(1.5)

def talk(ttsProxy, ledsProxy, message1, spd, message2):
    str1 = "\\rspd=" + spd + "\\" + message1 + " " + message2
    ttsProxy.say(str1)
    blink(ledsProxy)

def intermediate(motionProxy):
    names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "LShoulderPitch", "LShoulderRoll","LElbowYaw", "LElbowRoll", "LWristYaw"]
    anglesd = [50.0, -17.3, 29.2, 71.2, -1.5, 50.0, 17.3, -29.2, -71.2, -1.5]
    fractionMaxSpeed  = 0.35
    move(motionProxy, names, anglesd, fractionMaxSpeed)

def secondIntermediate(motionProxy):
    anglesd = [52.9, -9.1, 34.0, -37.3, 104.0, 0.58, -4.0, 0.0, -52.9, 9.1, 34.0, 37.3, -104.0, 0.58]
    fractionMaxSpeed  = 0.2
    moveAll(motionProxy, anglesd, fractionMaxSpeed)

def sayHi1(motionProxy, postureProxy, ttsProxy, ledsProxy):  
    # Move
    anglesd = [65.0, -65.6, 55.5, 119.0, 4.6, -7.0, 0.0]
    fractionMaxSpeed  = 0.15
    # Move head and arms
    moveRightSide(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(1.0)
  
def sayHi2(motionProxy, postureProxy, ttsProxy, ledsProxy):
    anglesd = [88.3, -65.6, 80.2, 119.0, 4.6, -7.0, 0.0]
    fractionMaxSpeed  = 0.15
    # Move
    moveRightSide(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(1.0)

def justPoint(motionProxy, postureProxy):
    # Wake up robot
    motionProxy.wakeUp()
    
    # Send robot to initial position: sitting down
    postureProxy.goToPosture("Sit", 0.6)

    # intermediate position
    intermediate(motionProxy)
    # Move
    anglesd = [4.0,-50.0,-85.0,-40.0,60.0,-25.2,-60.2]
    fractionMaxSpeed  = 0.25

    # Open right hand
    motionProxy.post.openHand('RHand')
    time.sleep(0.5)
    
    # Move head and arms
    moveRightSide(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(0.5)

def turnHead(motionProxy, postureProxy, ttsProxy, ledsProxy):
    motionProxy.wakeUp()
    
    # Send robot to initial position: sitting down
    postureProxy.goToPosture("Sit", 0.6)
    
    # Move Head
    names = ["HeadPitch", "HeadYaw"]
    anglesd = [-25.2, -60.2]
    fractionMaxSpeed  = 0.25
    move(motionProxy, names, anglesd, fractionMaxSpeed)
    time.sleep(2.0)
    postureProxy.goToPosture("Sit", 0.6)

def touchHead(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd):
    # Send robot to initial position: sitting down
    postureProxy.goToPosture("Sit", 0.6)

    # intermediate position
    intermediate(motionProxy)

    # touch head
    anglesd = [86.3, -32.7, -75.0, -4.6, 92.1, 0.59, -4.0, 0.0, -86.3, 32.7, -75.0, -4.6, -92.1, 0.59]
    fractionMaxSpeed  = 0.15 #de 0 a 1 (1 mas rapido)

    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    talk(ttsProxy, ledsProxy, name, spd, "has esto")
    time.sleep(5.0)
    
    goBackInitial(motionProxy, postureProxy, 2.0)
    # Go back to initial position
    #intermediate(motionProxy)
    #time.sleep(2.0)
    #postureProxy.goToPosture("Sit", 0.6)

def armsUp(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd):
    
    # Send robot to initial position: sitting down
    postureProxy.goToPosture("Sit", 0.6)

    # intermediate position
    intermediate(motionProxy)

    # touch head
    anglesd = [40.9, -32.7, -75.0, -4.6, 92.1, 0.59, -4.0, 0.0, -40.9, 32.7, -75.0, -4.6, -92.1, 0.59]
    fractionMaxSpeed  = 0.15 #de 0 a 1 (1 mas rapido)

    # Move head and arms
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    talk(ttsProxy, ledsProxy, name, spd, "has esto")
    blink(ledsProxy)
    time.sleep(5.0)

    goBackInitial(motionProxy, postureProxy, 2.0)

   # Go back to initial position
    #intermediate(motionProxy)
    #time.sleep(2.0)
    #postureProxy.goToPosture("Sit", 0.6)
 
def armsinFront(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd):
    
    # Send robot to initial position: sitting down
    postureProxy.goToPosture("Sit", 0.6)

    # intermediate position
    secondIntermediate(motionProxy)
    time.sleep(1.0)

    # arms up
    anglesd = [2.2, 10.7, 3.8, -92.5, 92.1, 0.58, -4.0, 0.0, -2.2, -10.7, 3.8, 92.5, -92.1, 0.58]
    fractionMaxSpeed  = 0.15 #de 0 a 1 (1 mas rapido)

    # Move head and arms
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    talk(ttsProxy, ledsProxy, name, spd, "has esto")
    blink(ledsProxy)
    time.sleep(5.0)
    
    goBackInitial(motionProxy, postureProxy, 1.0)

   # Go back to initial position
    #secondIntermediate(motionProxy)
    #time.sleep(1.0)
    #postureProxy.goToPosture("Sit", 0.6)

def coverEyes(motionProxy, postureProxy, ttsProxy, ledsProxy, name, spd):
    # Move
    anglesd = [87.6, 15.0, 10.0, 64.7, 82.1, 0.0, -7.0, 0.0, -87.6, -15.0, 10.0, -64.7, -82.1, 0.0,]
    fractionMaxSpeed  = 0.25

    # Move head and arms
    moveAll(motionProxy, anglesd, fractionMaxSpeed)
    time.sleep(0.5)

    talk(ttsProxy, ledsProxy, "Donde esta", spd, name)
    time.sleep(5.0)

def robotRecibe(motionProxy, ttsProxy, ledsProxy, name, spd):
    anglesd = [3.0, 4.0, 28.0, 119.0, 60.0, 10.0, 0.0]
    fractionMaxSpeed  = 0.08

    moveRightSide(motionProxy, anglesd, fractionMaxSpeed)
    motionProxy.openHand('RHand')

    talk(ttsProxy, ledsProxy, name, spd, "Dame")
    time.sleep(5.0)

    motionProxy.closeHand('RHand')
    time.sleep(1.0)


def robotEntrega(motionProxy, ttsProxy, ledsProxy, name, spd):
    anglesd = [3.0, 4.0, 28.0, 119.0, 60.0, 10.0, 0.0]
    fractionMaxSpeed  = 0.08

    moveRightSide(motionProxy, anglesd, fractionMaxSpeed)

    talk(ttsProxy, ledsProxy, name, spd, "Toma")
    time.sleep(2.0)
    motionProxy.openHand('RHand')
    time.sleep(5.0)

  

