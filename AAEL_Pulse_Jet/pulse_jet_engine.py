from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt
import scipy

importData = False
plotGraphs = False
# constants
# frequencyOfSampling, inletTemperatureToV, pressureToV, exhaustTemperatureToVo, fuelPressureToV, thrustToV,
constants = [1/3500, 120, 120, 1.6, 1, 35]

if importData:
  # import of the data
  wb = load_workbook('Pulse engine_test1_1.xlsx', read_only=True)
  ws = wb[wb.sheetnames[0]]
  data = np.array([[i.value for i in j[0:5]] for j in ws.rows])
  names = data[0, :]
  for columns in range(data.shape[1]):
    savedArray = data[1:, columns].astype('float64')
    savedArray = np.multiply(savedArray, constants[columns])
    np.savetxt('data/'+names[columns]+'.txt', savedArray)
  np.savetxt('data/names.txt', names, fmt='%s')
  del ws, wb

#calculating the data

#
plt.rcParams['font.size'] = '8'
plt.rcParams['font.family'] = 'Times New Roman'
fig, ax = plt.subplots(1, 4)

names = np.loadtxt('data/names.txt', delimiter='\n', dtype=str)
time = np.loadtxt('data/'+names[0]+".txt")
names = names[1:]

for i in range(names.shape[0]):
  if plotGraphs:
    plottedArray = np.loadtxt('data/'+names[i]+'.txt', dtype=float)
    ax[i].plot(time, plottedArray)
    frequency = scipy.fft(plottedArray)
    ax[i].set_title(names[i])

pressure_file = None
for name in names:
  str.lower(name)
  if str.find(name, "chamber") > 0: pressure_file = name
pressure = np.loadtxt('data/'+pressure_file+'.txt', dtype=float)
pressure.

fig.savefig('results/plots.png')
