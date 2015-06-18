import wave, struct, csv
from collections import deque
from math import log

class CyclicBuffer(deque):
	def __init__(self, size=0):
		super(CyclicBuffer, self).__init__(maxlen=size)
	@property
	def mean(self):
		return sum(self)/len(self)

ifile = open('SD_1_A1.csv', 'rU')
reader = csv.reader(ifile)

min = 1000000.0
max = 0.0

for row in reader:
	if log(float(row[1])) > max:
		max = log(float(row[1]))

scale = 32765 * 2 / max

print scale


song = wave.open('song_exp.wav', 'w')
song.setparams((2, 2, 882, 0, 'NONE', 'not compressed'))

cb = CyclicBuffer(size=3)

ifile.seek(0)

for row in reader:
	value = (log(float(row[1])) * scale) - 32767
	cb.append(value)

	value_cb = value * cb.mean
	value_cb = sorted([-32767, value_cb, 32767])[1]

	value_cb = 0
	if cb.mean > 0:
		value_cb = value

	value /= 4

	packed_value = struct.pack('h', int(value))
	packed_value_cb = struct.pack('h', int(value_cb))
	song.writeframes(packed_value)
	song.writeframes(packed_value_cb)

song.close()
