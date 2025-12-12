import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

import wcslib as wcs

# %matplotlib ipympl
pi = np.pi

channel_id = 14   # Your channel ID
Tb = 0.04  # Symbol width in seconds

fc = 3800
wc = 3800*2*pi*4 

lowcut = 3750
highcut = 3850

Kc = 4
Tc = 1/fc
Ts = Tc / Kc 
dt = Ts
fs = 1/Ts

Ac = np.sqrt(2)

bit_seq = np.random.randint(2, size=10)
xb = wcs.encode_baseband_signal(bit_seq, Tb)
t = np.arange(0, xb.shape[0])*dt

xc = np.sin(wc * t) * np.sqrt(2)
xm = xc * xb