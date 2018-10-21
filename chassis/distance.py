import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)

TRIG = 36
ECHO = 37
gpio.BOARD
def get_distance(setmode,TRIG=36,ECHO=37):
   '''
   calculate the distance between the obstacle and ultrasonic sensor (US-015)
   :param setmode: could be GPIO.BOARD or GPIO.BCM
   :param TRIG: trigger pin number for raspberry pie
   :param ECHO: echo pin number for raspberry pie
   :return:
   '''
   gpio.setmode(setmode)

   gpio.setup(TRIG, gpio.OUT)
   gpio.setup(ECHO, gpio.IN)
   gpio.output(TRIG,True)
   time.sleep(0.001)
   gpio.output(TRIG,False)

   while gpio.input(ECHO) == False:
        pass
   start = time.time()
   while gpio.input(ECHO) == True:
       end = time.time()
   ##clear the channel
   gpio.cleanup()

   sig_time = end - start
   #cm:
   distance = sig_time / 0.000058
   return distance


if __name__ == "__main__":
    TRIG = 36
    ECHO = 37
    setmode=gpio.BOARD
    for i in range(20):
        start = time.time()
        dist=get_distance(setmode,TRIG=36,ECHO=37)
        print("disitance: {} CM".format(dist))
        end = time.time()
        print(end-start)
        time.sleep(1)
