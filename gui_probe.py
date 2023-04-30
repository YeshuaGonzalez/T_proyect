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
import os
#from tqdm import tqdm


#Global varibales
x_data=[]
y_data=[]

#Charging phase 
# path_file = "E:\\ExpRecientes\\PRK20220816s01_RAW.h5"
# file = h5py.File(path_file)
# channel_data = file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
# signal_data = np.array(channel_data[52])

# x_data=[]
# y_data=[]
# creating data
# for i in range(0, 1000):
#     x_data.append(i)
#     y_data.append(signal_data[i])
    


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

def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)
    
def callback_plot(sender, app_data):
    
    if dpg.get_value(label1_control) != "File path" :
        print("Charging file ... ")
        path_file = dpg.get_value(label1_control)
        #print(os.path.abspath(path_file))
        try :
            file = h5py.File(path_file)
        except: 
            print("Error to charge file")
        
        channel_data = file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
        signal_data = np.array(channel_data[52])
        
        #creating data
        # for i in range(0, 30000):
        #     print(i)
        #     x_data.append(i)
        #     y_data.append(signal_data[i])
        
        x_data_np = np.arange(0, 10000, 1)
        y_data_np = signal_data[0:10000]
        print("Finish...")
        #series belong to a y axis
        dpg.add_line_series(x_data_np, y_data_np, label="ch 52", parent="y_axis")
        
    else:
        print("Callback plot ready!")
    
#__________________________________________________

dpg.create_viewport(title='Custom Title', width=1000, height=700)

# file & directory selector configuration
with dpg.file_dialog(directory_selector = False,
                      show = False,
                      callback = callback,
                      tag = "file_dialog_id",
                      cancel_callback = cancel_callback,
                      width = 700,
                      height= 400):
    dpg.add_file_extension(".h5", color = (255, 0, 255, 255), custom_text = "[H5]")
    dpg.add_file_extension(".*")
    

# ____________________________________________CREATE A WINDOW____________________________________________

with dpg.window(label="Simple plot example"):
    
    # label: Path File Name
    label1_control = dpg.add_text("File path")
    
    #create file & directory selector
    dpg.add_button(label = "File Selector", 
                   callback = lambda: dpg.show_item("file_dialog_id"))
    
    dpg.add_button(label = "Plot segment 52",
                   callback = callback_plot)

    #create plot
    with dpg.plot(label="Raw Data", width=800, height=600):
        dpg.add_plot_legend()
        
        #Create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
        
        #series belong to a y axis
        #dpg.add_line_series(x_data, y_data, label="ch 52", parent="y_axis")

# dpg.create_viewport(title="Custom title", width=800, height=600)    

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

# import dearpygui.dearpygui as dpg
# import dearpygui.demo as demo

# dpg.create_context()
# dpg.create_viewport(title='Custom Title', width=600, height=600)

# demo.show_demo()

# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()