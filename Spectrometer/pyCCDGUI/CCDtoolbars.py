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
from tkinter import filedialog
import threading
from CCDcallbacks import *
from CCDhelp import *
from CCDserial import *
import config

#top toolbar
class ToolBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.b = tk.Button(master, text="new", width=6, command=callback)
 #       self.b.pack(side=tk.LEFT, padx=2, pady=2)
        self.b.grid(row=0, column=0)

        self.b = tk.Button(master, text="open", width=6, command=callback)
#        self.b.pack(side=tk.LEFT, padx=2, pady=2)
        self.b.grid(row=0, column=1)




#right  toolbar
class CCDtoolbar(tk.Frame):
    def __init__(self, master, plot):
        tk.Frame.__init__(self, master=None)
        SHrow = 6

        self.ICGSHstatus = tk.StringVar()
        self.ICGSHstatus.set("Correct CCD pulse timing.")
        self.ICGSHstatuscolor = tk.StringVar()
        self.DevValue = tk.StringVar()
        #self.DevValue.set(port) #set this after trace-setup, to check port immediately
        self.Devstatus = tk.StringVar()
        #self.Devstatus.set("Device exists")
        self.Devstatuscolor = tk.StringVar()
        
		#initiate CCD-variables
        self.SHvalue = tk.StringVar()
        self.SHvalue.set("200") 
        self.tint = tk.StringVar()
        self.tint.set("Integration time is 0.1 ms")
        self.ICGvalue = tk.StringVar()
        self.ICGvalue.set("500000")
        self.AVGvalue = tk.StringVar()
        self.AVGvalue.set("1")

		#about
#        self.bcollect = tk.Button(self, text="About", width=25, command=lambda helpfor=10: helpme(helpfor))
#        self.bcollect.grid(row=0, columnspan=4, sticky="N")

		#insert vertical space
#        self.grid_rowconfigure(1, minsize=150)

        #geometry-rows
        devrow = 0
        shicgrow = 10
        avgrow = 20
        collectrow = 30
        invrow = 40
        saverow = 50
        

		#device setup
        self.ldevice = tk.Label(self, text="COM-device:")
        self.ldevice.grid(column=0, row=devrow)
        self.eDevice = tk.Entry(self, textvariable=self.DevValue, justify='left')
        self.eDevice.grid(column=1, row=devrow)

		#setup device-status label
        self.ldev = tk.Label(self, textvariable=self.Devstatus, fg="green")
        self.DevValue.trace("w", lambda name, index, mode, Device=self.DevValue, status=self.Devstatus, colr=self.ldev: DEVcallback(name, index, mode, Device, status, colr))
        self.DevValue.set(config.port)
        self.ldev.grid(columnspan=2, row=devrow+1)

		#insert vertical space
        self.grid_rowconfigure(devrow+3, minsize=30) 

		#pulse timing tip
        self.ltipSHICG = tk.Label(self, text="ICG = n·SH")
        self.ltipSHICG.grid(columnspan=2, row=shicgrow-1) 

		#setup SH-entry
        self.lSH = tk.Label(self, text="SH-period:")
        self.lSH.grid(column=0, row=shicgrow)
        self.eSH = tk.Entry(self, textvariable=self.SHvalue, justify='right')
        self.eSH.grid(column=1, row=shicgrow)

        #integration time tip
        #self.ltiptint = tk.Label(self, text="Integration time:")
        #self.ltiptint.grid(row=SHrow+1) 

		#setup ICG-entry
        self.lICG = tk.Label(self, text="ICG-period:")
        self.lICG.grid(column=0, row=shicgrow+1)
        self.eICG = tk.Entry(self, textvariable=self.ICGvalue, justify='right')
        self.eICG.grid(column=1, row=shicgrow+1)

		#setup ICGSH-status label
        self.lICGSH = tk.Label(self, textvariable=self.ICGSHstatus, fg="green")
        self.lICGSH.grid(columnspan=2, row=shicgrow+2)

        #integration time label
        self.ltint = tk.Label(self, textvariable=self.tint)
        #self.ltint = tk.Label(self, text="Integration time is")
        self.ltint.grid(columnspan=2, row=shicgrow+3)

		#insert vertical space
        self.grid_rowconfigure(shicgrow+4, minsize=30) 

		#setup AVG entry
        self.lAVG = tk.Label(self, text="Average:")
        self.lAVG.grid(column=0, row=avgrow)
        #self.eAVG = tk.Entry(self, textvariable=self.AVGvalue, justify='right')
        #self.eAVG.grid(column=1, row=SHrow+4)

        self.AVGscale = tk.Scale(self, orient='horizontal', from_=1, to=15)
        self.AVGscale.configure(command=AVGcallback)
        self.AVGscale.grid(column=1, row=avgrow, sticky="we")


        self.grid_rowconfigure(avgrow+2, minsize=30) 

        self.bcollect = tk.Button(self, text="Collect", command=lambda plot=plot: rxtx(plot))
        self.bcollect.grid(row=collectrow, columnspan=4, sticky="EW", padx=5)

        self.grid_rowconfigure(collectrow+1, minsize=30) 

        #options
        self.optionframe = tk.Frame(self)
        self.optionframe.grid(row=invrow, columnspan=2)        

        #self.optionframe.grid_columnconfigure(0, minsize=70) 

        self.invvar = tk.IntVar()
        self.cinvert = tk.Checkbutton(self.optionframe, text="Plot raw data", variable=self.invvar, offvalue=1, onvalue=0)#, state=tk.ACTIVE)
        self.cinvert.deselect()
        self.cinvert.grid(row=0, column=1, sticky="W")

        self.balvar = tk.IntVar()
        self.cbalance = tk.Checkbutton(self.optionframe, text="Balance output", variable=self.balvar, offvalue=0, onvalue=1)#, state=tk.ACTIVE)
        self.cbalance.select()
        self.cbalance.grid(row=0, column=2, sticky="W")

        self.grid_rowconfigure(invrow+2, minsize=50)

        #files
        self.fileframe = tk.Frame(self)
        self.fileframe.grid(row=saverow, columnspan=2)
        self.bopen = tk.Button(self.fileframe, text="Open", width=11, command=lambda plot=plot: openf(plot))
        self.bsave = tk.Button(self.fileframe, text="Save", width=11, command=savef)
#        self.bexport = tk.Button(self.fileframe, text="Export vector graphics", command=exportgfx)
#        self.bexport.pack(fill=tk.X)
        self.bopen.pack(side=tk.LEFT)
        self.bsave.pack(side=tk.LEFT)

		#setup traces to update tx-data
        self.SHvalue.trace("w", lambda name, index, mode, status=self.ICGSHstatus, tint=self.tint, colr=self.lICGSH, SH=self.SHvalue, ICG=self.ICGvalue: ICGSHcallback(name, index, mode, status, tint, colr, SH, ICG))
        self.ICGvalue.trace("w", lambda name, index, mode, status=self.ICGSHstatus, tint=self.tint, colr=self.lICGSH, SH=self.SHvalue, ICG=self.ICGvalue: ICGSHcallback(name, index, mode, status, tint, colr, SH, ICG))
        self.invvar.trace("w", lambda name, index, mode, invert=self.invvar, plot=plot: INVcallback(name, index, mode, invert, plot))
        self.balvar.trace("w", lambda name, index, mode, balance=self.balvar, plot=plot: BALcallback(name, index, mode, balance, plot))

        #self.AVGvalue.trace("w", lambda name, index, mode, AVG=self.AVGvalue: AVGcallback(name,index,mode,AVG))
        #self.DevValue.trace("w", lambda name, index, mode, Device=self.DevValue, status=self.Devstatus, colr=self.ldev: DEVcallback(name, index, mode, Device, status, colr))


		#help buttons
        self.bhdev = tk.Button(self, text="?", command=lambda helpfor=0: helpme(helpfor))
        self.bhdev.grid(row=devrow, column=3)
        self.bhtiming = tk.Button(self, text="?", command=lambda helpfor=1: helpme(helpfor))
        self.bhtiming.grid(row=shicgrow, rowspan=2, column=3)
        self.bhavg = tk.Button(self, text="?", command=lambda helpfor=2: helpme(helpfor))
        self.bhavg.grid(row=avgrow, column=3)
        self.bhinv = tk.Button(self, text="?", command=lambda helpfor=3: helpme(helpfor))
        self.bhinv.grid(row=invrow, column=3)
       # self.bhbal = tk.Button(self, text="?", command=lambda helpfor=4: helpme(helpfor))
       # self.bhbal.grid(row=invrow+1, column=3)
        self.bhsav = tk.Button(self, text="?", command=lambda helpfor=5: helpme(helpfor))
        self.bhsav.grid(row=saverow, column=3)


        
