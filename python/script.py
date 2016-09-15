import webiopi
import datetime
#import Adafruit_DHT as dht
import sys

GPIO = webiopi.GPIO

VDHT = 6
Dth = 19
Pluz=  17
Pcascada = 27
Plluvia = 12
Pcalefactor = 13
Ppeltier = 14
Tmin=22
Tmax=28
Hmin=100
Hmax=0
HoraLuzOn  = 9  # Turn Light ON at 08:00
HoraLuzOff = 20 # Turn Light OFF at 18:00
t = 1
h = 2
AUTO = True
TemperaturaElevada = 0

# setup function is automatically called at WebIOPi startup
def setup():
    # set the GPIO used by the light to output
    GPIO.setFunction(VDHT, GPIO.OUT) #pin 6 5V DHT
    GPIO.setFunction(Pluz, GPIO.OUT)
    GPIO.setFunction(Pcascada, GPIO.OUT)
    GPIO.setFunction(Plluvia, GPIO.OUT)
    GPIO.setFunction(Pcalefactor, GPIO.OUT)
    GPIO.setFunction(Ppeltier, GPIO.OUT)

    GPIO.digitalWrite(VDHT, GPIO.HIGH) #pin 6 5V DHT
    GPIO.digitalWrite(Pcascada, GPIO.LOW)
    GPIO.digitalWrite(Plluvia, GPIO.HIGH)
    GPIO.digitalWrite(Pcalefactor, GPIO.HIGH)
    GPIO.digitalWrite(Pluz, GPIO.HIGH)
    GPIO.digitalWrite(Ppeltier, GPIO.HIGH)


    hora = datetime.datetime.now()

    if ((hora.hour >= HoraLuzOn) and (hora.hour < HoraLuzOff)):
        GPIO.digitalWrite(Pluz, GPIO.HIGH)

# loop function is repeatedly called by WebIOPi 
def loop():
    hora = datetime.datetime.now()
    if (AUTO):

    # toggle light ON all days at the correct time
        if ((hora.hour == HoraLuzOn) and (hora.minute == 0) and (hora.second == 0)):
            if (GPIO.digitalRead(Pluz) == GPIO.LOW):
                GPIO.digitalWrite(Pluz, GPIO.HIGH)

    # toggle light OFF
        if ((hora.hour == HoraLuzOff) and (hora.minute == 0) and (hora.second == 0)):
            if (GPIO.digitalRead(Pluz) == GPIO.HIGH):
                GPIO.digitalWrite(Pluz, GPIO.LOW)

    #h,t = dht.read_retry(dht.DHT22, Dth)
        h=1
        t=25
        if t<Tmin:
            if (GPIO.digitalRead(Pcalefactor) == GPIO.HIGH):
                GPIO.digitalWrite(Pcalefactor, GPIO.LOW)
        if t>Tmax:
            if (GPIO.digitalRead(Pcalefactor) == GPIO.LOW):
                GPIO.digitalWrite(Pcalefactor, GPIO.HIGH)
        if t>30:
            TemperaturaElevada = 1
        if (t<28) and (TemperaturaElevada == 1):
            TemperaturaElevada = 0          

        if (hora.hour==10 and hora.minute==50) or (hora.hour==12 and hora.minute==0) or (hora.hour==13 and hora.minute==50) or (hora.hour==16 and hora.minute==50) or (hora.hour==19 and hora.minute==50) or (hora.hour==22 and hora.minute==50):
            GPIO.digitalWrite(Plluvia, GPIO.LOW)
            time.sleep(30)
            GPIO.digitalWrite(Plluvia, GPIO.HIGH)
        if (TemperaturaElevada):
            GPIO.digitalWrite(Ppeltier, GPIO.LOW)


    # gives CPU some time before looping again
    webiopi.sleep(1)

# destroy function is called at WebIOPi shutdown
def destroy():
    GPIO.digitalWrite(Pluz, GPIO.LOW)
    GPIO.digitalWrite(Pcascada, GPIO.LOW)
    GPIO.digitalWrite(Plluvia, GPIO.HIGH)
    GPIO.digitalWrite(Pcalefactor, GPIO.HIGH)
    GPIO.digitalWrite(Pluz, GPIO.HIGH)
    GPIO.digitalWrite(peltier, GPIO.HIGH)

@webiopi.macro
def getTemperaturaHumedad():
    return "%d;%d" % (t, h)

@webiopi.macro
def getLuzHours():
    return "%d;%d" % (HoraLuzOn, HoraLuzOff)

@webiopi.macro
def setLuzHours(on, off):
    global HoraLuzOn, HoraLuzOff
    HoraLuzOn = int(on)
    HoraLuzOff = int(off)
    return getLuzHours()

@webiopi.macro
def getTemperaturaLimits():
    return "%d;%d" % (Tmin, Tmax)

@webiopi.macro
def setTemperaturaLimits(on, off):
    global Tmin, Tmax
    Tmin = int(on)
    Tmax = int(off)
    return getTemperaturaLimits()

@webiopi.macro
def getModo():
    if (AUTO):
        return "auto"
    return "manual"

@webiopi.macro
def setModo(modo):
    global AUTO
    if (mode == "auto"):
        AUTO = True
    elif (mode =="manual"):
        AUTO = FALSE
    return getModo()
