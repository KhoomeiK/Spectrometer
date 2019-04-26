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
from CCDcallbacks import *
from CCDhelp import *
from sys import exit

class MenuBar(tk.Frame):


    def __init__(self, master,plot):
        tk.Frame.__init__(self, master)
        
        self.menubar = tk.Menu(master)
      
        #self.filemenu = tk.Menu(self.menubar)
        #self.filemenu.add_command(label="Open", command=lambda plot=plot: openf(plot))
        #self.filemenu.add_command(label="Save", command=savef)
        #self.filemenu.add_separator()
        #self.filemenu.add_command(label="Exit", command=callback)
        #self.menubar.add_cascade(label="File", menu=self.filemenu)

        #self.helpmenu = tk.Menu(self.menubar)
#        self.helpmenu.add_command(label="Help", command=callback)
#        self.helpmenu.add_separator()
        self.menubar.add_command(label="Exit", command=exit)
        self.menubar.add_command(label="About", command=lambda helpfor=10: helpme(helpfor))
#        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        master.config(menu=self.menubar)



