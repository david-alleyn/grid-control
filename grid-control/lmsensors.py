# On linux, most sensors are provided through the lmsensors program/library
# Most CPUs, Motherboards, GPUs have sensors that will interface with this library
# Nvidia GPUs using proprietary drivers do not use this sensor package. Nvidia provides its own interface

import sensors

TEMPSENSOR = 512

# subfeature type 512: temp sensor

# sensor ids should be a combination of names: chip.name + feature.name + subfeature.number

def get_sensor_tree():
    sensor_tree = []

    for chip in sensors.get_detected_chips():
        features_with_tempsensors = []

        for feature in chip.get_features():
            temp_sensors = []

            for subfeature in chip.get_all_subfeatures(feature):
                if subfeature.type == TEMPSENSOR:
                    temp_sensors.append(subfeature.number)

            if temp_sensors:
                new_node = [chip.get_label(feature), temp_sensors]
                features_with_tempsensors.append(new_node)

        if features_with_tempsensors:
            new_node = [chip.str(), features_with_tempsensors]
            sensor_tree.append(new_node)

    # If the there are any elements in the list at all, we have a valid list. Otherwise, return None
    if sensor_tree:
        return sensor_tree
    else:
        sensor_tree = None
        return sensor_tree

def print_stuff():
    for chip in sensors.get_detected_chips():
        #print(chip)

        for feature in chip.get_features():
            #print('  {0}'.format(chip.get_label(feature)))

            for subfeature in chip.get_all_subfeatures(feature):
                #print('    {0}'.format(subfeature,
                #                       chip.get_value(subfeature.number)))

            #print() new line basically

# def main():
#     print_stuff()


# if __name__ == '__main__':
#     try:
#         main()
#     finally:
#         sensors.cleanup()