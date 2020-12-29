# """
#     sensors.py
#     ------------
#     Implements communication with lm_sensors via userspace tool sensors
#     The module also provides functions for populating the QT Tree Widget with hardware nodes and temperature sensors.
# """

import json
import xml.etree.ElementTree as ET
import subprocess
from PyQt5 import QtCore, QtWidgets, QtGui

def populate_tree(treeWidget, start_silently):
    sensors_dict = get_sensors()

    # No sensor data (empty list) indicates LM-Sensors is not able to collect any sensor data
    if not sensors_dict:
        print("No sensors available with LM-Sensors!")

    # Add hardware nodes and temperature sensors to the three widget
    for component_key, component_nodelist in sensors_dict.items():
        parent = treeWidget
        component_qt_item = QtWidgets.QTreeWidgetItem(parent)
        component_qt_item.setText(0, component_key)
        component_qt_item.setFlags(QtCore.Qt.ItemIsEnabled)  # Make hardware nodes "not selectable" in the UI

        for sensor_key, sensor_nodelist in component_nodelist.items():
            if sensor_key == 'Adapter':
                continue
            else:
                parent = component_qt_item
                sensor_qt_item = QtWidgets.QTreeWidgetItem(parent)
                sensor_qt_item.setText(0, sensor_key)  # First column, name of the node
                sensor_qt_item.setFlags(QtCore.Qt.ItemIsEnabled)  # Make hardware nodes "not selectable" in the UI

                for sensor_param_key, sensor_param_nodelist in sensor_nodelist.items():
                    if ("temp" not in sensor_param_key):
                        continue

                    sensor_param_parent = sensor_qt_item
                    sensor_param_qt_item = QtWidgets.QTreeWidgetItem(sensor_param_parent)

                    sensor_param_qt_item.setText(0, sensor_param_key)  # First column, name
                    sensor_param_qt_item.setText(1, component_key + "<>" + sensor_key + "<>" + sensor_param_key)  # Second column, name
                    sensor_param_qt_item.setText(2, str(sensor_param_nodelist))  # Third column, temperature value

                    # Set node name and temperature value to blue
                    sensor_param_qt_item.setForeground(0, QtGui.QBrush(QtCore.Qt.blue))
                    sensor_param_qt_item.setForeground(2, QtGui.QBrush(QtCore.Qt.blue))
                
                if sensor_qt_item.childCount() == 0:
                    parent.removeChild(sensor_qt_item)

def get_sensors():
    # Get LM-Sensors Data    
    sensors_json = subprocess.check_output(['sensors', '-j'])
    sensors_dict = json.loads(sensors_json)

    # Get Nvidia-Smi Sensors data, if available
    result_nvidia_smi_search = subprocess.check_output(['which', 'nvidia-smi']).decode("utf-8")
    nvidia_smi_installed = not result_nvidia_smi_search.startswith("which: no")
    if nvidia_smi_installed:
        nvidia_query_xml = subprocess.check_output(['nvidia-smi','-q','-x']) # Get all GPU data in XML format
        nvidia_result_treeroot = ET.fromstring(nvidia_query_xml)

        for gpu in nvidia_result_treeroot.findall('gpu'):
            gpu_name = gpu.find('product_name').text + " || " + gpu.attrib['id']
            gpu_temperature = gpu.find('temperature').find('gpu_temp').text.strip(' C')

            if not sensors_dict:
                sensors_dict = {}

            sensors_dict[gpu_name] = { "Temperature" : { "temp_in_celcius" : gpu_temperature } }

    return sensors_dict