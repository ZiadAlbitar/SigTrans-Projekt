import wcslib as wcs
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

dt = 1/22050
Tb = 0.04
bit_seq = np.random.randint(2, size=10)
print(bit_seq)
xb = wcs.encode_baseband_signal(bit_seq, Tb)
t = np.arange(0, xb.shape[0])*dt

wc = 3800*2 * np.pi
xc = np.sin(wc * t) * np.sqrt(2)

xm = xc * xb

yd = xc * np.sin(wc * t) * xb

alpha = 400 * np.pi
num = np.array([alpha**2])
den = np.array([1, 2 * alpha, alpha**2]) 
H = signal.TransferFunction(num, den)

w, mag, phase = H.bode()
# fig, ax4 = plt.subplots(2 , 1)
# ax4[0].semilogx(w, mag)
# # ax4[0].plot(w, mag)
# ax4[1].semilogx(w, phase)

T, yb, xout = signal.lsim(H, yd, t)

recovered_bits = wcs.decode_baseband_signal(yd, Tb)
print(recovered_bits)
 

plt.grid()
# plt.plot(t , xc, label="xc")
# plt.plot(t , yb, label="yb")
plt.plot(t , yb, label="xb")
plt.legend()
plt.show()





