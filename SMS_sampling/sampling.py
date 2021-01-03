from glob import glob
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.size'] = '8'
plt.rcParams['font.family'] = 'Times New Roman'


constants = [[1000/50], [121/200], [60/200], [180/200], [117/200]]
titles = ["data", "spectrum"]
xlabels = ["time [s]", "frequency [Hz]"]
ylabels = ["signal [V]", "amplitude"]
names = glob('D:\GitHub\sensors_measurements_projects\SMS_sampling\data\*.txt')
dataTypes = {}
for name in names:
  if len(dataTypes) > 0:
    addKey = True
    for key in dataTypes:
      ratio = SequenceMatcher(None, name, dataTypes[key][0]).ratio()
      if SequenceMatcher(None, name, dataTypes[key][0]).ratio() > 0.95:
        dataTypes[key].append(name)
        addKey = False
        break
    if addKey:
      dataTypes[len(dataTypes)+1]=[name]
  else:
    dataTypes[0] = [name]
del names

types = list(dataTypes.keys())
for datasets in range(len(dataTypes[types[0]])):
  fig, ax = plt.subplots(len(types), 1)
  for type in range(len(types)):
    data = np.loadtxt(dataTypes[types[type]][datasets])
    if type !=0:
      data[:, 0] = np.multiply(data[:, 0], constants[datasets])
    ax[type].plot(data[:, 0], data[:, 1], color = 'k')
    ax[type].set_title(titles[type])
    ax[type].set_ylabel(ylabels[type])
    ax[type].set_xlabel(xlabels[type])
  fig.tight_layout(pad=2.0)
  fig.savefig('results/ex'+str(datasets+1)+'.png')

