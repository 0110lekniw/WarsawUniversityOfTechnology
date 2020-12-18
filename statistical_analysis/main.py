from matplotlib import pyplot as plt
from glob import glob
import pandas as pd
import numpy as np
from pandas.plotting import table

names = glob('D:/GitHub/sensors_measurements_projects/statistical_analysis/data/*.*')

datasets = ['No filter', 'time step 1', 'time step 10', 'time step 100']
requiredData = ['Standard Deviation', 'Median', '25th Percentile', '75th Percentile', 'Minimum Value', 'Maximum Value']
arrays = {}
headings = {}
outliers = {}

standardDeviation = []
median = []
quantiles_25 = []
quantiles_75 =[]
minimumValues = []
maximumValues = []
calculatedMinimumValues = []
calculatedMaximumValues = []

fig1, ax = plt.subplots(1, 1)
fig2, az = plt.subplots(1, 1)
fig3, ay = plt.subplots(1, 1)

for i in range(len(names)):
  array = np.loadtxt(names[i], dtype=str)[:60, :]
  array = np.delete(array, range(2, int(array.shape[1] - 1)), 1)

  az.plot( array[:, 0])

  heading = np.array(array[:, 0], dtype = float)
  minimumValues.append(np.amin(heading))
  maximumValues.append(np.amax(heading))

  median.append(np.median(heading))
  standardDeviation.append(np.std(heading))
  quantiles_25.append(np.quantile(heading, 0.25))
  quantiles_75.append(np.quantile(heading, 0.75))

  calculatedMinimumValues.append(quantiles_25[i] - 1.5*(quantiles_75[i]-quantiles_25[i]))
  calculatedMaximumValues.append(quantiles_25[i] + 1.5*(quantiles_75[i]-quantiles_25[i]))

  outliersPosition = list(np.where(array[1] == "E")[0])
  outliersPosition += list(np.where(heading < calculatedMinimumValues[i])[0])
  outliersPosition += list(np.where(heading > calculatedMaximumValues[i])[0])
  outliers[1] = array[outliersPosition, :]

  array = np.delete(array, outliersPosition, 0)
  ax.hist(array[:, 0], density=True, alpha=0.75)

  headings[datasets[i]] = array[:, 0].astype('float64')

headingRange = range(int(min(minimumValues))-1, int(max(maximumValues))+1, 1)
ax.axes.set_xscale('linear')
az.axes.set_yscale('linear')

ay.boxplot(headings.values())


fig1.savefig('results/histogram.png')
fig3.savefig('results/boxPlots.png')
fig2.savefig('results/heading.png')

data = pd.DataFrame([median, standardDeviation, quantiles_25, quantiles_75, calculatedMinimumValues,
                     calculatedMaximumValues], columns = datasets, index = requiredData).T

data.to_excel("results/results.xlsx")
print(data)