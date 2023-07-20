# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 18:42:15 2023

@author: gojiy
"""

#Bibliotecas
import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import sys

##Generar un archivo PKL
import pickle 

sys.path.insert(1, '/home/yeshua/Documentos/repositorios/T_proyect')
import utiles

#WINDOWS
#path_file = "E:\\T_proyect\\20230622\\datamanager\\Rebanada02\\"

#LINUX
path_file = "/media/yeshua/zeiler_v2/MEA_data/20230622/datamanager/Rebanada02/"

namefile = "L6.h5"

file_raw = h5py.File(path_file+namefile)

'''
-Data
--Recording_0
---AnalogStream
----Stream_0
-----ChannelData : shape (120, 6000000)
------[0].shape() : (6000000,)
-----ChannelDataTimeStamps : shape (1, 3)
------[0] : [      0,       0, 5999999]
-----InfoChannel : shape (120,)
------[0] : (0, 0, 0, 0, b'F7', b'Int', b'V', -12, 0, 100, 59605, 24, b'', b'-1', -1, b'', b'-1', -1)
------[1] : (1, 1, 0, 0, b'F8', b'Int', b'V', -12, 0, 100, 59605, 24, b'', b'-1', -1, b'', b'-1', -1)


'''


#Charge Files

signal_electrode = np.array(file_raw['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][0])
size_signal = len(signal_electrode)

start = 91000
finish = 92000

x = np.arange(0,size_signal)[start:finish]
y = signal_electrode[start:finish]
fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))

ax1.plot(x, y)
st_1s = utiles.StiGen(size_signal,
               10000,
               9,
               1000,
               0,
               1)
z = st_1s[start:finish]*400
ax1.plot(x,z)

#ax1.set_ylim(-2, 2)
ax1.set_title('Raw data explorer')
line2, = ax2.plot([], [])
line3, = ax2.plot([],[])
#line2, = ax2.plot([])

def onselect(xmin, xmax):
    indmin, indmax = np.searchsorted(x, (xmin, xmax))
    indmax = min(len(x) - 1, indmax)

    region_x = x[indmin:indmax]
    
    region_y = y[indmin:indmax]
    
    region_z = z[indmin:indmax]

    if len(region_x) >= 2:
        line2.set_data(region_x, region_y)
        line3.set_data(region_x, region_z)
        ax2.set_xlim(region_x[0], region_x[-1])
        ax2.set_ylim(region_y.min()+50, region_y.max()+50)
        fig.canvas.draw_idle()

span = SpanSelector(
    ax1,
    onselect,
    "horizontal",
    useblit=True,
    props=dict(alpha=0.5, facecolor="tab:blue"),
    interactive=True,
    drag_from_anywhere=True
)
plt.show()
