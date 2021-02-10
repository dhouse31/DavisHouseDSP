import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import time

def loadSoundFile(filename):
    rate,soundfile = read(filename)
    soundfile = np.array(soundfile,dtype = "float")
    return soundfile

def myTimeConv(x,h):

    if len(h)%2 == 0:
         h = np.append(h,0)
    N1 = len(x)
    N2 = len(h)
    N = N1+N2-1    #length of conv sig is s1+s2 -1
    y = np.zeros(N)
    halfk = int(N2/2)
    x =np.pad(x,((halfk,halfk)),'constant')
    h = np.flip(h)
    iter = 0
    for i in range(halfk):
        y[iter] = np.dot(h[:i+1], x[halfk+i:halfk-1:-1])
        iter += 1
    for n in range (halfk, N1 + halfk):
        y[n] = np.dot(h, x[n-halfk:n+halfk+1])
        iter += 1
    #for i in range(halfk):
        #y[N - halfk] = np.dot(h[halfk+1:halfk+i+2], x[N1+halfk-1:N1+halfk-i-2:-1])
        #iter += 1
    return y

def CompareConv(x,h):
    start_time = time.time()
    myconv = myTimeConv(x,h)
    end_time = time.time()
    totaltime1 = end_time-start_time

    start_time = time.time()
    theirconv = scipy.convolve(x,h)
    end_time = time.time()
    totaltime2 = end_time-start_time

    diff = theirconv - myconv[0:-1]
    m = np.mean(myconv) - np.mean(theirconv)
    mabs = np.mean(np.absolute(diff - np.mean(diff)))
    stdev = np.std(diff)
    times = [totaltime1,totaltime2]

    return m,mabs,stdev,times




#set up for sample convolution signals
x = np.zeros(200)
for n in range(len(x)):
    x[n] = 1
h1 = np.linspace(0,1,26)
h2 = np.linspace(1,0,26)
h2 = h2[1:]
h = np.concatenate((h1,h2), axis=0)
y = myTimeConv(x,h)

h = loadSoundFile("impulse-response.wav")
x = loadSoundFile("piano.wav")

m,mabs,stdev,times = CompareConv(x,h)
f=open("02-compareconv.txt","w")
f.write(str([m,mabs,stdev,times]))
f.close()
plt.plot(y)
plt.title("x*h Convolution")
plt.xlabel("Time")
plt.ylabel("Response")
plt.savefig('01-convolution')
