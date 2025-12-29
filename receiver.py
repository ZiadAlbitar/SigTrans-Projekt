#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receiver template for the wireless communication system project in Signals and
transforms

2022-present -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import sounddevice as sd

import wcslib as wcs

# TODO: Add relevant parameters to parameters.py
from parameters import Tb, dt, wc, fc, fs, Ts, Kc, xc, Ac;
from bandpass import bandpass
from scipy.signal import sosfilt


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

    #yb = yr * xc

    # I = Arxb(t-tr)sin(2wct)
    # Q = Arxb(t-tr)cos(2wct)
    # Baseband signal
    # yb = ...

    I = 2*yr * np.sin(wc*t)
    Q = 2*yr * np.cos(wc*t)

    #LOW PASS FILTER HERE!!!!!!!!!!!!!!
    # filter out high frequencies so that only 1s or 0s are seen
    w = 3800 / (fs / 2)  #~3800/7575.8 ~ 0.5

    fc_lp = 2 / Tb
    Wn = fc_lp / (fs / 2)

    b, a = signal.butter(5, w , 'lowpass')
    output_I = signal.lfilter(b, a, I)
    output_Q = signal.lfilter(b, a, Q)

    phase = np.arctan2(output_I, output_Q)
    output = np.sqrt(output_I**2 + output_Q**2)

    # Symbol decoding
    # TODO: Adjust fs (lab 2 only, leave untouched for lab 1 unless you know what you are doing)
    br = wcs.decode_baseband_signal(output, Tb, 1/dt)
    data_rx = wcs.decode_string(br)
    print(f'Received: {data_rx} (no of bits: {len(br)}).')
    plt.figure()
    plt.plot(I, label='I')
    plt.plot(Q, label='Q')
    plt.plot(output_I, label='out_I')
    plt.plot(output_Q, label='out_Q')
    plt.plot(output, label='Envelope')
    plt.legend()
    plt.show()

if __name__ == "__main__":    
    main()
