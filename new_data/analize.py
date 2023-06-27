# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 18:42:15 2023

@author: gojiy
"""

#Bibliotecas
import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

##Generar un archivo PKL
import pickle 

path_file = "E:\\T_proyect\\20230622\\datamanager\\Rebanada02\\"
namefile = "OPTOa20230622s02_RAW.h5"

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


vChannelData = file_raw['Data']['Rcording_0']['Stream_0']['ChannelData'][0]