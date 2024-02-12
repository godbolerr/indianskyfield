from skyfield.api import load
from skyfield.api import GREGORIAN_START
ts = load.timescale()
#t = ts.tt(202, 1, 1, 12, 0)
t = ts.now()

print('TT date and time: ', t.tt_strftime())
print('TAI date and time:', t.tai_strftime())
print('UTC date and time:', t.utc_strftime())
print('TDB Julian date: {:.10f}'.format(t.tdb))
print('Julian century: {:.1f}'.format(t.J))

ts.julian_calendar_cutoff = GREGORIAN_START

t = ts.tt_jd(range(2299159, 2299163))
for s in t.tt_strftime():
    print(s)