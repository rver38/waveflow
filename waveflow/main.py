import numpy as np, pyaudio as p,time
from collections.abc import Sequence

rate = 44100

pa = p.PyAudio()
outstream = pa.open(rate=rate,channels=1,output=True,format=p.paFloat32)




class tls:
    def amp(self,amp):
        return (lambda tn:np.full(rate*tn.dr,amp))
    def freq(self,freq):
        return (lambda tn:np.full(rate*tn.dr,freq))
    
    def amp_fade(self,start,end):
        return (lambda tn:np.linspace(start,end,rate*tn.dr))
    def freq_fade(self,start,end):
        return (lambda tn:np.linspace(start,end,rate*tn.dr))
    
    def create(self,tn):
        t = np.linspace(0, tn.dr, int(rate * tn.dr))
        freq = tn.fq
        
        match tn.wave:
            case'sine':
                note = tn.amp * np.sin(2 * np.pi * freq * t)
            case 'square':
                note = tn.amp * np.sign(np.sin(2 * np.pi * freq * t))
            case 'sawtooth':
                note = tn.amp * (2 * (freq * t - np.floor(0.5 + freq * t)))
            case 'triangle':
                note = tn.amp * np.abs((4 * freq * t - 1 + np.floor(2 * freq * t)) % 4 - 2) - 1
            case _:
                raise ValueError("Unknown wave type")
        result = np.tile(note,tn.repeat)
        return result.astype(np.float32)
    
    def play(self,x):
        if isinstance(x, Sequence):
            for i in x:
                self.play(i)
        elif isinstance(x, Tone):
            x = self.create(x)
        elif not isinstance(x,np.ndarray):
            return TypeError(f"play() value is not of sequential, waveflow.Tone or numpy.ndarray type ({type(x)}) ")
        try:
            outstream.write(x.tobytes(),len(x))
            time.sleep(0.02)
        except:
            ...
        
wvtools = tls()

class Tone:
    def __init__(self,fq,dr,amp=wvtools.amp(0.5),wave="sine",repeat=1):
        self.dr = dr
        self.fq = fq(self)
        self.amp = amp(self)
        self.wave = wave
        self.repeat = repeat
    def create(self):
        return wvtools.create(self)