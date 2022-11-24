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
#downx2=[]

style.use('fivethirtyeight')

fig = plt.figure()
#fig2 = plt.figure()
#fig3 = plt.figure()
ax1 = fig.add_subplot(1,1,1)
#ax1 = fig.add_subplot(4,1,1)
#ax2 = fig.add_subplot(4,1,2)
#ax3 = fig.add_subplot(4,1,3)
#ax4 = fig.add_subplot(4,1,4)
#ax3 = fig3.add_subplot(1,1,1)

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
    conn = sqlite3.connect('16Khz_100hz_ADCAFE.db')
    CC = conn.cursor()
 #   CC6 = conn.cursor()
 #   CC3 = conn.cursor()
 #   CC5 = conn.cursor()



    CC.execute("SELECT * FROM CH4")  # <<<<<<<<<< ADDED
    number_of_rows = CC.execute("SELECT * FROM CH4")
  #  CC6.execute("SELECT * FROM CH6")  # <<<<<<<<<< ADDED
  #  number_of_rows_6 = CC6.execute("SELECT * FROM CH6")
  #  CC3.execute("SELECT * FROM CH3")  # <<<<<<<<<< ADDED
  #  number_of_rows_3 = CC3.execute("SELECT * FROM CH3")
  #  CC5.execute("SELECT * FROM CH5")  # <<<<<<<<<< ADDED
  #  number_of_rows_5 = CC5.execute("SELECT * FROM CH5")
    downx =[]
  #  downx6 =[]
  #  downx5 = []
  #  downx3 = []
    print((number_of_rows))
    #print(len(CC.fetchall()))
    #for row in CC.fetchmany(4000):
     #   downx.append(row[0])

  #  t= np.linspace(0,(N-1)*tstep,N)
  #  f= np.linspace(0,(N-1)*Fstep,N)#    b=len(t)
  #  b=32000*100
    for row in CC.fetchall():
        downx.append(row[1])
  #  for row in CC6.fetchall():
   #     downx6.append(row[1])
   # for row in CC3.fetchall():
   #     downx3.append(row[1])
   # for row in CC5.fetchall():
   #     downx5.append(row[1])

    print(len(downx))
    #newdata=downx[(len(downx) - b):(len(downx) - b)+b]
  #  newdata= downx[len(downx)-32000+400:len(downx)-32000+450]#sine32k
    #newdata = downx[len(downx)+12204 - 32000:len(downx)-32000+12304]#sine64k
    #newdata = downx[len(downx) - 32000+21050:len(downx)-32000+21050+200]  # sine128k
    #newdata = downx[len(downx) - 32000+17000:len(downx)-32000+17000+400]  # sine256k
    #newdata = downx[820000:980000] #All_four_continuous_data
 #   newdata = downx6[len(downx6) - 32000 + 6450:len(downx6) - 32000 + 6450 + 200]
   # newdata6 = downx6[len(downx6)-32000+6450:len(downx6)-32000+6450+100]#All_four_continuous_data
   # newdata3 = downx3[len(downx3)-32000+6454:len(downx3)-32000+6454+50]#All_four_continuous_data
   # newdata5 = downx5[len(downx5) -32000+6450:len(downx5)-32000+6450+50]#All_four_continuous_data
    newdata = downx[32000:len(downx)]
 #   print(type(newdata))



#    print(type(newdata))
   # numpy_newdata=np.array(newdata)
   # print(type(numpy_newdata))

    ax1.clear()
    ax1.cla()
  #  ax2.clear()
  #  ax2.cla()
  #  ax3.clear()
  #  ax3.cla()
  #  ax4.clear()
  #  ax4.cla()
#    ax1.plot(t,newdata,'.-')

    ax1.plot(newdata)
   # ax2.plot(newdata6)
   # ax3.plot(newdata3)
   # ax4.plot(newdata5)

    downx.clear()
    #downx6.clear()
    #downx3.clear()
    #downx5.clear()

    CC.close()
    #CC6.close()
    #CC3.close()
    #CC5.close()

    conn.close()

ani = animation.FuncAnimation(fig, animate,interval=500000)
plt.tight_layout()
plt.show()