import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sps
from scipy import signal
import csv
from csv import writer

import xlsxwriter




Fs=32000
tstep = 1/ Fs
F= 1000
N=int(100*Fs/F) #10 cycle
Fstep=Fs/N

#window=tk.Tk()
#conn=sqlite3.connect('FF5.db')
#CC=conn.cursor()
#CC2=conn.cursor()
downx = []
downx2=[]

style.use('fivethirtyeight')

fig = plt.figure()
fig2 = plt.figure()
fig3 = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax2 = fig2.add_subplot(1,1,1)
ax3 = fig3.add_subplot(1,1,1)

def decg_peaks(ecg):
    """Step 1: Find the peaks of the derivative of the ECG signal"""
    d_ecg = np.diff(ecg)  # find derivative of ecg signal
    peaks_d_ecg, _ = sps.find_peaks(d_ecg)  # peaks of d_ecg

    # plot step 1
    plt.figure()

    plt.plot(d_ecg)
    plt.plot(d_ecg[peaks_d_ecg], "x")
    plt.xlabel('Sample [s]')
    plt.ylabel('Derivative of activation []')
    plt.title('R-wave peaks step 1: peaks of derivative of ECG')
    plt.show()
    return d_ecg, peaks_d_ecg


def animate(i):
    conn = sqlite3.connect('EMG_SIR.db')
    CC = conn.cursor()
    CC2 = conn.cursor()


    CC.execute("SELECT * FROM CH0")  # <<<<<<<<<< ADDED
    number_of_rows = CC.execute("SELECT * FROM CH0")
    downx=[]
    print((number_of_rows))
    #print(len(CC.fetchall()))
    #for row in CC.fetchmany(4000):
     #   downx.append(row[0])

    t= np.linspace(0,(N-1)*tstep,N)
    f= np.linspace(0,(N-1)*Fstep,N)#    b=len(t)
    b=32000*100
    for row in CC.fetchall():
        downx.append(row[1])
    #newdata=downx[(len(downx) - b):(len(downx) - b)+b]
    newdata= downx[0:len(downx)]
    print(type(newdata))


    samp_freq = 32000  # Sample frequency (Hz)
    notch_freq = 50.0  # Frequency to be removed from signal (Hz)
    quality_factor = 30.0  # Quality factor
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
    freq, h = signal.freqz(b_notch, a_notch, fs=samp_freq)

    ax3.plot(freq, 20 * np.log10(abs(h)))

    # apply notch filter to signal
    y_notched = signal.filtfilt(b_notch, a_notch, newdata)

    print(type(newdata))
    numpy_newdata=np.array(newdata)
    print(type(numpy_newdata))
    FF_newdata=(np.abs(np.fft.fft(numpy_newdata)))/N
   # newdata= downx[1800:2000]
   # for row in CC2.fetchall():
     #   downx2.append(row[0])
    #newdata2 = downx2[(len(downx2) - 200):]
    #newdata=downx[1850:6000]
  #  Wn=0.1
  #  b, a = sps.butter(4, Wn, 'low', analog=False)

   # ecg_filtered = sps.filtfilt(b, a, newdata)

   # for i in range(len(ecg_filtered)):
    #    print(int(ecg_filtered[i]))

#    numpy_ecg = np.array(ecg_filtered)
#    FF_ecg = (np.abs(np.fft.fft(numpy_ecg))) / N

    F_plot=f[0:int(N/2+1)]
    Mag_FF_newdata=FF_newdata[0:int(N/2+1)]

#    Mag_FF_ecg = FF_ecg[0:int(N/2+1)]



   # myFile = open('MEHEDI_REST_HigherFreq_Filtered.csv', 'w')
    #with myFile:
     #   writer = csv.writer(myFile, delimiter='\n')
      #  writer.writerow(newdata)
  #  decg_peaks(newdata)
  #  Noise=newdata-ecg_filtered
  #  RMS=np.sqrt((np.square(Noise))/len(Noise))
 #   MODN=np.abs(Noise)
   # me=np.mean(MODN)
 #   print(me)
 #   M=np.max(Noise)
  #  print(M)
    ax1.clear()
    ax2.clear()
    ax1.cla()
    ax2.cla()
#    ax1.plot(t,newdata,'.-')

    ax1.plot(newdata)
    ax2.plot(y_notched)
   # ax1.plot(newdata2)
    #ax1.plot(ecg_filtered)

   # ax2.plot(F_plot, Mag_FF_newdata)
#    ax2.plot(F_plot, Mag_FF_ecg)
  #  ax1.plot(Noise)
  #  ax1.plot(RMS)
    #ax1.plot(downx)
    downx.clear()
   # downx2.clear()
    CC.close()
    conn.close()

ani = animation.FuncAnimation(fig, animate,interval=500000)
plt.tight_layout()
plt.show()