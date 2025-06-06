import numpy as np
import scipy
import scipy.signal



def lms(u, d, N, mu = 0.002, returnCoeffs = False):
    input_signal = u
    desired_signal = d
    tap_number = N
    valid_interation = len(u) - N + 1

    y = np.zeros(valid_interation)     #output signal
    e = np.zeros(valid_interation)     #error signal

    w = np.zeros(N)

    if returnCoeffs:
        W = np.zeros((valid_interation, N))
    
    for n in range(valid_interation):
        x = np.flipud(u[n:n+N])
        y[n] = np.dot(x,w)
        e[n] = d[n+N-1] -  y[n]

        w = w + mu * x * e[n]
        y[n] = np.dot(x,w)
        if returnCoeffs:
            W[n] = w
    
    if returnCoeffs:
        w = W

    return y,e,w 

_, desired_signal = scipy.io.wavfile.read('raw_hello_world.wav')
_, input_signal = scipy.io.wavfile.read('input.wav')

input_signal = input_signal / np.max(np.abs(input_signal))
desired_signal = desired_signal / np.max(np.abs(desired_signal))

ouput_signal, error_signal, filter_coeff = lms(input_signal, desired_signal, 256, returnCoeffs=False)

scipy.io.wavfile.write('output_signal.wav', 44100, ouput_signal)
