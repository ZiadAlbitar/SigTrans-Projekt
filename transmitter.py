#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transmitter template for the wireless communication system project in Signals and
transforms

For plain text inputs, run:
$ python3 transmitter.py "Hello World!"

For binary inputs, run:
$ python3 transmitter.py -b 010010000110100100100001

2022-present -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

import argparse
import numpy as np
from scipy import signal
import sounddevice as sd

import wcslib as wcs

# TODO: Add relevant parameters to parameters.py
from parameters import Tb, Ac, dt, fc, Ts, Kc,fs;


def main():
    parser = argparse.ArgumentParser(
        prog='transmitter',
        description='Acoustic wireless communication system -- transmitter.'
    )

    parser.add_argument(
        '-b',
        '--binary',
        help='message is a binary sequence',
        action='store_true'
    )

    parser.add_argument('message', help='message to transmit', nargs='?')
    args = parser.parse_args()

    if args.message is None:
        args.message = 'Hello World!'

    # Set parameters
    data = args.message

    # Convert string to bit sequence or string bit sequence to numeric bit
    # sequence
    if args.binary:
        bs = np.array([bit for bit in map(int, data)])
    else:
        bs = wcs.encode_string(data)
    
    # Transmit signal
    print(f'Sending: {data} (no of bits: {len(bs)}; message duration: {np.round(len(bs)*Tb, 1)} s).')

    # Encode baseband signal
    # TODO: Adjust fs (lab 2 only, leave untouched for lab 1 unless you know what you are doing)
    xb = wcs.encode_baseband_signal(bs, Tb, fs)

    # TODO: Implement transmitter code here
    t = np.arange(0, xb.shape[0])*dt
    wc = fc*2 * np.pi
    xc = np.sin(wc * t) * np.sqrt(2)
    xm = xc * xb

    # Ensure the signal is mono, then play through speakers
    xm_audio = np.stack((xm, np.zeros(xm.shape)), axis=1)
    sd.play(xm_audio, 1/dt, blocking=True)
    return xm_audio


if __name__ == "__main__":
    main()
