import numpy as np

from scipy.signal import butter, buttord

def bandpass(fs):
    # Passband
    fp1, fp2 = 3750, 3850   # Hz

    # Stopband (50 Hz transition)
    fs1, fs2 = 3700, 3900   # Hz

    Ap = 0.1
    As = 60

    fN = fs/2

    wp = np.array([fp1/fN, fp2/fN])
    ws = np.array([fs1/fN, fs2/fN])

    order, wn = buttord(wp, ws, Ap, As)
    print(order)

    sos = butter(order, wn, btype='bandpass', output='sos')

    return sos