import RPi.GPIO as gpio
import time
import numpy as np

def get_distance(setmode=gpio.BOARD,TRIG=36,ECHO=37,max_wait_time=5):
   '''
   calculate the distance between the obstacle and ultrasonic sensor (US-015)
   :param setmode: could be GPIO.BOARD or GPIO.BCM
   :param TRIG: trigger pin number for raspberry pie
   :param ECHO: echo pin number for raspberry pie
   :param max_wait_time: max wait time for receiving the signal
   :return:
   '''
   gpio.setmode(setmode)

   gpio.setup(TRIG, gpio.OUT)
   gpio.setup(ECHO, gpio.IN)
   gpio.output(TRIG,True)
   time.sleep(0.001)
   gpio.output(TRIG,False)
   wait_start = time.time()
   try:
      while gpio.input(ECHO) == False:
        ## exit if the wait is longer than max_wait_time
        if time.time()> wait_start + max_wait_time:
            return np.nan
        else:
            pass
      start = time.time()
      while gpio.input(ECHO) == True:
        end = time.time()

      ##clear the channel
      gpio.cleanup()

      sig_time = end - start
      # cm:
      distance = sig_time / 0.000058
      return distance

   except:

       gpio.cleanup()
       return np.nan



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
