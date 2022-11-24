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

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)



conn = sqlite3.connect('ECG_sir_32khzsamp.db')
CC = conn.cursor()
CC2 = conn.cursor()


CC.execute("SELECT * FROM CH4")  # <<<<<<<<<< ADDED
number_of_rows = CC.execute("SELECT * FROM CH4")
downx=[]
print((number_of_rows))
    #print(len(CC.fetchall()))
    #for row in CC.fetchmany(4000):
     #   downx.append(row[0])


b=32000*100
for row in CC.fetchall():
    downx.append(row[1])

newdata= downx[820000:980000]
print(type(newdata))

workbook = xlsxwriter.Workbook('write_ECG_SirFinal.xlsx')
worksheet = workbook.add_worksheet()

for rows in range(len(newdata)):
    worksheet.write(rows, 0, newdata[rows])
    print((rows))
workbook.close()
print("End_xlx")




print(type(newdata))
#numpy_newdata=np.array(newdata)
#print(type(numpy_newdata))
   # newdata= downx[1800:2000]
   # for row in CC2.fetchall():
     #   downx2.append(row[0])
    #newdata2 = downx2[(len(downx2) - 200):]
    #newdata=downx[1850:6000]

ax1.plot(newdata)
downx.clear()
CC.close()
conn.close()

#ani = animation.FuncAnimation(fig, animate,interval=500000)
plt.tight_layout()
plt.show()