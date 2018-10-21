import RPi.GPIO as GPIO
import time

def change_pos(setmode=GPIO.BOARD,pos="neutral",servoPIN=29, rottime=1):
   '''
   change the position of servo to an assigned "pos"
   :param setmode: could be GPIO.BOARD or GPIO.BCM
   :param pos: neutral, left or right
   :param servoPIN: dedicated pin number on the raspberry pie
   :param rottime: total time interval in seconds to make the rotation
   :return: None
   '''
   GPIO.setmode(setmode)
   GPIO.setup(servoPIN, GPIO.OUT)

   p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
   p.start(2.5) # Initialization
   start=time.time()
   end=time.time()+rottime
   try:
       while time.time() <= end:
          if pos == "neutral":
             p.ChangeDutyCycle(7.5)  # pos towards 90 degree
          elif pos == "right":
             p.ChangeDutyCycle(2.5)  # pos towards 0 degree
          elif pos == "left":
             p.ChangeDutyCycle(12.5) # pos towards 180 degree
          else:
             raise("invalid pos")
       p.stop()

   except KeyboardInterrupt:
       p.stop()
       GPIO.cleanup()
   finally:
       GPIO.cleanup()
       return

if __name__ == "__main__":
    import sys
    pos=sys.argv[1]
    servoPIN = 29
    setmode=GPIO.BOARD
    change_pos(setmode,pos=pos,servoPIN=servoPIN)
