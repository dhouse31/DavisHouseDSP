import numpy as np
import scipy
import matplotlib.pyplot as plt

def generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    samples = sampling_rate_Hz*length_secs
    t = np.arange(0,length_secs,1/sampling_rate_Hz)
    x = amplitude*np.sin(2*np.pi*frequency_Hz*t + phase_radians)
    return t,x

def generateSquare(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    x = 0
    k=1
    for i in range(0,10):
        t,sine = generateSinusoidal(amplitude, sampling_rate_Hz, k*frequency_Hz, length_secs, phase_radians)
        sine = sine * 1/k
        k = k+2
        x = x + sine
    x = x * 4/np.pi
    return t,x

def computeSpectrum(x,sample_rate_Hz,window_type):
    numbins = len(x)/2
    binwidth = (sample_rate_Hz/2)/numbins
    if window_type == "rect":
        fft = np.fft.fft(x)
        fft = fft[:round(len(x)/2)]
        f = np.linspace(0,sample_rate_Hz/2,len(fft))
        XAbs = np.abs(fft)
        XPhase = np.angle(fft)
        XRe = fft.real
        XIm = fft.imag
    elif window_type == "hann":
        fft = np.fft.fft(x)
        fft = fft[:round(len(x)/2)]
        f = np.linspace(0,sample_rate_Hz/2,len(fft))
        window = np.hanning(len(fft))
        fft = fft * window
        XAbs = np.abs(fft) * window
        XPhase = np.angle(fft) * window
        XRe = fft.real * window
        XIm = fft.imag * window
    return f,XAbs,XPhase,XRe,XIm



def main():
    tsine,sine = generateSinusoidal(1,44100,400,.5,np.pi/2)
    ind = int(44100*0.005)
    plt.plot(tsine[0:ind],sine[0:ind])
    plt.title("Generated Sinusoid")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.savefig('01-sinusoid')
    plt.close()

    tsquare,square = generateSquare(1,44100,400,.5,0)
    plt.plot(tsquare[0:ind],square[0:ind])
    plt.title("Square Wave Approximation")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.savefig('02-square')
    plt.close()

    fsquare,XAbsquare,XPhasesquare,XResquare,XImsquare = computeSpectrum(square,44100,"rect")
    fsine,XAbsine,XPhasesine,XResine,XImsine = computeSpectrum(sine,44100,"rect")
    plt.figure()
    plt.subplot(2,1,1)
    plt.title("Sine Wave Fourier Transform")
    plt.plot(fsine,XAbsine)
    plt.xlabel("Frequency (Hertz)")
    plt.ylabel("Magnitude")
    plt.subplot(2,1,2)
    plt.plot(fsine,XPhasesine)
    plt.xlabel("Frequency (Hertz)")
    plt.ylabel("Phase (Radians)")
    plt.savefig("03-sinefft")
    plt.close()

    plt.figure()
    plt.subplot(2,1,1)
    plt.title("Square Wave Fourier Transform")
    plt.plot(fsquare,XAbsquare)
    plt.xlabel("Frequency (Hertz)")
    plt.ylabel("Magnitude")
    plt.subplot(2,1,2)
    plt.plot(fsquare,XPhasesquare)
    plt.xlabel("Frequency (Hertz)")
    plt.ylabel("Phase (Radians)")
    plt.savefig("04-squarefft")
    plt.close()

    frect,XAbsrect,XPhaserect,XRerect,XImrect = computeSpectrum(square,44100,"rect")
    fhann,XAbshann,XPhasehann,XRehann,XImhann = computeSpectrum(square,44100,"hann")
    plt.figure()
    plt.subplot(2,1,1)
    plt.title("Square Wave Rect vs. Hann")
    plt.plot(frect,XAbsrect)
    plt.xlabel("Frequency (Hertz)")
    plt.ylabel("Magnitude")
    plt.subplot(2,1,2)
    plt.plot(fhann,XAbshann)
    plt.xlabel("Frequency (Hertz)")
    plt.ylabel("Magnitude")
    plt.savefig("05-rectvhann")
    plt.show()
    plt.close()
    return

main()
