import curses
import distance
import servo
import RPi.GPIO as GPIO
import time
import math

def no_obstacle(threshold=20):
    dist = distance.get_distance()
    if (not math.isnan(dist)) and (dist < threshold):
        return False
    return True
def estimate_dist():
    directions = ['right','left']
    dist_dict={}
    for direction in directions:
        servo.change_pos(pos=direction)
        dist=distance.get_distance()
        if not math.isnan(dist):
            dist_dict[direction] = distance.get_distance()

    ##back to neutral
    servo.change_pos(pos='neutral')

    return dist_dict


def self_drive_wkeyb():
    motor1a = 7
    motor1b = 11
    motor1e = 22

    motor2a = 13
    motor2b = 16
    motor2e = 15

    def setup_gpio():
        GPIO.setwarnings(False)

        #  set GPIO numbering mode and define output pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(motor1a, GPIO.OUT)
        GPIO.setup(motor1b, GPIO.OUT)
        GPIO.setup(motor1e, GPIO.OUT)
        GPIO.setup(motor2a, GPIO.OUT)
        GPIO.setup(motor2b, GPIO.OUT)
        GPIO.setup(motor2e, GPIO.OUT)

    def backward():
        setup_gpio()
        GPIO.output(motor1a, GPIO.HIGH)
        GPIO.output(motor1b, GPIO.LOW)
        GPIO.output(motor1e, GPIO.HIGH)
        GPIO.output(motor2a, GPIO.HIGH)
        GPIO.output(motor2b, GPIO.LOW)
        GPIO.output(motor2e, GPIO.HIGH)

    def forward():
        setup_gpio()
        GPIO.output(motor1a, GPIO.LOW)
        GPIO.output(motor1b, GPIO.HIGH)
        GPIO.output(motor1e, GPIO.HIGH)
        GPIO.output(motor2a, GPIO.LOW)
        GPIO.output(motor2b, GPIO.HIGH)
        GPIO.output(motor2e, GPIO.HIGH)

    def turnl(interval=0.5):
        '''
        turn left
        '''
        setup_gpio()

        now=time.time()
        while time.time() < now + interval:
            GPIO.output(motor1a, GPIO.HIGH)
            GPIO.output(motor1b, GPIO.LOW)
            GPIO.output(motor1e, GPIO.HIGH)
            GPIO.output(motor2a, GPIO.LOW)
            GPIO.output(motor2b, GPIO.HIGH)
            GPIO.output(motor2e, GPIO.HIGH)
        stop()

    def turnr(interval=0.5):

        setup_gpio()
        now = time.time()
        while time.time() < now + interval:
            GPIO.output(motor1a, GPIO.LOW)
            GPIO.output(motor1b, GPIO.HIGH)
            GPIO.output(motor1e, GPIO.HIGH)
            GPIO.output(motor2a, GPIO.HIGH)
            GPIO.output(motor2b, GPIO.LOW)
            GPIO.output(motor2e, GPIO.HIGH)
        stop()

    def stop():
        setup_gpio()
        GPIO.output(motor1a, GPIO.LOW)
        GPIO.output(motor1b, GPIO.LOW)
        GPIO.output(motor1e, GPIO.LOW)
        GPIO.output(motor2a, GPIO.LOW)
        GPIO.output(motor2b, GPIO.LOW)
        GPIO.output(motor2e, GPIO.LOW)
    #Always starts with the default position (straight direction or 90 deg)
    servo.change_pos(pos='neutral')
    # Get the curses window, turn off echoing of keyboard to screen, turn on
    # instant (no waiting) key response, and use special values for cursor keys
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.halfdelay(3)
    screen.keypad(True)
    try:
        while True:
            char = screen.getch()

            # print(char)
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                #print( "no_obstacle",no_obstacle())
                while no_obstacle():
                  forward()
                dist_dict = estimate_dist()

                next_direction = max(dist_dict,key=dist_dict.get)
                if next_direction == "right":
                    turnr()
                elif next_direction == "left":
                    turnl()
                else:
                    backward()
            
            elif char == curses.KEY_DOWN:
                backward()
            elif char == curses.KEY_RIGHT:
                turnr()
            elif char == curses.KEY_LEFT:
                turnl()
            elif char == 10:
                stop()


    finally:
        # Close down curses properly, inc turn echo back on!
        curses.nocbreak();
        screen.keypad(0);
        curses.echo()
        curses.endwin()
        GPIO.cleanup()

if __name__ == "__main__":
    self_drive_wkeyb()
