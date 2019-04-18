import machine
#import math
from math import sqrt
import neopixel
import time
from random import randint, choice
import sys

BLACK =     [  0,   0,   0]      # black
WHITE =     [255, 255, 255]
RED =       [255,   0,   0]      # red
LIME =      [  0, 255,   0]      # green
BLUE =      [  0,   0, 255]      # blue
YELLOW =    [255, 255,   0]      # yellow
AQUA =      [  0, 255, 255]
MAGENTA =   [255,   0, 255]
SILVER =    [192, 192, 192]
GRAY =      [128, 128, 128]
MAROON =    [128,   0,   0]
OLIVE =     [128, 128,   0]
GREEN =     [  0, 128,   0]
PURPLE =    [128,   0, 128]
TEAL =      [  0, 128, 128]
NAVY =      [  0,   0, 128]

NICE_PINK = [  6,   0,   3]


#ColourNames = [ 'BLACK',    'WHITE',    'RED',      'LIME',
ColourNames = [ 'WHITE',    'RED',      'LIME',
                'BLUE',     'YELLOW',   'AQUA',     'MAGENTA',
                'SILVER',   'GRAY',     'MAROON',   'OLIVE',
                'GREEN',    'PURPLE',   'TEAL',     'NAVY']

Colours = { 'BLACK' : BLACK,    'WHITE' : WHITE,    'RED' : RED,        'LIME' : LIME,
            'BLUE' : BLUE,      'YELLOW' : YELLOW,  'AQUA' : AQUA,      'MAGENTA' : MAGENTA,
            'SILVER' : SILVER,  'GRAY' : GRAY,      'MAROON' : MAROON,  'OLIVE' : OLIVE,
            'GREEN' : GREEN,    'PURPLE' : PURPLE,  'TEAL' : TEAL,      'NAVY' : NAVY   }

RING_PIXELS = 16
STRIP_PIXELS = 240
PIXELS = STRIP_PIXELS
#PIXELS = RING_PIXELS

np = neopixel.NeoPixel(machine.Pin(13), PIXELS)

default_limit = 15


"""
HELPER FUNCTIONS
"""
def OddEven(x):
    even = randint(0,x)
    odd = even
    while odd == even:
        odd = randint(0,x)
    return odd,even



class LIGHTS:
    def __init__(self, np, timeout = 15):
        """
        Class with default attributes and methods
        for NeoPixel Strip light animations
        """
        self.colours_BG_alt = [ 
                (5, 0, 0), (0, 5, 0), (0, 0, 5), 
                (2, 2, 0), (2, 0, 2), (0, 2, 2)
        ]
        self.bg_R = [ [1,0,0], [2,0,0], [1,0,0], [1,0,0] ]    # RED
        self.bg_G = [ [0,1,0], [0,2,0], [0,1,0], [0,1,0] ]    # GREEN
        self.bg_B = [ [0,0,1], [0,0,2], [0,0,1], [0,0,1] ]    # BLUE

        self.time_start = 0
        self.duration = 0
        self.np = np


    def TurnOffLights(self):
        for x in range(self.np.n):
            self.np[x] = (0, 0, 0)  # Turn off NeoPixel
        self.np.write()

    def ColourWheel(self, angle):
        """
        RGB colourspace if plotted produces a cube.  Unlike
        HSV which is cylindrical, RGB provides no simple solution
        for seamlessly cycle through colours.  This function useses the 
        number range of 0 to 255 as a 'virtual' cyclindrical co-ordinates
        to map the corresponding RGB tuple.
                
          0 <  85 = Red
         85 < 170 = Green 
        170 < 256 = Blue
        
        then wraps around to 0 (Red)

        """
        if angle < 85:
            return( int(angle * 3),				# red
                    int(255 - (angle * 3)),		# green
                    0)							# blue
        elif angle < 170:
            angle -= 85
            return( int(255 - (angle * 3)),		# red
                    0,							# green
                    int(angle * 3))				# blue
        else:
            angle -= 170
            return( 0,							# red
                    int(angle * 3),				# green
                    int(255 - angle * 3))    	# blue


    def pattern_RainbowTrain(self, timeout=60):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        offset = 0
        idx = 0
        atten = 10
        print("Function: pattern_RainbowTrain")
        try:
            while self.duration < self.timeout:
                idx = offset
                for i in range(0, self.np.n, 4):
                    # tuple([z*2 for z in rgb])
                    self.np[i] = tuple([int(z/atten) for z in self.ColourWheel(idx)])
                    self.np[i+1] = tuple([int(z/atten) for z in self.ColourWheel(idx)])
                    self.np[i+2] = tuple([int(z/atten) for z in self.ColourWheel(idx)])
                    self.np[i+3] = tuple([int(z/atten) for z in self.ColourWheel(idx)])
                    idx += 2
                    if idx > 255:
                        idx = 0
                self.np.write()
                offset += 2
                if offset > 255:
                    offset = 0
                #time.sleep(0.1)
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n") 
        finally:
            self.TurnOffLights()


    def pattern_SolidColour(self, timeout=120):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_SolidColour")
        try:
            while self.duration < self.timeout:
                for name in ColourNames:
                    rgb = Colours[name]
                    colour = [int(rgb[0]/10), int(rgb[1]/10), int(rgb[2]/10)]
                    for x in range(PIXELS):
                        self.np[x] = colour
                    self.np.write()
                    print("R:%03d G:%03d B:%03d  Colour = %8s" % (Colours[name][0], Colours[name][1], Colours[name][2], name), end='')
                    time.sleep(3)
                    time_new = time.time()
                    self.duration = time_new-self.time_start
                    print("    timeout in %03d secs\r" % (timeout - self.duration), end='')
            print("\n") 
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    def pattern_SolidColourSlide(self, timeout=120):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_SolidColourSlide")
        atten = 20
        try:
            while self.duration < self.timeout:
                for name in ColourNames:
                    rgb = Colours[name]
                    colour = [int(rgb[0]/atten), int(rgb[1]/atten), int(rgb[2]/atten)]
                    for x in range(0,PIXELS,2):
                        self.np[x] = colour
                        self.np[x+1] = colour
                        self.np.write()
                    time_new = time.time()
                    self.duration = time_new-self.time_start
                    print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    def pattern_AlternateColour(self, timeout=180):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: alternateColor")
        delay = 0.2
        timer = 0
        time_old = 0
        time_new = 0
        # get odd/even indexes
        rangeMax = len(self.colours_BG_alt)-1
        odd,even = OddEven(rangeMax)
        try:
            while self.duration < self.timeout:
                for x in range(PIXELS):
                    if x % 2:
                        np[x] = self.colours_BG_alt[even]
                    else:
                        np[x] = self.colours_BG_alt[odd]
                self.np.write()
                time.sleep(delay)
                for x in range(PIXELS):
                    if x % 2:
                        self.np[x] = self.colours_BG_alt[odd]
                    else:
                        self.np[x] = self.colours_BG_alt[even]
                self.np.write()
                time.sleep(delay)  
                time_old = time_new
                time_new = time.time()
                self.duration = time_new - self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
                timer += (time_new - time_old)
                if timer > 15:
                    timer = 0
                    odd,even = OddEven(rangeMax)
            print("\n")
        except KeyboardInterrupt:
            print("\n") 


    def pattern_SideFill(self, timeout=240):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_SideFill")
        pixelMax = 5
        count = 0
        speed = 3
        y = len(ColourNames)-1
        try:
            while self.duration < self.timeout:
                rgb = Colours[ColourNames[randint(1, y)]]
                rgb_dim = [int(rgb[0]/4), int(rgb[1]/4), int(rgb[2]/4)]
                level = PIXELS - count
                for x in range(0,level,3):
                    self.np[x] = rgb_dim
                    self.np[x+1] = rgb_dim
                    self.np[x+2] = rgb_dim
                    if x >= 3:
                        self.np[x-1] = BLACK
                        self.np[x-2] = BLACK
                        self.np[x-3] = BLACK
                    self.np.write()
                count += 3
                if count > PIXELS:
                    count = 0
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")


    def pattern_RandomFill(self, timeout=240):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_RandomFill")
        pixelMax = 20
        used = [0] * self.np.n
        count = 0
        state = 0
        try:
            while self.duration < self.timeout:
                idx = randint(0,(self.np.n-1))
                if state == 0:
                    if count < 185:
                        red = randint(0, pixelMax)
                        green = randint(0, pixelMax)
                        blue = randint(0, int(pixelMax/2))
                        if np[idx] == (0,0,0):
                            np[idx] = (red, green, blue)
                            count += 1
                            np.write()
                            time.sleep(0.05)
                    else:
                        count += 1
                        state = 1
                elif state == 1:
                    if count > 55:
                        while np[idx] == (0,0,0):
                            idx = randint(0,(self.np.n-1))
                        np[idx] = BLACK
                        count -= 1
                        np.write()
                        time.sleep(0.05)
                    else:
                        count -= 1
                        state = 0
                print("count = %3d" % count, end='')
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("    timeout in %03d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")


    def pattern_MiddleFill(self, timeout=60):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_MiddleFill")        
        limit = int(PIXELS/2)
        topStart = limit
        bottomStart = limit-1
        numColours = len(ColourNames)
        time_start = time.time()
        #duration = 0
        atten = 10
        # Colours
        try:
            while self.duration < timeout:
                # tuple([z*2 for z in rgb])
                rgb = Colours[ColourNames[randint(1, (numColours-1))]]
                topColour = [int(z/atten) for z in rgb]
                rgb = Colours[ColourNames[randint(1, (numColours-1))]]
                bottomColour = [int(z/atten) for z in rgb]
                width = randint(100, limit)
                for x in range(0,width):
                    self.np[bottomStart-x] = bottomColour
                    self.np[topStart+x] = topColour
                    self.np.write()
                for x in range(width-1,-1,-1):
                    self.np[bottomStart-x] = BLACK
                    self.np[topStart+x] = BLACK
                    self.np.write()
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    def pattern_MountainCarChase(self, timeout=300):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_MountainCarChase")        
        #               R    G    B    pos  speed         R    G    B    pos  speed
        cars = [    [[  0, 150,   0],    0,    1],    [[150,   0,   0],   30,    1],
                    [[  0,   0, 150],   70,    1],    [[100,   0, 100],  120,    1],
                    [[100, 100,   0],  150,    1],    [[  0, 100, 100],  190,    2],
                    [[ 50,  50,  50],  200,    3],    [[  0,  60, 100],  230,    4],
                    [[ 80,   5, 200],  231,    5],    [[  8, 105,   5],  232,    6]   ]
        num_cars = len(cars)
        bg = [self.bg_R, self.bg_G, self.bg_B]
        bg_len = len(bg)
        bg_count = 0
        bg_idx = randint(0,2)

        # randomize position
        for car in cars:
            car[1] = randint(0,240)

        # randomize speed
        for idx in range(5,10,1):
            cars[idx][2] = randint(2,5)

        # randomize background
        try:
            while self.duration < self.timeout: 
                for x in range(PIXELS):
                    if x % bg_len == 0:
                        self.np[x] = bg[bg_idx][0]
                    elif x % bg_len == 1:
                        self.np[x] = bg[bg_idx][1]
                    elif x % bg_len == 2:
                        self.np[x] = bg[bg_idx][2]
                    else:
                        self.np[x] = bg[bg_idx][3]
                    for idx in range(num_cars):
                        if x == cars[idx][1]:
                            self.np[x] = cars[idx][0]
                # update positions
                for idx in range(num_cars):
                    cars[idx][1] += cars[idx][2]
                    if cars[idx][1] >= PIXELS:
                        cars[idx][1] = 0
                # update background
                bg_count += 1
                if bg_count == (bg_len+1):
                    tmp = bg[bg_idx][3]
                    bg[bg_idx][3] = bg[bg_idx][2]
                    bg[bg_idx][2] = bg[bg_idx][1]
                    bg[bg_idx][1] = bg[bg_idx][0]
                    bg[bg_idx][0] = tmp
                    bg_count = 0
                self.np.write()
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")


    def pattern_BouncyBalls(self, timeout=120, BallCount=3):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_BouncyBalls")
        Gravity = -9.81
        StartHeight = 1
        ImpactVelocityStart = sqrt( -2 * Gravity * StartHeight )
        # allocate arrays
        Offset = [25,60,155]
        Ceiling = [70,70,70]
        Height = []
        ImpactVelocity = []
        TimeSinceLastBounce = []
        Position = []
        PositionOld = []
        ClockTimeSinceLastBounce = []
        Dampening = []
        BallColour = [] 
        for x in range(BallCount):
            Height.append(0)
            ImpactVelocity.append(0)
            TimeSinceLastBounce.append(0)
            Position.append(0)
            PositionOld.append(0)
            ClockTimeSinceLastBounce.append(0)
            Dampening.append(0)
            rgb = Colours[ColourNames[randint(1, (len(ColourNames)-1))]]
            if x > 0:
                if rgb == BallColour[x-1]:
                    rgb = Colours[ColourNames[randint(1, (len(ColourNames)-1))]]
            BallColour.append(rgb)
        for ball in range(BallCount):
            ClockTimeSinceLastBounce[ball] = time.ticks_ms()
            Height[ball] = StartHeight
            Position[ball] = 0
            PositionOld[ball] = 0
            ImpactVelocity[ball] = ImpactVelocityStart
            TimeSinceLastBounce[ball] = 0
            Dampening[ball] = 0.90 - float(ball)/pow(BallCount,2)  
        
        try:
            while self.duration < self.timeout:
                for ball in range(BallCount):
                    TimeSinceLastBounce[ball] =  time.ticks_ms() - ClockTimeSinceLastBounce[ball]
                    Height[ball] = 0.5 * Gravity * pow( TimeSinceLastBounce[ball]/1000 , 2.0 ) + ImpactVelocity[ball] * TimeSinceLastBounce[ball]/1000
                    if Height[ball] < 0:
                        Height[ball] = 0
                        ImpactVelocity[ball] = Dampening[ball] * ImpactVelocity[ball]
                        ClockTimeSinceLastBounce[ball] = time.ticks_ms()
                    if ImpactVelocity[ball] < 0.01:
                        ImpactVelocity[ball] = ImpactVelocityStart
                        rgb = Colours[ColourNames[randint(1, (len(ColourNames)-1))]]
                        #if ball > 0:
                        if rgb == BallColour[ball-1]:
                            rgb = Colours[ColourNames[randint(1, (len(ColourNames)-1))]]
                        BallColour[ball] = rgb
                    PositionOld[ball] = Position[ball]
                    Position[ball] = round( Height[ball] * (Ceiling[ball] - 1) / StartHeight) + Offset[ball]

                for ball in range(BallCount):
                    if PositionOld[ball] != Position[ball]:
                        self.np[PositionOld[ball]] = (0,0,0)
                    self.np[Position[ball]] = BallColour[ball]
                self.np.write()
                #self.TurnOffLights()
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    def pattern_BackwardsSlidingStripes(self, timeout=120):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_BackwardsSlidingStripes")
        rgb = Colours[ColourNames[randint(1, (len(ColourNames)-1))]]
        pallete = [[int(z/1000*i**1.5) for z in rgb] for i in range(15)]
        idx = 0
        offset = 0
        try:
            while self.duration < self.timeout:
                idx = offset
                for x in range(0, self.np.n):
                    self.np[x] = pallete[idx]
                    idx += 1
                    if idx == len(pallete):
                        idx = 0
                self.np.write()
                offset += 1
                if offset == len(pallete):
                    offset = 0
                    rgb = Colours[ColourNames[randint(1, (len(ColourNames)-1))]]
                    pallete = [[int(z/1000*i**1.5) for z in rgb] for i in range(15)]
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    def pattern_FireSparks(self, timeout=120):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_FireSparks")
        loops = 1
        fire = [ (1,0,0), (2,0,0), (3,0,0) ]
        sparks = [  (10,0,0),    # light red
                    (5,5,0),    # faint yellow
                    (5,1,0),    # faint orange
                    (10,2,0),
                    (50,0,0)]
                    #(50,5,5)]   # pinkish white
        sparkFactor = 25
        try:
            while self.duration < self.timeout:
                for loop in range(loops):
                    for led in range(self.np.n):
                        self.np[led] = choice(fire)
                    if loop == 0:
                        for i in range(sparkFactor):
                            self.np[randint(0,self.np.n-1)] = choice(sparks)
                    self.np.write()
                time.sleep(0.02)

                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    def pattern_RandomColourTrain(self, timeout=180):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_RandomColourTrain")
        # create pallete
        #
        myColours = []
        for rgb in list(Colours.values()):
            rgb_atten = [int(z/10) for z in rgb]
            myColours.append(rgb_atten)
        # Pre-fill led strip
        idx = 0
        for px in range(self.np.n):
            self.np[px] = myColours[idx]
            idx += 1
            if idx == len(myColours):
                idx = 0
        self.np.write()
        try:
            while self.duration < self.timeout:
                for px in range((self.np.n-1), 0, -2):
                    self.np[px] = self.np[px-1]
                    self.np[px-1] = self.np[px-2]
                self.np[0] = myColours[idx]
                self.np.write()
                idx += 1
                if idx == len(myColours):
                    idx = 0
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    def pattern_RandomColourStrips(self, timeout=120):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_RandomColourStrips")
        # create pallete
        #
        myColours = []
        lineLength = 5
        for rgb in list(Colours.values()):
            if rgb != [0,0,0]:
                rgb_atten = [int(z/10) for z in rgb]
                myColours.append(rgb_atten)

        try:
            while self.duration < self.timeout:
                for colour in myColours:
                    offset = randint(0, (self.np.n - 1))
                    for px in range(randint(5,9)):
                        if (offset+px) < (self.np.n - 1):
                            self.np[offset+px] = colour
                    self.np.write()
                    #time.sleep(0.2)
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    def pattern_GreenSparks(self, timeout=120):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_GreenSparks")
        palette = [(0,24,0), (0,8,0), (0,4,0)]
        #colour = [int(rgb[0]/atten), int(rgb[1]/atten), int(rgb[2]/atten)]
        try:
            while self.duration < self.timeout:
                for px in range(self.np.n):
                    self.np[px] = palette[randint(0,len(palette)-1)]
                self.np.write()

                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    def pattern_RedWithGreenSparks(self, timeout=120):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_RedWithGreenSparks")
        palette = [(0,24,0), (0,8,0), (0,4,0)]
        #offsets = [25,50,75,100,125,150,175,200]
        offsets = [(x*15) for x in range(16)]
        sparkLen = 7
        # prefill with Dark Red
        for px in range(self.np.n):
            self.np[px] = (5,0,0)
        self.np.write()
        try:
            while self.duration < self.timeout:
                for offset in offsets:
                    for px in range(sparkLen):
                        self.np[offset+px] = palette[randint(0,2)]
                self.np.write()
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    def pattern_SnowSparkles(self, timeout=120):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_SnowSparkles")
        palette = [(5,5,5), (15,15,15), (1,1,15), (1,1,25), (0,25,25)]
        try:
            while self.duration < self.timeout:
                for px in range(self.np.n):
                    self.np[px] = palette[randint(0,len(palette)-1)]
                self.np.write()
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()

    def pattern_PurplePinkSparkles(self, timeout=120):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: pattern_PurplePinkSparkles")
        palette = [(3,0,4), (6,0,3), (10,0,3), (15,1,5), (22,2,9)]
        #offsets = [(x*15) for x in range(16)]
        offsets = [(x*20) for x in range(12)]
        sparkLen = 7
        # prefill with Dark Red
        for px in range(self.np.n):
            self.np[px] = (2,0,2)
        self.np.write()
        try:
            while self.duration < self.timeout:
                for offset in offsets:
                    for px in range(sparkLen):
                        self.np[offset+px] = palette[randint(0,len(palette)-1)]
                self.np.write()
                time.sleep(0.1)
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()


    """
    PATTERN TEMPLATE
    
    def newPattern1(self, timeout=120):
        self.time_start = time.time()
        self.duration = 0
        self.timeout = timeout
        print("Function: newPattern1")

        try:
            while self.duration < self.timeout:
                pass
                time_new = time.time()
                self.duration = time_new-self.time_start
                print("timeout in %3d secs\r" % (timeout - self.duration), end='')
            print("\n")
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.TurnOffLights()
    """


def LightShow(np):
    Lights = LIGHTS(np)
    LightsMenu = [  Lights.pattern_RainbowTrain,
                    Lights.pattern_SolidColour,
                    Lights.pattern_SolidColourSlide, 
                    Lights.pattern_AlternateColour,
                    Lights.pattern_SideFill,
                    Lights.pattern_RandomFill, 
                    Lights.pattern_MiddleFill,
                    Lights.pattern_MountainCarChase,
                    Lights.pattern_BouncyBalls,
                    Lights.pattern_BackwardsSlidingStripes,
                    Lights.pattern_FireSparks,
                    Lights.pattern_RandomColourTrain,
                    Lights.pattern_RandomColourStrips,
                    Lights.pattern_GreenSparks,
                    Lights.pattern_RedWithGreenSparks,
                    Lights.pattern_SnowSparkles,
                    Lights.pattern_PurplePinkSparkles     ]
    try:
        while True:
            for func in LightsMenu:
                Lights.TurnOffLights()                
                func()
    except KeyboardInterrupt:
        print ("\nCtrl-C pressed.  Cleaning up and exiting...")
    finally:
        Lights.TurnOffLights()



LightShow(np)

