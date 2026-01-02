import numpy as np

from scipy.signal import butter, buttord, cheb1ord, cheby1

def bandpass(fs):
    # Passband
    fp1, fp2 = 3750, 3850   # Hz

    # Stopband (50 Hz transition)
    fs1, fs2 = 3700, 3900   # Hz

    Ap = 1
    As = 50

    fN = fs/2

    wp = np.array([fp1/fN, fp2/fN])
    ws = np.array([fs1/fN, fs2/fN])

    #order, wn = buttord(wp, ws, Ap, As)

    order, wn = cheb1ord(wp, ws, Ap, As)
    print(order)

    sos = cheby1(
        order,
        Ap,
        wn,
        btype='bandpass',
        output='sos'
    )

    #sos = butter(order, wn, btype='bandpass', output='sos')

    return sos