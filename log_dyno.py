#%%
file = open('log.log','r')
data = {'Detect':[], 'Match':[], 'Shoot':[]}
while True:
    line = file.readline()
    if not line:
        break
    line = line[26:]
    line = line.split(':')
    data[line[0]].append(float(line[1]))
size = len(data['Detect'])
for i in range(size):
    data['Detect'][i] *= 1000
    data['Match'][i] *= 1000
    data['Shoot'][i] *= 1000
# %%
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
#sns.kdeplot(data['Detect'],shade = True)
detect_data = data['Detect']
print(min(detect_data))
print(max(detect_data))
plt.hist(detect_data, bins=5000)
plt.xlim((min(detect_data),max(detect_data[1:])))
plt.title('Detect time = ms')
plt.show()

# %%
