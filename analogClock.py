"""Analog Clock, by Al Sweigart al@inventwith.com
An analog clock animation. Press Ctrl-C to stop.
"""
__version__ =0
import time, math, sys


try:
    import bext
except ImportError:
    print('This program requires the best module, which you\n'
          'can install by following the instructions at\n'
          'https://pypi.org/project/Bext/')
    sys.exit()

# Set up the constants
HOUR_HAND_CHAR = '@'
MINUTE_HAND_CHAR = '*'
SECOND_HAND_CHAR = '.'
HOUR_HAND_LENGTH = 4
MINUTE_HAND_LENGTH = 6
SECOND_HAND_LENGTH = 8
CENTERX, CENTERY = 10,10
COMPLETE_ARC = 2 * math.pi
OFFSET_90_DEGREES = -0.5 * math.pi

CLOCKFACE = """       ##12###
     ##       ##
    11          1
   #             #
  #               #
 10                2
 #                  #
#                   #
#                   #
#                   #
9                   3
#                   #
#                   #
#                   #
 8                 4
 #                 #
  #               #
   #             #
    7           5
     ##       ##
       ###6###"""


def main():
    bext.clear()
    # Draw the circle of the clock:
    for y, row in enumerate(CLOCKFACE.splitlines()):
        for x, char in enumerate(row):
            if char != ' ':
                bext.goto(x,y)
                print(char)
    
    while True: # Main program loop.
        # Get the current time from the computers clock:
        currentTime = time.localtime()
        h = currentTime.tm_hour % 12 # Use 12-hour clock, not 24
        m = currentTime.tm_min
        s = currentTime.tm_sec

        # Drwa the second hand:
        secHandDirection = COMPLETE_ARC * (s/60) + OFFSET_90_DEGREES
        secHandXPos = math.cos(secHandDirection)
        secHandYPos = math.sin(secHandDirection)
        secHandX = int(secHandXPos * SECOND_HAND_LENGTH + CENTERX)


