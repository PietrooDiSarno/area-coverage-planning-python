import glob
import os
from turtledemo.penrose import start

import matplotlib.pyplot as plt
import numpy as np

from conversion_functions import mat2py_et2utc


class dataHandling:
    def __init__(self, dataPath_ = None):

        if dataPath_:
            self.valPath = os.path.join(dataPath_, 'ROI_makespans', 'makespanValues')
            self.plotPath = os.path.join(dataPath_, 'ROI_makespans', 'plots')
        else:  # Use the path specified with the configuration file or the default
            self.valPath = os.path.join(self.getDefaultDataPath(), 'makespanValues')
            self.plotPath = os.path.join(self.getDefaultDataPath(), 'plots')

        print('dataHandling: Using ', self.valPath, ' for makespan values and ', self.plotPath, ' for plots')

        if not os.path.isdir(self.valPath):
            print('Creating folder', self.valPath)
            os.makedirs(self.valPath, exist_ok = True)

        if not os.path.isdir(self.plotPath):
            print('Creating folder', self.plotPath)
            os.makedirs(self.plotPath, exist_ok = True)

    def getDefaultDataPath(self):
        homeFolder = os.path.expanduser('~')
        dataFolder = os.path.join(homeFolder, 'ROI_makespans')
        return dataFolder

    def getName(self, mosaic, ROIname, n):
        return '%s_%s_%d' % (ROIname, mosaic, n)

    def savePlots(self, mosaic, ROIname, start_times, makespan):
        fname = os.path.join(self.plotPath, self.getName(mosaic, ROIname, len(start_times)) + '.tif')
        plt.figure()
        not_visible = []
        visible = []
        makespan_ = []
        for i,val in enumerate(makespan):
            if val == None:
                not_visible.append(start_times[i])
            else:
                visible.append(start_times[i])
                makespan_.append(makespan[i])
        plt.plot(visible, makespan_, 'o', color='b', linestyle='none', markersize=2)
        plt.plot(not_visible, np.zeros(len(not_visible)), 'o', color='r', linestyle='none', markersize=2)
        plt.xticks(np.linspace(start_times[0],start_times[-1],num=6),
                   mat2py_et2utc(np.linspace(start_times[0],start_times[-1],num=6),'C',0), rotation=15)
        plt.xlabel('Initial observation instant')
        plt.ylabel('Observation make-span [s]')
        plt.title(f"Function for the {ROIname} ROI")
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.20, top=0.92)
        plt.savefig(fname, format="tiff")
        print(f"Plot saved as {self.getName(mosaic, ROIname, len(start_times)) + '.tif'}")

    def saveValues(self, mosaic, ROIname, start_times, makespan):
        fname = os.path.join(self.valPath, self.getName(mosaic, ROIname, len(start_times)) + '.txt')
        with open(fname, 'w') as file:
            file.write("start_times:\n")
            file.write(" ".join(map(str, start_times)) + "\n")

            file.write("makespan:\n")
            file.write(" ".join(map(str, makespan)) + "\n")

            file.write("num_points:\n")
            file.write(str(len(start_times)) + "\n")
        print(f"File saved as {self.getName(mosaic, ROIname, len(start_times)) + '.txt'}")

    def readValues(self, filename, ROIname):
        with (open(filename, 'r') as file):
            lines = file.readlines()
            data = {}
            current_key = None
            for line in lines:
                line = line.strip()
                if line.endswith(':'):
                    current_key = line[:-1]
                    data[current_key] = []
                elif current_key:
                    data[current_key].append(line)

            start_times = np.array([float(x) for x in data["start_times"][0].split()])
            makespan = []
            for x in data["makespan"][0].split():
                if x != 'None':
                    makespan.append(float(x))
                else:
                    makespan.append(None)
            makespan = np.array(makespan)
            num_points = int(data["num_points"][0])

            print('\n', ROIname, 'ROI','with',num_points,'points','\n', 'start_times:', start_times, '\n','makespan:', makespan, '\n')
            return start_times, makespan, num_points

    def getValues(self, mosaic, ROIname, n_points = None):
        if n_points:
            fname = os.path.join(self.valPath, self.getName(mosaic, ROIname, n_points) + '.txt')
            start_times, makespan, num_points = self.readValues(fname,ROIname)
            return start_times, makespan, num_points
        else:
            pattern = os.path.join(self.valPath,'%s_%s' % (ROIname, mosaic) + '*.txt')
            file_list = glob.glob(pattern)
            start_times = []
            makespan = []
            num_points = []
            for fname in file_list:
                aux1, aux2, aux3 = self.readValues(fname,ROIname)
                start_times.append(aux1)
                makespan.append(aux2)
                num_points.append(aux3)
            return start_times, makespan, num_points

