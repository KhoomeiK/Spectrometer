 # Copyright (c) 2018 Esben Rossel
 # All rights reserved.
 #
 # Author: Esben Rossel <esbenrossel@gmail.com>
 #
 # Redistribution and use in source and binary forms, with or without
 # modification, are permitted provided that the following conditions
 # are met:
 # 1. Redistributions of source code must retain the above copyright
 #    notice, this list of conditions and the following disclaimer.
 # 2. Redistributions in binary form must reproduce the above copyright
 #    notice, this list of conditions and the following disclaimer in the
 #    documentation and/or other materials provided with the distribution.
 #
 # THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 # ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 # ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE
 # FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 # DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 # OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 # HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 # LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 # OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 # SUCH DAMAGE.

import tkinter as tk
import numpy as np
import serial
import config
import csv

def callback():
    print("called the callback!")

def plotdata(myCCDplot):
    myCCDplot.a.clear()
    if (config.datainvert == 1):
        myCCDplot.a.plot((config.rxData16[10]+config.rxData16[11])/2 + config.offset - config.rxData16)
        myCCDplot.a.set_ylabel("Intensity")
    else:
        myCCDplot.a.plot(config.rxData16)
        myCCDplot.a.set_ylabel("ADCcount")
    myCCDplot.a.set_xlabel("Pixelnumber")
    myCCDplot.canvas.draw()

def ICGSHcallback(name, index, mode, status, tint, colr, SH, ICG):
#    print("SH change!")
#    status.set("news")
#    colr.set("red")

    config.SHperiod = np.uint32(int(SH.get()))
    config.ICGperiod = np.uint32(int(ICG.get()))
    tint.set("Integration time is " + str(config.SHperiod/2000) + " ms")

    #if (int(ICG.get()) % int(SH.get()) or (int(SH.get())<20) or (int(ICG.get())<14776) ):
    if ((config.ICGperiod % config.SHperiod) or (config.SHperiod < 20) or (config.ICGperiod < 14776)):
        status.set("CCD pulse timing violation!")
        colr.configure(fg="red")
    else:
        status.set("Correct CCD pulse timing.")
        colr.configure(fg="green")

def AVGcallback(AVGvalue):
    config.AVGn[1] = np.uint8(AVGvalue)

def INVcallback(name, index, mode, invert, myCCDplot):
    config.datainvert = invert.get()
    plotdata(myCCDplot)

def BALcallback(name, index, mode, balanced, myCCDplot):
    config.balanced = balanced.get()
    plotdata(myCCDplot)

def DEVcallback(name, index, mode, Device, status, colr):
    config.port = Device.get()
    try:
        ser = serial.Serial(config.port, config.baudrate, timeout=1)
        status.set("Device exist")
        ser.close()
        colr.configure(fg="green")
    except serial.SerialException:
        status.set("Device doesn't exist")
        colr.configure(fg="red")

def openf(myCCDplot):
    filename =  tk.filedialog.askopenfilename(title = "Select file",filetypes = (("data files","*.dat"),("all files","*.*")))
#    try:
#        fp = open(filename,'r')          
#    except:
#        messagebox.showerror("By the great otter!","There was a read error.")
#    print (filename)
    i = 0
    with open(filename, newline='') as fp:
        ccdreader = csv.reader(fp, delimiter=' ', quotechar='|')
        for row in ccdreader:
            if i > 3:
                config.rxData16[int(row[0])-1] = int(row[1])
            i += 1
        plotdata(myCCDplot)

def savef():  
    filename =  tk.filedialog.asksaveasfilename(title = "Select file",filetypes = (("data files","*.dat"),("all files","*.*")))
    with open(filename, 'w', newline='') as fp:
        fp.write("#Data from the TCD1304 linear CCD\n")
        fp.write("#column 1 = pixelnumber,  column 2 = pixelvalue\n")
        fp.write("#Pixel 1-32 and 3679-3694 and are dummy pixels\n")
        fp.write("#SH-period: "+str(config.SHperiod)+"    ICG-period: "+str(config.ICGperiod)+"    Integration time: "+str(config.SHperiod/2)+" us\n")
        ccdwriter = csv.writer(fp, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range (0, 3694):
            ccdwriter.writerow([i+1, config.rxData16[i]])

def exportgfx():
    print("export!")
