import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import correlate


def loadSoundFile(filename):
    rate,soundfile = read(filename + ".wav")
    soundfile = np.array(soundfile,dtype = "float")
    soundfile = soundfile[:,0]

    return rate,soundfile


def crossCorr(x,y):
    z = correlate(x,y)
    return z

def findCorr(x,y):
    sr1,loop = loadSoundFile(x)
    sr2,snare = loadSoundFile(y)
    result = crossCorr(loop,snare)

    plt.title("Signal Correlation")
    plt.xlabel("Samples")
    plt.ylabel("Correlation")
    plt.plot(result)
    plt.savefig('01-correlation')
    return result

def findSnarePosition(snareFilename,drumloopFilename):
    correlation = findCorr(snareFilename,drumloopFilename)
    onset, _ = scipy.signal.find_peaks(correlation,height = 1e11,distance = 40000)
    print(onset)
    f=open("02-snareLocation.txt","w")
    f.write(str(onset))
    f.close()

findSnarePosition("snare","drum_loop")
