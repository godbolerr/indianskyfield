from datetime import datetime 
from datetime import timedelta
import datetime
import datetime

from pytz import timezone
import pytz  
from skyfield import almanac
from skyfield import api
from skyfield import eclipselib
from skyfield.api import GREGORIAN_START
from skyfield.api import N, E, wgs84, load
from skyfield.framelib import ecliptic_frame
from skyfield.toposlib import Topos
from skyfield.trigonometry import position_angle_of
from wx.lib.ogl.composit import _objectStartY

import datetime as dt
import numpy as np
import pandas as pd


def convert(seconds):
    hour = int(seconds/3600) 
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return "%d:%02d:%02d" % (hour, minutes, seconds)

test = convert(95640)

print(test,26*3600+34*60+0)