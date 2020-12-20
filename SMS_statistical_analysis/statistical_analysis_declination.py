from matplotlib import pyplot as plt
from matplotlib import ticker
from glob import glob
import pandas as pd
import numpy as np
import sys
from pandas.plotting import table

#changing the plots font size and family
plt.rcParams['font.size'] = '8'
plt.rcParams['font.family'] = 'Times New Roman'

#defining the names of the files in data folder
names = glob('C:\GitHub\WarsawUniversityOfTechnology\SMS_statistical_analysis\data\*.*')

if len(names) == 0:
  print('no data detected or wrong direction. \n Press Enter')
  input()
  sys.exit()

#defining the required data - useful to describe resulting data
datasets = ['No filter', 'Time step 1', 'Time step 10', 'Time step 100']
requiredData = ['Standard Deviation', 'Median', '25th Percentile', '75th Percentile', 'Minimum Value', 'Maximum Value',
                'number of outliers']

#creating empty dictionaries and lists for data
arrays = {}
headings = {}
outliers = []

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

  ax[0].plot(heading)
  ax[1].plot(movingAverageValues)
  ax[2].plot(movingStandardDeviation)

# saving the range of the array
  minimumValues.append(np.amin(heading))
  maximumValues.append(np.amax(heading))

# calculating required data
  median.append(np.median(heading))
  standardDeviation.append(np.std(heading))
  quantiles_25.append(np.quantile(np.sort(heading), 0.25))
  quantiles_75.append(np.quantile(np.sort(heading), 0.75))

  calculatedMinimumValues.append(quantiles_25[i] - 1.5*(quantiles_75[i]-quantiles_25[i]))
  calculatedMaximumValues.append(quantiles_25[i] + 1.5*(quantiles_75[i]-quantiles_25[i]))

# searching for outliers
  outliersPosition = list(np.where(array[1] == "E")[0])
  outliersPosition += list(np.where(heading < calculatedMinimumValues[i])[0])
  outliersPosition += list(np.where(heading > calculatedMaximumValues[i])[0])
  outliers.append(len(outliersPosition))

# updating the data and creating the histogram
  array = np.delete(array, outliersPosition, 0)
  az.hist(array[:, 0].astype('float64'), bins=20, alpha=0.75, histtype='barstacked')

# adding the heading values to the dictionary
  headings[datasets[i]] = heading.astype('float64')

# setting up the plot description
fig1.tight_layout(pad=3.0)
for i in range(ax.shape[0]):
  ax[i].set_xlabel('Times [s]')
ax[0].axes.set_yticks(np.arange(min(minimumValues), max(maximumValues), 2.5))
ax[0].set_ylabel('Declination [$^\circ$]')
ax[2].legend(datasets, loc='best')
# ax[0].axes.set_title('Change of heading')
ax[1].set_yticks(np.arange(min(minimumValues), max(maximumValues), 2.5))
# ax[1].axes.set_title('Change of average heading ')
ax[1].set_ylabel('Average declination [$^\circ$]')
ax[2].axes.set_yscale('linear')
# ax[2].axes.set_title('Change of standard deviation ')
ax[2].set_ylabel('Standard deviation of declination')

#az.axes.set_xticks(np.arange(min(minimumValues), max(maximumValues), 2.5))
az.axes.set_xlabel('Declination [$^\circ$]')
az.axes.set_ylabel('Number of appearances')
az.legend(datasets)
ay.boxplot(headings.values(),whis=1.5,vert = False, usermedians = median,labels=datasets)
ay.axes.set_ylabel('Declination [$^\circ$]')
# saving the graphs
fig1.savefig('results/heading.png')
fig3.savefig('results/boxPlots.png')
fig2.savefig('results/histogram.png')

# saving resulting data to xlsx
data = pd.DataFrame([median, standardDeviation, quantiles_25, quantiles_75, calculatedMinimumValues,
                     calculatedMaximumValues, outliers], columns=datasets, index=requiredData).T
data.to_excel("results/results.xlsx")