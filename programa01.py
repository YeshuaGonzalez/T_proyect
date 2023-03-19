# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 18:13:51 2023

@author: gojiy
"""

import pickle
import h5py
import numpy as np
#import matplotlib.pyplot as plt
import os
import copy

#path = "E:\\Servicio\\MEA2\\20211004\\H5\\SPK\\CTR"
path = "E:\\Servicio\\MEA2\\20211015\\H5\\SPK\\CTR"
content_dir = os.listdir(path)
content_dir.sort()

#Open Resume File
index_dot = content_dir[0].index('.')
name = path+"\\"+content_dir[0][0:index_dot]+ ".txt"
resume_file = open(name, "w")


#Nombre de cada archivo encontrado
for i in range(0,len(content_dir)):
    print("FILE[{}]: {}".format(i, content_dir[i]))
    resume_file.write("FILE[{}]: {}\n".format(i, content_dir[i]))

#Cargar archivos 

files = []
keys = []
keys_segments = []

for i in range(0,len(content_dir)):
    files.append(h5py.File(path+"\\"+content_dir[i]))#Cargar el archivo .h5
    keys.append(list(files[i]['Data']['Recording_0']['SegmentStream']['Stream_0'].keys()))
    keys_segments.append([])            
                
    for j in range(0, len(keys[i])):
        if "SegmentData" in keys[i][j] and not("ts" in keys[i][j]):
            keys_segments[i].append(keys[i][j])
        
#Se imprime el tamaño de cada archivo
num_electrodes = []
for i in range(0,len(keys_segments)):
    print("Number of electrodes in file{}: {}".format(i,len(keys_segments[i])))
    resume_file.write("Number of electrodes in file{}: {}\n".format(i,len(keys_segments[i])))
    
    num_electrodes.append(len(keys_segments[i]))

'''________________________Concatenar Archivos_____________________________'''

if max(num_electrodes) == 120:
    
    # ¿Qué archivo tiene los segmentos comletos?
    max_num_electrodes = max(num_electrodes)
    index_max = num_electrodes.index(max_num_electrodes)
    ###
    electrodes = dict() #Se crea un diccionario 
    ###
    for i in range(0, 120):
        
        e_files_temp = []
        
        for j in range(0,len(files)):
            
            try:
                e_files_temp.append(np.array(files[j]['Data']['Recording_0']['SegmentStream']['Stream_0'][keys_segments[index_max][i]]).T)
            except KeyError:
                e_files_temp.append(np.array([]))
        
        empty_args = []
        #Ver que arreglos estan vacíos y guardar su indice en la lista "empty_args"
        for j in range(0,len(e_files_temp)):
            if len(e_files_temp[j]) == 0:
               empty_args.append(j) 
               
        # for recorre el arreglo del último elemento al primero
        for k in range(len(empty_args)-1,-1,-1):
        # Para borrar indices que si existen
            e_files_temp.pop(empty_args[k])
        
        e_np_temp = np.concatenate(e_files_temp, axis = 0)
        electrodes[keys_segments[index_max][i]] = e_np_temp
        
else:
    print("Ninguno de los archivos tiene los electrodos completos...")
    
    # Create a deeo copy of the keys_segments[0]
    keys_segments_temp = copy.deepcopy(keys_segments[0])
    
    for i in range(1, len(keys_segments[0])):
        #list merge without dupe
        keys_segments_temp.extend([element for element in keys_segments[1] if element not in keys_segments_temp])
    
    electrodes = dict() #Se crea un diccionario 
    ###
    for i in range(0, len(keys_segments_temp)):
        
        e_files_temp = []
        
        for j in range(0,len(files)):
            
            try:
                e_files_temp.append(np.array(files[j]['Data']['Recording_0']['SegmentStream']['Stream_0'][keys_segments_temp[i]]).T)
            except KeyError:
                e_files_temp.append(np.array([]))
        
        empty_args = []
        #Ver que arreglos estan vacíos y guardar su indice en la lista "empty_args"
        for j in range(0,len(e_files_temp)):
            if len(e_files_temp[j]) == 0:
               empty_args.append(j) 
               
        # for recorre el arreglo del último elemento al primero
        for k in range(len(empty_args)-1,-1,-1):
        # Para borrar indices que si existen
            e_files_temp.pop(empty_args[k])
        
        e_np_temp = np.concatenate(e_files_temp, axis = 0)
        electrodes[keys_segments_temp[i]] = e_np_temp
    
    
'''Resumen'''

conde = 0
#print("\n     Key/Electrode    number of spikes per electrode", end='')
for key in electrodes.keys():
    #encabezado tabla
    if conde == 0:
        print("\n     Key/Electrode    ", end='')
        resume_file.write("\n     Key/Electrode    ")
        for i in range(0,len(content_dir)):
            print("File[{}] ".format(i), end = '')
            resume_file.write("File[{}] ".format(i))
        print("Concat")
        resume_file.write("Concat\n")
    
    file_size = []
    
    for i in range(0,len(content_dir)):
        try:
            file_size.append(len(np.array(files[i]['Data']['Recording_0']['SegmentStream']['Stream_0'][key]).T))
        except KeyError:
            file_size.append(0)
        
        #star of line
        if i == 0:
            print("[{:<3}]{:<15}: {:<7}".format(conde,key,file_size[i]), end = '')
            resume_file.write("[{:<3}]{:<15}: {:<7}".format(conde,key,file_size[i]))
        # end of the line, the last file
        elif i == len(content_dir)-1:
            print(" {:<7} {:<7}".format(file_size[i], len(electrodes[key])))
            resume_file.write(" {:<7} {:<7}\n".format(file_size[i], len(electrodes[key])))
        #middle of lines
        else:
            print(" {:<7}".format(file_size[i]), end = '')
            resume_file.write(" {:<7}".format(file_size[i]))
        
            
    #print("{:<16}-> F1: {:<4}, F2: {:<4}, F3: {:<4}, C: {:<4}".format(key,file_size[0], file_size[1], file_size[2], len(electrodes[key])))
    #resume_file.write("[{}]{:<20}-> F1: {:<4}, F2: {:<4}, F3: {:<4}, C: {:<4}\n".format(conde,key,file_size[0], file_size[1], file_size[2], len(electrodes[key])))
    conde+=1

resume_file.close()

#Gráfica de prueba

#plt.plot(electrodes['SegmentData_68'].T)
    
'''Crear el archivo pckl'''

# Escritura en modo binario, vacía el fichero si existe
index_dot = content_dir[0].index('.')
name = path+"\\"+content_dir[0][0:index_dot]+ ".pckl"
print(name)
electrodes_file = open(name,'wb')
# Escribe la colección en el fichero 
pickle.dump(electrodes, electrodes_file) 
electrodes_file.close()