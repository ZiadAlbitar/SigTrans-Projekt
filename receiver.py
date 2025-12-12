#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receiver template for the wireless communication system project in Signals and
transforms

2022-present -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

import argparse
import numpy as np
from scipy import signal
import sounddevice as sd

import wcslib as wcs

# TODO: Add relevant parameters to parameters.py
from parameters import Tb, dt, wc, fc, fs, Ts, Kc, xc;
from scipy.signal import butter, buttord, sosfilt

def bandpass(fs):
    # Passband
    fp1, fp2 = 3750, 3850   # Hz
    
    # Stopband (50 Hz transition)
    fs1, fs2 = 3720, 3880   # Hz
    
    Ap = 1      
    As = 60     

    fN = fs/2

    wp = np.array([fp1/fN, fp2/fN])
    ws = np.array([fs1/fN, fs2/fN])

    order, wn = buttord(wp, ws, Ap, As)
    print(order)

    sos = butter(order, wn, btype='bandpass', output='sos')

    return sos



def main():
    parser = argparse.ArgumentParser(
        prog='receiver',
        description='Acoustic wireless communication system -- receiver.'
    )
    parser.add_argument(
        '-d',
        '--duration',
        help='receiver recording duration',
        type=float,
        default=10
    )
    args = parser.parse_args()

    # Set parameters
    T = args.duration

    # Receive signal
    print(f'Receiving for {T} s.')
    yr = sd.rec(int(T/dt), samplerate=1/dt, channels=1, blocking=True)
    yr = yr[:, 0]           # Remove second channel


    #BAND PASS FITLER HERE!!!!!!!!!!!!!!!
    t = np.arange(len(yr)) * dt
    xc = np.sin(wc * t) * np.sqrt(2)

    yr = sosfilt(bandpass(fs),yr)

    # TODO: Implement demodulation, etc. here
    # ...
    # xc = A_c*sin(w_c*t)

    yb = yr * xc
    # Baseband signal
    # yb = ...

    #LOW PASS FILTER HERE!!!!!!!!!!!!!!
    w = 3800 / (fs / 2)
    b, a = signal.butter(5, w, 'low')
    output = signal.filtfilt(b, a, yb)
    

    # Symbol decoding
    # TODO: Adjust fs (lab 2 only, leave untouched for lab 1 unless you know what you are doing)
    br = wcs.decode_baseband_signal(output, Tb, 1/dt)
    data_rx = wcs.decode_string(br)
    print(f'Received: {data_rx} (no of bits: {len(br)}).')


if __name__ == "__main__":    
    main()
