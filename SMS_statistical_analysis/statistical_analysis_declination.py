from matplotlib import pyplot as plt
from glob import glob
import pandas as pd
import numpy as np
import sys
from pandas.plotting import table

#changing the plots font size and family
plt.rcParams['font.size'] = '8'
plt.rcParams['font.family'] = 'Times New Roman'

#defining the names of the files in data folder
names = glob('/SMS_statistical_analysis/data/*.*')

if len(names) == 0:
  print('no data detected or wrong direction. \n Press Enter')
  input()
  sys.exit()

#defining the required data - useful to describe resulting data
datasets = ['No filter', 'time step 1', 'time step 10', 'time step 100']
requiredData = ['Standard Deviation', 'Median', '25th Percentile', '75th Percentile', 'Minimum Value', 'Maximum Value']

#creating empty libraries and lists for data
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

# creating the area of the plot
fig1, ax = plt.subplots(1, 3)
fig2, az = plt.subplots(1, 1)
fig3, ay = plt.subplots(1, 1)

# itearating accross every detected file
for i in range(len(names)):
  array = np.loadtxt(names[i], dtype=str)[:60, :]
  array = np.delete(array, range(2, int(array.shape[1] - 1)), 1)
  heading = np.array(array[:, 0], dtype = float)


# calculating the moving average values
  calculatedArray = heading
  movingAverageValues = []
  movingStandardDeviation = []
  for j in range(calculatedArray.shape[0]):
    if j == 0:
      singularAverage = calculatedArray[j]
      singularStandardDeviation = 0
    else:
      singularAverage = np.average(calculatedArray[:j])
      singularStandardDeviation = np.std(calculatedArray[:j])
    movingAverageValues.append(singularAverage)
    movingStandardDeviation.append(singularStandardDeviation)

  ax[0].plot( array[:, 0])
  ax[1].plot(movingAverageValues)
  ax[2].plot(movingStandardDeviation)

# saving the range of the array
  minimumValues.append(np.amin(heading))
  maximumValues.append(np.amax(heading))

# calculating required data
  median.append(np.median(heading))
  standardDeviation.append(np.std(heading))
  quantiles_25.append(np.quantile(heading, 0.25))
  quantiles_75.append(np.quantile(heading, 0.75))

  calculatedMinimumValues.append(quantiles_25[i] - 1.5*(quantiles_75[i]-quantiles_25[i]))
  calculatedMaximumValues.append(quantiles_25[i] + 1.5*(quantiles_75[i]-quantiles_25[i]))

# searching for outliers
  outliersPosition = list(np.where(array[1] == "E")[0])
  outliersPosition += list(np.where(heading < calculatedMinimumValues[i])[0])
  outliersPosition += list(np.where(heading > calculatedMaximumValues[i])[0])
  outliers[1] = array[outliersPosition, :]

# updating the data and creating the histogram
  array = np.delete(array, outliersPosition, 0)
  az.hist(array[:, 0], bins=20, alpha=0.75, histtype='barstacked')

# adding the heading values to the dictionary
  headings[datasets[i]] = array[:, 0].astype('float64')

headingRange = range(int(min(minimumValues))-1, int(max(maximumValues))+1, 1)

# setting up the plot description
ax[0].axes.set_yscale('linear')
ax[0].axes.set_title('Change of heading')
ax[1].axes.set_yscale('linear')
ax[1].axes.set_title('Change of average heading ')
ax[2].axes.set_yscale('linear')
ax[2].axes.set_title('Change of standard deviation ')
az.axes.set_xscale('linear')

ay.boxplot(headings.values())

# saving the graphs
fig1.savefig('results/heading.png')
fig3.savefig('results/boxPlots.png')
fig2.savefig('results/histogram.png')

# saving resulting data to xlsx
data = pd.DataFrame([median, standardDeviation, quantiles_25, quantiles_75, calculatedMinimumValues,
                     calculatedMaximumValues], columns=datasets, index=requiredData).T
data.to_excel("results/results.xlsx")