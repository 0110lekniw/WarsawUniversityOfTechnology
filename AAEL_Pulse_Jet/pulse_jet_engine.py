from openpyxl import load_workbook
import numpy as np
import matplotlib.pyplot as plt

wb = load_workbook('Pulse engine_test1_1.xlsx', read_only=True)
ws = wb[wb.sheetnames[0]]
data = np.array([[i.value for i in j[0:5]] for j in ws.rows])
del ws, wb

fig, ax = plt.subplots(1, 4)
axis0 = data.shape[0]
axis1 = data.shape[1]
print(data[0, 4])
for i in range(data.shape[1]-1):
  ax[i-1].plot(data[1:, 0], data[1:, i])
