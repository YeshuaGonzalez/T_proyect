# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 15:21:16 2023

@author: gojiy
"""
# GUI
import dearpygui.dearpygui as dpg

# Others
import h5py
import numpy as np
#import matplotlib.pyplot as plt
#from tqdm import tqdm

#global variables
channel_list = []

# Create GUI
dpg.create_context()


# CALLBACKS
#__________________________________________________
def callback(sender, app_data):
    print('OK was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)
    print("file_path: {}".format(app_data['file_path_name']))
    dpg.set_value(label1_control,app_data['file_path_name'])
    
    print("Charging file ... ")
    dpg.set_value(messages, "Charging file ... ")
    path_file = app_data['file_path_name']
    #print(os.path.abspath(path_file))
    try :
        global file 
        file = h5py.File(path_file)
        global channel_data
        channel_data = file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
        options = list(range(0,len(channel_data)))
        dpg.configure_item(combo1, items = options)
        
        
    except: 
        print("Error to charge file")
    
    print("End charge ... ")   
    dpg.set_value(messages, "End charge :)")

def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)
    
def callback_plot(sender, app_data):
    
    #print('file' in globals())
    #print('channel_data' in globals())
    if dpg.get_value(label1_control) != "File path" and 'file' in globals() and 'channel_data' in globals():
        dpg.set_value(messages, "Plotting")
        index = dpg.get_value(combo1)
        
        if index != "Channel" and not(int(index) in channel_list):
            signal_data = np.array(channel_data[int(index)])
            
            #x_data_np = np.arange(0, 10000, 1)
            #y_data_np = signal_data[0:10000]
            ini = int(dpg.get_value(val_ini))
            fin = int(dpg.get_value(val_fin))
            x_data_np = np.arange(ini, fin, 1)
            y_data_np = signal_data[ini:fin]
            
            #series belong to a y axis
            dpg.add_line_series(x_data_np, y_data_np, label="ch {}".format(index), parent="y_axis")
            channel_list.append(int(index))
            print("Finish...")
            dpg.set_value(messages, "Finish ...")
            print(channel_list)
        else :
            print("Este canal ya se cargo / Seleccione un canal")
            print(channel_list)
        
    else:
        print("Callback plot ready!")
        dpg.set_value(messages, "Call back plot ready!")
    
#__________________________________________________

dpg.create_viewport(title='GUI test', width=1000, height=800)

# file & directory selector configuration
with dpg.file_dialog(directory_selector = False,
                      show = False,
                      callback = callback,
                      tag = "file_dialog_id",
                      cancel_callback = cancel_callback,
                      width = 700,
                      height= 400,
                      default_path = "E:\ExpRecientes"):
    dpg.add_file_extension(".h5", color = (255, 0, 255, 255), custom_text = "[H5]")
    dpg.add_file_extension(".*")
    

# ____________________________________________CREATE A WINDOW____________________________________________

with dpg.window(label="Simple plot example"):
    
    '''Line 1'''
    with dpg.group(horizontal = True):
    #create file & directory selector
        button_file = dpg.add_button(label = "File Selector", 
                                 callback = lambda: dpg.show_item("file_dialog_id"))
    # label: Path File Name
        label1_control = dpg.add_text("File path")
    '''Line 2'''
    with dpg.group(horizontal = True):
        dpg.add_button(label = "Plot channel",
                   callback = callback_plot)
    
        combo1 = dpg.add_combo(["Channel"], default_value = "Channel")
    '''Line 3'''
    with dpg.group(horizontal = True):
        val_ini = dpg.add_input_text(default_value = "0", label = "Valor inicial", width = 100)
        val_fin = dpg.add_input_text(default_value = "1000", label = "Valor final", width = 100)

    #create plot
    with dpg.plot(label="Raw Data", width=800, height=600):
        dpg.add_plot_legend()
        
        #Create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
    messages = dpg.add_text("System Messages", color = [0,124,255,255])
        
        #series belong to a y axis
        #dpg.add_line_series(x_data, y_data, label="ch 52", parent="y_axis")

# dpg.create_viewport(title="Custom title", width=800, height=600)    

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()