import ast

class wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, config):

        # LED strip configuration:
        language=config.get('stencil_parameter', 'language')
        stencil_content  = ast.literal_eval(config.get('language_options', language))
        self.WCA_HEIGHT  = len(stencil_content)
        self.WCA_WIDTH   = len(stencil_content[0].decode('utf-8'))
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT+4 # Number of LED pixels.
        self.LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
        self.LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)
        print('Wiring configuration')
        print('  WCA_WIDTH: ' + str(self.WCA_WIDTH))
        print('  WCA_HEIGHT: ' + str(self.WCA_HEIGHT))
        print('  Num of LEDs: ' + str(self.LED_COUNT))

        wiring_layout = config.get('wordclock_display', 'wiring_layout')
        if wiring_layout == 'bernds_wiring':
            self.wcl = bernds_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'christians_wiring':
            self.wcl = christians_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'timos_wiring':
            self.wcl = timos_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'mini_wiring':
            self.LED_COUNT   = self.WCA_HEIGHT*(self.WCA_WIDTH+1)+3
            self.wcl = mini_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        elif wiring_layout == 'marks_wiring':
            self.LED_COUNT   = 100
            self.wcl = marks_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        else:
            print('Warning: No valid wiring layout found. Falling back to default!')
            self.wcl = bernds_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)

    def setColorBy1DCoordinates(self, strip, ledCoordinates, color):
        '''
        Linear mapping from top-left to bottom right
        '''
        for i in ledCoordinates:
            self.setColorBy2DCoordinates(strip, i%self.WCA_WIDTH, i/self.WCA_WIDTH, color)

    def setColorBy2DCoordinates(self, strip, x, y, color):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        strip.set_pixel(self.wcl.getStripIndexFrom2D(x,y), color)
    def getStripIndexFrom2D(self, x,y):
        return self.wcl.getStripIndexFrom2D(x,y)

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        '''
        return self.wcl.mapMinutes(min)

class marks_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH   = WCA_WIDTH
        self.WCA_HEIGHT  = WCA_HEIGHT
        self.LED_COUNT   = 100
        # 71 is dead...replaced by 99
        self.MAP         = \
              [[ 9,  8,  7, 71,  6,  5,  4,  3,  2,  1,  0], \
               [71, 71, 10, 11, 12, 13, 14, 15, 71, 71, 71], \
               [23, 22, 21, 20, 19, 18, 17, 71, 16, 71, 71], \
               [71, 24, 25, 26, 71, 27, 71, 28, 29, 71, 71], \
               [39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 71], \
               [40, 41, 42, 43, 44, 45, 71, 46, 47, 71, 71], \
               [58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48], \
               [59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69], \
               [71, 77, 76, 75, 74, 73, 72, 99, 70, 71, 71], \
               [78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88], \
               [71, 71, 71, 94, 93, 92, 91, 90, 89, 71, 71]]

    def getStripIndexFrom2D(self, x, y):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        return self.MAP[y][x]

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        '''
        if min == 1:
            return 95
        elif min == 2:
            return 96
        elif min == 3:
            return 97
        elif min == 4:
            return 98
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0

class bernds_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH   = WCA_WIDTH
        self.WCA_HEIGHT  = WCA_HEIGHT
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT+4

    def getStripIndexFrom2D(self, x, y):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        if x%2 == 0:
            pos = (self.WCA_WIDTH-x-1)*self.WCA_HEIGHT+y+2
        else:
            pos = (self.WCA_WIDTH*self.WCA_HEIGHT)-(self.WCA_HEIGHT*x)-y+1
        return pos

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        '''
        if min == 1:
            return self.LED_COUNT-1
        elif min == 2:
            return 1
        elif min == 3:
            return self.LED_COUNT-2
        elif min == 4:
            return 0
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0

class christians_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH   = WCA_WIDTH
        self.WCA_HEIGHT  = WCA_HEIGHT
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT+4

    def getStripIndexFrom2D(self, x, y):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        if y%2 == 0:
            pos = (self.WCA_HEIGHT-y-1)*self.WCA_WIDTH+x
        else:
            pos = (self.WCA_HEIGHT*self.WCA_WIDTH)-(self.WCA_WIDTH*y)-x-1
        return pos

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as the last four leds of the led-strip
        '''
        if min == 1:
            return self.LED_COUNT-4
        elif min == 2:
            return self.LED_COUNT-3
        elif min == 3:
            return self.LED_COUNT-2
        elif min == 4:
            return self.LED_COUNT-1
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0


class timos_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH   = WCA_WIDTH
        self.WCA_HEIGHT  = WCA_HEIGHT
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT+4

    def getStripIndexFrom2D(self, x, y):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        if x%2 == 0:   # even columns 0,2,4,6,8,10
            pos = (x)*self.WCA_HEIGHT+y+2     # last +2 for the minute LEDs before the WCA
        else:          # odd columns 1,3,5,7,9
            pos = (self.WCA_HEIGHT)+(self.WCA_HEIGHT*x)-y+1
        return pos

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        '''
        if min == 1:
            return 1
        elif min == 2:
            return self.LED_COUNT-1
        elif min == 3:
            return self.LED_COUNT-2
        elif min == 4:
            return 0
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0

class mini_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    Special setting here: Building a wordclock with minimal efforts.
    '''

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH   = WCA_WIDTH
        self.WCA_HEIGHT  = WCA_HEIGHT+1
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT+4

    def getStripIndexFrom2D(self, x, y):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        if x%2 == 0:
            pos = (self.WCA_WIDTH*self.WCA_HEIGHT)-(self.WCA_HEIGHT*x)-y+2
        else:
            pos = (self.WCA_WIDTH-x-1)*self.WCA_HEIGHT+y+4
        return pos

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as the last four leds of the led-strip
        '''
        if min == 1:
            return 0
        elif min == 2:
            return 1
        elif min == 3:
            return 2
        elif min == 4:
            return 3
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return 0
