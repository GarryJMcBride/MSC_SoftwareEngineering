import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



# Test Suites Estimated and actual results
# set width of bar
barWidth = 0.20

# set height of bar
bars1 = [22.67770848311177, 159.11177220600118, 176.7810996985465, 111.68492874213663, 32.46499533446852, -49.50453663458771]
bars2 = [69.9, 69.9, 69.9, 69.9, 69.9, 69.9,]
bars3 = [288.06040054468946, 199.22697455210348, 206.4402327874571, 218.96231303992266, 160.7628508546307, -149.45740827604655]
bars4 = [246.9, 246.9, 246.9, 246.9, 246.9, 246.9]

# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]

# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Estimated Effort (TDL1')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Actual Effort (TDL1)')
plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='Estimated EfforT (TDL2)')
plt.bar(r4, bars4, color='#2B65EC', width=barWidth, edgecolor='white', label='Actual Effort (TDL2')

# Add xticks on the middle of the group bars
plt.ylabel('Count', fontsize=35)
plt.xlabel('RUN', fontsize=35)
plt.title('Estimated and Actual Effort of Test Suites Kemerer', fontsize=35)
plt.xticks([r + barWidth for r in range(len(bars1))], ['RUN 1', 'RUN 2', 'RUN 3', 'RUN 4', 'RUN 5', 'RUN 6'])

# # Create legend & Show graphic
plt.legend()
plt.show()



# Test Suites Estimated and actual results
# set width of bar
barWidth = 0.20

# set height of bar
bars1 = [54.05368468692217, -41.720303610168344, 60.018382928662135, 60.63599985918429, 9.614943170344988, 21.483754021504392]
bars2 = [50.1, 50.1, 50.1, 50.1, 50.1, 50.1]
bars3 = [60.95190165131309, 54.745773594274866, 39.074305332484094, 32.3361420695021, 71.00000000001917, 64.388718890668]
bars4 = [31.5, 31.5, 31.5, 31.5, 31.5, 31.5, ]

# Set position of bar on X axis
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]

# Make the plot
plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Estimated Effort (TDL1')
plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Actual Effort (TDL1)')
plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='Estimated EfforT (TDL2)')
plt.bar(r4, bars4, color='#2B65EC', width=barWidth, edgecolor='white', label='Actual Effort (TDL2')

# Add xticks on the middle of the group bars
plt.ylabel('Count', fontsize=35)
plt.xlabel('RUN', fontsize=35)
plt.title('Estimated and Actual Effort of Test Suites Miyazaki94', fontsize=35)
plt.xticks([r + barWidth for r in range(len(bars1))], ['RUN 1', 'RUN 2', 'RUN 3', 'RUN 4', 'RUN 5', 'RUN 6'])

# # Create legend & Show graphic
plt.legend()
plt.show()
















