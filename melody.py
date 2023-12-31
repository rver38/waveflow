from waveflow.main import Tone,wvtools
import matplotlib.pyplot as plt

a = Tone(wvtools.freq_fade(40,0),1,wvtools.amp(1))
print(a.fq[0])
plt.plot(a.create())
plt.show()
wvtools.play(a)
