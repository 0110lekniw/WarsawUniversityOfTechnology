from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt

wb = load_workbook('Pulse engine_test1_1.xlsx', read_only=True)
ws = wb[wb.sheetnames[0]]
data = np.array([[i.value for i in j[0:5]] for j in ws.rows])
del ws, wb

plt.rcParams['font.size'] = '8'
plt.rcParams['font.family'] = 'Times New Roman'
fig, ax = plt.subplots(1, 4)
names = data[0, :]

for i in range(data.shape[1]-1):
  ax[i].plot(data[1:, 0].astype('float64'), data[1:, i+1].astype('float64'))
  ax[i].set_title(names[i+1])

fig.savefig('results/plots.png')
