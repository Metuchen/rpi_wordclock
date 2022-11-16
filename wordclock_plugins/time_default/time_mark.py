''' Provided by Alexandre'''
from itertools import chain

import datetime as dt

class time_mark():
    '''
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on an english WCA
    '''

    def __init__(self):
        self.prefix = list(range(0,3)) # -> IT'S
        self.minutes=[[], \
            # -> FIVE PAST
            list(chain(range(25,29),range(44,48))), \
            # -> TEN PAST
            list(chain(range(34,37),range(44,48))), \
            # -> QUARTER PAST
            list(chain(range( 4,11),range(44,48))), \
            # -> TWENTY PAST
            list(chain(range(13,19),range(44,48))), \
            # -> TWENTYFIVE PAST
            list(chain(range(13,19),range(25,29),range(44,48))), \
            # -> HALF PAST
            list(chain(range(22,26),range(44,48))), \
            # -> TWENTYFIVE TO
            list(chain(range(13,19),range(25,29),range(47,49))), \
            # -> TWENTY TO
            list(chain(range(13,19),range(47,49))), \
            # -> QUARTER TO
            list(chain(range( 4,11),range(47,49))), \
            # -> TEN TO
            list(chain(range(34,37),range(47,49))), \
            # -> FIVE TO
            list(chain(range(25,29),range(47,49)))]
            # -> TWELVE
        self.hours= [ list(range(99,105)), \
            # -> ONE
            list(range(79,82)), \
            # -> TWO
            list(range(77,80)), \
            # -> THREE
            list(range(55,60)), \
            # -> FOUR
            list(range(66,70)), \
            # -> FIVE
            list(range(70,74)), \
            # -> SIX
            list(range(74,77)), \
            # -> SEVEN
            list(range(89,94)), \
            # -> EIGHT
            list(range(81,86)), \
            # -> NINE
            list(range(93,97)), \
            # -> TEN
            list(range(85,88)), \
            # -> ELEVEN
            list(range(104,110)), \
            # -> TWELVE ... again
            list(range(99,105))]
        # -> OCLOCK
        self.full_hour= list(range(113,119))

    def get_time(self, time, withPrefix=True):
        # Assemble indices
        if time.hour%12 == 0 and time.minute == 20:
                    # IVORY         # LOVE              # MARK
            return  list(range(49,54)) + [ 40, 51, 62, 73 ] + [ 30, 41, 52, 63 ]
        else:
            hour=time.hour%12+(1 if time.minute/5 >= 7 else 0)
            minute=int(time.minute/5)
            return  \
                (self.prefix if withPrefix else []) + \
                self.minutes[minute] + \
                self.hours[hour] + \
                (self.full_hour if (minute == 0) else [])
